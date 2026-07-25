#!/usr/bin/env python3
"""Offline, visible-evidence MIB packet reader.

The implementation intentionally OCRs rendered pages instead of trusting the PDF
text layer.  That keeps hidden/off-page prompt injection out of the evidence
path while remaining small enough for the challenge CPU budget.
"""

from __future__ import annotations

import concurrent.futures
import difflib
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import threading
import time
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import date
from pathlib import Path


SPECIES = (
    "ALPHA_DRACONIAN", "ANDROMEDAN", "AQUARIAN_MANTIS", "ARCTURIAN",
    "CENTAURI_SYNTH", "JOVIAN_GASFORM", "KAIJU_MICRO", "LUNA_SECURID",
    "ORION_GRAYS", "SIRIUS_AVIAN", "TRIANGULAN", "VENUSIAN_MYCELIAL",
)
HOME_WORLDS = (
    "Barnard-c", "Eris Relay", "Europa Station", "Gliese-581g",
    "Kepler-186f", "Luyten-b", "Mars Dome-7", "Proxima-b",
    "Sirius Outpost", "Titan Freeport", "TRAPPIST-1e", "Wolf-1061c",
    "Zeta Reticuli",
)
VISAS = ("TRANSIT-7", "DIP-1", "MED-3", "XW-1", "XW-2")
PURPOSES = (
    "archive audit", "cultural exchange", "diplomatic", "field repair",
    "medical consult", "reactor maintenance", "research", "transit",
    "translation", "xenobotany",
)
RISK_FLAGS = (
    "active_warrant", "biohazard_red", "identity_conflict",
    "illegible_biometrics", "memory_tampering", "planetary_embargo",
    "rescinded_denial", "sponsor_mismatch",
)
DISQUALIFYING = {
    "active_warrant", "biohazard_red", "memory_tampering",
    "planetary_embargo",
}
REVIEW_ONLY = {
    "identity_conflict", "illegible_biometrics", "rescinded_denial",
    "sponsor_mismatch",
}
REVOKED_SPONSORS = {"SPN-0007", "SPN-0139", "SPN-4040"}

_PRINT_LOCK = threading.Lock()
_OCR_VIEW_SEPARATOR = "\n[OCR VIEW 6]\n"
_NATIVE_VIEW_SEPARATOR = "\n[PIXEL-VERIFIED NATIVE TEXT]\n"
_ADJUDICATION_MODEL = json.loads(
    Path(__file__).with_name("adjudication_model.json").read_text(
        encoding="utf-8"
    )
)
_ADJUDICATION_CALIBRATOR = json.loads(
    Path(__file__).with_name("adjudication_calibrator.json").read_text(
        encoding="utf-8"
    )
)


def _normalized(text: str) -> str:
    return (
        text.replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("|", "I")
    )


def _compact(text: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", text.upper())


def _vocabulary_value(text: str, values: tuple[str, ...]) -> str | None:
    compact = _compact(text)
    for value in sorted(values, key=len, reverse=True):
        if _compact(value) in compact:
            return value
    return None


def _labeled_value(text: str, labels: tuple[str, ...]) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    label_pattern = "|".join(re.escape(label) for label in labels)
    next_field = re.compile(
        r"^(?:case\s+id|applicant(?:\s+name)?|registry\s+name|"
        r"species(?:\s+code|\s+match)?|home\s+world|visa\s+class|"
        r"sponsor(?:\s+id)?|arrival\s+date|declared\s+purpose|purpose|"
        r"observed\s+flags?|fee\s+status|payment\s+status|amount|"
        r"waiver\s+code)\b",
        re.I,
    )
    for index, line in enumerate(lines):
        match = re.search(
            rf"\b(?:{label_pattern})\b\s*(?:[:#-]\s*)?(.+)?$",
            line,
            flags=re.IGNORECASE,
        )
        if not match:
            continue
        value = (match.group(1) or "").strip(" :|-")
        if value and not re.fullmatch(r"(record|status|information)", value, re.I):
            return value
        if index + 1 < len(lines):
            candidate = lines[index + 1].strip(" :|-")
            if not next_field.match(candidate):
                return candidate
    return None


def _labeled_values(text: str, labels: tuple[str, ...]) -> list[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    label_pattern = "|".join(re.escape(label) for label in labels)
    values: list[str] = []
    for index, line in enumerate(lines):
        match = re.search(
            rf"\b(?:{label_pattern})\b\s*(?:[:#-]\s*)?(.+)?$",
            line,
            flags=re.IGNORECASE,
        )
        if not match:
            continue
        value = (match.group(1) or "").strip(" :|-")
        if not value and index + 1 < len(lines):
            candidate = lines[index + 1].strip(" :|-")
            if not re.match(
                r"^(?:case\s+id|applicant(?:\s+name)?|registry\s+name|"
                r"species(?:\s+code|\s+match)?|home\s+world|visa\s+class|"
                r"sponsor(?:\s+id)?|arrival\s+date|declared\s+purpose|"
                r"purpose|observed\s+flags?|fee\s+status|payment\s+status|"
                r"amount|waiver\s+code)\b",
                candidate,
                re.I,
            ):
                value = candidate
        if value:
            values.append(value)
    return values


def _fuzzy_closed_value(
    text: str,
    labels: tuple[str, ...],
    values: tuple[str, ...],
    threshold: float = 0.70,
) -> str | None:
    exact = _vocabulary_value(text, values)
    if exact:
        return exact
    best: tuple[float, str] = (0.0, "")
    for candidate in _labeled_values(text, labels):
        candidate_key = _compact(candidate)
        for value in values:
            value_key = _compact(value)
            score = difflib.SequenceMatcher(None, candidate_key, value_key).ratio()
            if score > best[0]:
                best = (score, value)
    return best[1] if best[0] >= threshold else None


def _ocr_page(image: Path, psm: int = 4) -> str:
    command = [
        "tesseract", str(image), "stdout", "--psm", str(psm),
        "-l", "eng", "-c", "preserve_interword_spaces=1",
    ]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        timeout=20,
        check=False,
    )
    return _normalized(result.stdout)


def _read_pgm(path: Path) -> tuple[int, int, bytes]:
    data = path.read_bytes()
    match = re.match(
        br"P5\s+(?:#[^\r\n]*[\r\n]+\s*)*(\d+)\s+(\d+)\s+(\d+)\s",
        data,
    )
    if not match or int(match.group(3)) != 255:
        raise ValueError(f"unsupported PGM header: {path.name}")
    return int(match.group(1)), int(match.group(2)), data[match.end():]


def _word_has_visible_ink(
    word: ET.Element,
    page_width: float,
    page_height: float,
    image_width: int,
    image_height: int,
    pixels: bytes,
) -> bool:
    try:
        x0 = float(word.attrib["xMin"]) * image_width / page_width
        y0 = float(word.attrib["yMin"]) * image_height / page_height
        x1 = float(word.attrib["xMax"]) * image_width / page_width
        y1 = float(word.attrib["yMax"]) * image_height / page_height
    except (KeyError, ValueError, ZeroDivisionError):
        return False
    if x1 <= 0 or y1 <= 0 or x0 >= image_width or y0 >= image_height:
        return False
    left = max(0, int(x0))
    top = max(0, int(y0))
    right = min(image_width, max(left + 1, int(x1 + 1)))
    bottom = min(image_height, max(top + 1, int(y1 + 1)))
    area = (right - left) * (bottom - top)
    if area <= 0:
        return False
    dark = 0
    darkest = 255
    for row in range(top, bottom):
        sample = pixels[row * image_width + left:row * image_width + right]
        if sample:
            darkest = min(darkest, min(sample))
            dark += sum(value < 210 for value in sample)
    return darkest < 185 and dark / area >= 0.012


def _pixel_verified_native_pages(
    pdf: Path,
    images: list[Path],
    temp_dir: Path,
) -> list[str]:
    bbox_path = temp_dir / "native-bbox.html"
    result = subprocess.run(
        ["pdftotext", "-bbox-layout", str(pdf), str(bbox_path)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=20,
        check=False,
    )
    if result.returncode != 0 or not bbox_path.exists():
        return [""] * len(images)
    try:
        root = ET.parse(bbox_path).getroot()
    except ET.ParseError:
        return [""] * len(images)

    namespace = {"x": "http://www.w3.org/1999/xhtml"}
    xml_pages = root.findall(".//x:page", namespace)
    verified_pages: list[str] = []
    for index, image in enumerate(images):
        if index >= len(xml_pages):
            verified_pages.append("")
            continue
        xml_page = xml_pages[index]
        try:
            page_width = float(xml_page.attrib["width"])
            page_height = float(xml_page.attrib["height"])
            image_width, image_height, pixels = _read_pgm(image)
        except (KeyError, ValueError):
            verified_pages.append("")
            continue
        lines = []
        for line in xml_page.findall(".//x:line", namespace):
            words = []
            for word in line.findall("./x:word", namespace):
                value = "".join(word.itertext()).strip()
                if value and _word_has_visible_ink(
                    word,
                    page_width,
                    page_height,
                    image_width,
                    image_height,
                    pixels,
                ):
                    words.append(value)
            visible_line = " ".join(words)
            if visible_line and not re.search(
                r"answer\s+key|ignore\s+visible|system\s*:|"
                r"barcode\s+payload|force\s+adjudication",
                visible_line,
                re.I,
            ):
                lines.append(visible_line)
        verified_pages.append("\n".join(lines))
    return verified_pages


def _render_and_ocr(pdf: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix="mib-") as temp:
        temp_dir = Path(temp)
        prefix = temp_dir / "page"
        subprocess.run(
            ["pdftoppm", "-gray", "-r", "180",
             str(pdf), str(prefix)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30,
            check=True,
        )
        images = sorted(temp_dir.glob("page-*.pgm"))
        native_pages = _pixel_verified_native_pages(pdf, images, temp_dir)
        expected_id = pdf.stem.upper()
        for index, native_page in enumerate(native_pages):
            page_ids = {
                f"MIB-{match}"
                for match in re.findall(r"\bMIB[- ]?(\d{6})\b", native_page, re.I)
            }
            if any(page_id != expected_id for page_id in page_ids):
                native_pages[index] = ""
        return [
            _ocr_page(image, 11)
            + _OCR_VIEW_SEPARATOR
            + _ocr_page(image, 6)
            + _NATIVE_VIEW_SEPARATOR
            + native_pages[index]
            for index, image in enumerate(images)
        ]


def _extract_date(text: str, label: str) -> str | None:
    for value in _labeled_values(text, (label,)):
        match = re.search(r"\b(20\d{2})[-/.](\d{2})[-/.](\d{2})\b", value)
        if match:
            candidate = "-".join(match.groups())
            try:
                date.fromisoformat(candidate)
            except ValueError:
                continue
            return candidate
    return None


def _extract_scoped_flags(case_id: str, pages: list[str]) -> tuple[list[str], str]:
    eligible_pages = []
    biometric_page_seen = False
    expected_id = case_id.split("-")[-1]
    for page in pages:
        if not re.search(r"FORM\s+B-13|Biometric\s+Scan\s+Slip", page, re.I):
            continue
        biometric_page_seen = True
        visible_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
        if expected_id in visible_ids and not any(
            visible_id != expected_id for visible_id in visible_ids
        ):
            eligible_pages.append(page)
    text = "\n".join(eligible_pages)

    trusted_lines = [
        line for line in text.splitlines()
        if not re.search(r"barcode\s+payload|answer\s+key|force\s+adjudication", line, re.I)
    ]
    trusted = "\n".join(trusted_lines)
    normalized = re.sub(r"[\s-]+", "_", trusted.lower())
    found: list[str] = []
    for flag in RISK_FLAGS:
        words = flag.split("_")
        pattern = r"[_\W]*".join(re.escape(word) for word in words)
        if re.search(pattern, normalized, flags=re.I):
            found.append(flag)
    if found:
        return found, "positive"

    # Damaged B-13 slips often preserve the label while corrupting one or two
    # glyphs in the value.  Restrict fuzzy repair to that scoped label.
    for candidate in _labeled_values(trusted, ("Observed flags", "Observed flag")):
        if re.search(r"\bnone\b", candidate, re.I):
            return [], "clean"
        pieces = re.split(r"[,|;/]+", candidate)
        for piece in pieces:
            piece_key = _compact(piece)
            matches = [
                (difflib.SequenceMatcher(None, piece_key, _compact(flag)).ratio(), flag)
                for flag in RISK_FLAGS
            ]
            score, flag = max(matches)
            if score >= 0.60 and flag not in found:
                found.append(flag)
    for line in trusted_lines:
        marker = re.search(r"\b(?:flags?|fags?)\b\s*[:=-]?\s*(.*)$", line, re.I)
        if not marker:
            continue
        if difflib.SequenceMatcher(
            None, _compact(line[:marker.start()]), "OBSERVED"
        ).ratio() < 0.45:
            continue
        for piece in re.split(r"[,|;/]+", marker.group(1)):
            if len(_compact(piece)) < 5:
                continue
            score, flag = max(
                (
                    difflib.SequenceMatcher(
                        None, _compact(piece), _compact(flag)
                    ).ratio(),
                    flag,
                )
                for flag in RISK_FLAGS
            )
            if score >= 0.52 and flag not in found:
                found.append(flag)
    if found:
        return found, "positive"
    if re.search(r"observed\s+flags?\s*:?\s*(?:\n\s*)?none\b", trusted, re.I):
        return [], "clean"
    return [], "unknown" if biometric_page_seen else "absent"


def _extract_visible_flags(text: str) -> list[str]:
    trusted_lines = [
        line for line in text.splitlines()
        if not re.search(
            r"barcode\s+payload|answer\s+key|force\s+adjudication",
            line,
            re.I,
        )
    ]
    trusted = "\n".join(trusted_lines)
    normalized = re.sub(r"[\s-]+", "_", trusted.lower())
    found = [
        flag
        for flag in RISK_FLAGS
        if re.search(
            r"[_\W]*".join(re.escape(word) for word in flag.split("_")),
            normalized,
            re.I,
        )
    ]
    if found:
        return found
    for candidate in _labeled_values(trusted, ("Observed flags", "Observed flag")):
        if re.search(r"\bnone\b", candidate, re.I):
            continue
        for piece in re.split(r"[,|;/]+", candidate):
            score, flag = max(
                (
                    difflib.SequenceMatcher(
                        None, _compact(piece), _compact(flag)
                    ).ratio(),
                    flag,
                )
                for flag in RISK_FLAGS
            )
            if score >= 0.60 and flag not in found:
                found.append(flag)
    for line in trusted_lines:
        marker = re.search(r"\b(?:flags?|fags?)\b\s*[:=-]?\s*(.*)$", line, re.I)
        if not marker:
            continue
        if difflib.SequenceMatcher(
            None, _compact(line[:marker.start()]), "OBSERVED"
        ).ratio() < 0.45:
            continue
        for piece in re.split(r"[,|;/]+", marker.group(1)):
            if len(_compact(piece)) < 5:
                continue
            score, flag = max(
                (
                    difflib.SequenceMatcher(
                        None, _compact(piece), _compact(flag)
                    ).ratio(),
                    flag,
                )
                for flag in RISK_FLAGS
            )
            if score >= 0.52 and flag not in found:
                found.append(flag)
    return found


def _supplementary_decision(case_id: str, pages: list[str]) -> str | None:
    expected_id = case_id.split("-")[-1]
    candidates: set[str] = set()
    lower_precedence = re.compile(
        r"registry\s+extract|fee\s+receipt|sponsor\s+attestation|"
        r"work\s+authorization\s+intake|biometric\s+scan",
        re.I,
    )
    class_patterns = {
        "APPROVED": re.compile(r"\bAPPROVED\b", re.I),
        "DENIED": re.compile(r"\bDENIED\b", re.I),
        "NEEDS_REVIEW": re.compile(r"\bNEEDS[\s_-]*REVIEW\b", re.I),
    }

    for page in pages:
        visible_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
        if any(visible_id != expected_id for visible_id in visible_ids):
            continue

        exact_heading = bool(
            re.search(r"\bManual\s+Adjudicator\s+Note\b", page, re.I)
        )
        if exact_heading:
            page_candidates: set[str] = set()
            views = re.split(
                rf"{re.escape(_OCR_VIEW_SEPARATOR)}|"
                rf"{re.escape(_NATIVE_VIEW_SEPARATOR)}",
                page,
            )
            for view in views:
                before_reason = re.split(r"\bReason\s*:", view, maxsplit=1, flags=re.I)[0]
                for decision, pattern in class_patterns.items():
                    if pattern.search(before_reason):
                        page_candidates.add(decision)

                for line in before_reason.splitlines():
                    words = re.findall(r"[A-Za-z_]+", line)
                    if len(words) >= 2:
                        label_score = difflib.SequenceMatcher(
                            None, _compact(words[-2]), "FINDING"
                        ).ratio()
                        value = _compact(words[-1])
                        scored = [
                            (
                                difflib.SequenceMatcher(
                                    None, value, _compact(decision)
                                ).ratio(),
                                decision,
                            )
                            for decision in ("DENIED", "APPROVED", "NEEDS_REVIEW")
                        ]
                        score, decision = max(scored)
                        threshold = 0.78 if decision == "NEEDS_REVIEW" else 0.80
                        if label_score >= 0.60 and score >= threshold:
                            page_candidates.add(decision)

                if not page_candidates:
                    for token in re.findall(r"[A-Za-z_]{6,}", before_reason):
                        scored = [
                            (
                                difflib.SequenceMatcher(
                                    None, _compact(token), _compact(decision)
                                ).ratio(),
                                decision,
                            )
                            for decision in ("DENIED", "APPROVED")
                        ]
                        score, decision = max(scored)
                        threshold = 0.83 if decision == "DENIED" else 0.87
                        if score >= threshold:
                            page_candidates.add(decision)
            if len(page_candidates) == 1:
                candidates.update(page_candidates)
            continue

        if lower_precedence.search(page):
            continue
        reason = re.search(r"\bReason\s*:\s*(.+)", page, re.I)
        if not reason:
            continue
        reason_text = reason.group(1)
        if re.search(
            r"planetary[_\s-]*embargo|mandatory\s+fee\s+unpaid|"
            r"active[_\s-]*warrant|memory[_\s-]*tampering|"
            r"biohazard[_\s-]*red",
            reason_text,
            re.I,
        ) and not re.search(r"rescinded\s+denial", reason_text, re.I):
            candidates.add("DENIED")

    return next(iter(candidates)) if len(candidates) == 1 else None


def _model_feature_row(
    applicant: str | None,
    species: str | None,
    home_world: str | None,
    visa: str | None,
    sponsor: str | None,
    arrival: str | None,
    purpose: str | None,
    visible_flags: list[str],
    fee: str | None,
    current_decision: str,
) -> dict[str, object]:
    arrival_age = -1
    if arrival:
        try:
            reference = date.fromisoformat(
                _ADJUDICATION_MODEL["reference_date"]
            )
            arrival_age = (reference - date.fromisoformat(arrival)).days
        except ValueError:
            pass
    flag_set = set(visible_flags)
    return {
        "species": species or "unknown",
        "home_world": home_world or "unknown",
        "visa": visa or "unknown",
        "purpose": purpose or "unknown",
        "fee": fee or "unknown",
        "current_decision": current_decision,
        "manual_revoked": sponsor in REVOKED_SPONSORS,
        "arrival_age": arrival_age,
        "known_name": applicant is not None,
        "known_species": species is not None,
        "known_home": home_world is not None,
        "known_visa": visa is not None,
        "known_sponsor": sponsor is not None,
        "known_arrival": arrival is not None,
        "known_purpose": purpose is not None,
        "known_fee": fee is not None,
        "flag_count": len(flag_set),
        **{f"flag_{flag}": flag in flag_set for flag in RISK_FLAGS},
    }


def _model_probabilities(features: dict[str, object]) -> list[float]:
    vector: list[float] = []
    for column, categories in _ADJUDICATION_MODEL["categorical"].items():
        vector.extend(
            float(features[column] == category) for category in categories
        )
    for column, median in _ADJUDICATION_MODEL["numeric_medians"].items():
        value = features.get(column)
        vector.append(float(median if value is None else value))

    scores = list(_ADJUDICATION_MODEL["baseline"])
    for iteration in _ADJUDICATION_MODEL["trees"]:
        for class_index, nodes in enumerate(iteration):
            node_index = 0
            while True:
                node = nodes[node_index]
                if node["is_leaf"]:
                    scores[class_index] += node["value"]
                    break
                value = vector[node["feature_idx"]]
                if math.isnan(value):
                    go_left = node["missing_go_to_left"]
                else:
                    go_left = value <= node["threshold"]
                node_index = node["left"] if go_left else node["right"]

    offset = max(scores)
    exponentials = [math.exp(score - offset) for score in scores]
    total = sum(exponentials)
    return [value / total for value in exponentials]


def _model_confidence(
    probabilities: list[float],
    modeled_decision: str,
    base_decision: str,
) -> float:
    classes = _ADJUDICATION_MODEL["classes"]
    by_class = dict(zip(classes, probabilities, strict=True))
    ordered = sorted(probabilities)
    maximum = ordered[-1]
    values = [
        by_class["APPROVED"],
        by_class["DENIED"],
        by_class["NEEDS_REVIEW"],
        by_class[modeled_decision],
        maximum,
        maximum - ordered[-2],
        -sum(value * math.log(max(value, 1e-12)) for value in probabilities),
        *[float(modeled_decision == value) for value in classes],
        *[float(base_decision == value) for value in classes],
    ]
    standardized = [
        (value - mean) / scale
        for value, mean, scale in zip(
            values,
            _ADJUDICATION_CALIBRATOR["mean"],
            _ADJUDICATION_CALIBRATOR["scale"],
            strict=True,
        )
    ]
    logit = _ADJUDICATION_CALIBRATOR["intercept"] + sum(
        coefficient * value
        for coefficient, value in zip(
            _ADJUDICATION_CALIBRATOR["coefficient"],
            standardized,
            strict=True,
        )
    )
    return 1.0 / (1.0 + math.exp(-logit))


def _model_decision(features: dict[str, object]) -> tuple[str, float]:
    classes = _ADJUDICATION_MODEL["classes"]
    probabilities = _model_probabilities(features)
    by_class = dict(zip(classes, probabilities, strict=True))
    utilities = {
        "APPROVED": (
            8 * by_class["APPROVED"]
            - 4 * by_class["DENIED"]
            + by_class["NEEDS_REVIEW"]
        ),
        "DENIED": (
            8 * by_class["DENIED"] + by_class["NEEDS_REVIEW"]
        ),
        "NEEDS_REVIEW": (
            2 * by_class["APPROVED"]
            + 2 * by_class["DENIED"]
            + 8 * by_class["NEEDS_REVIEW"]
        ),
    }
    decision = max(utilities, key=utilities.get)
    ceiling = _ADJUDICATION_MODEL["decision"][
        "approval_denial_ceiling"
    ]
    if decision == "APPROVED" and by_class["DENIED"] > ceiling:
        decision = "NEEDS_REVIEW"
    confidence = _model_confidence(
        probabilities,
        decision,
        str(features["current_decision"]),
    )
    return decision, confidence


def _explicit_decision(case_id: str, pages: list[str]) -> str | None:
    trusted_pages = []
    for page in pages:
        lower = page.lower()
        typed_note = "manual adjudicator note" in lower
        isolated_finding = bool(
            re.search(r"\bfinding\b", page, re.I)
            and not re.search(
                r"registry extract|fee receipt|sponsor attestation|"
                r"work authorization intake|biometric scan",
                page,
                re.I,
            )
        )
        signed_stamp = bool(re.search(
            r"MIB\s+(?:decision|adjudication)\s+stamp|signed\s+finding",
            page,
            re.I,
        ))
        if typed_note or isolated_finding or signed_stamp:
            trusted_pages.append(page)
    text = "\n".join(trusted_pages)
    clean_lines = []
    for line in text.splitlines():
        if re.search(
            r"sample\s+denial|training\s+example|answer\s+key|"
            r"barcode\s+payload|force\s+adjudication",
            line,
            re.I,
        ):
            continue
        clean_lines.append(line)
    clean = "\n".join(clean_lines)
    decision = r"(APPROVED|DENIED|NEEDS[\s_-]*REVIEW)"
    patterns = (
        rf"(?:finding|final\s+decision|adjudication|decision|status)\s*[:=-]?\s*{decision}",
        rf"\b{decision}\b\s+(?:STAMP|SIGNED|FINAL)\b",
        rf"\b(?:STAMP|SIGNED|FINAL)\b\s*[:=-]?\s*{decision}",
    )
    for pattern in patterns:
        match = re.search(pattern, clean, flags=re.I)
        if match:
            token = re.sub(r"[\s_-]+", "_", match.group(1).upper())
            return token

    for line in clean.splitlines():
        if not re.search(r"finding|decision|adjudication", line, re.I):
            continue
        tail = re.split(r"finding|decision|adjudication", line, flags=re.I)[-1]
        tail_key = _compact(tail)
        matches = [
            (difflib.SequenceMatcher(None, tail_key, _compact(value)).ratio(), value)
            for value in ("APPROVED", "DENIED", "NEEDS_REVIEW")
        ]
        score, value = max(matches)
        if score >= 0.58:
            return value

    if re.search(r"reason\s*:?.*(?:mandatory\s+fee\s+unpaid|embargo(?:ed)?\s+home\s+world)", clean, re.I):
        return "DENIED"
    if re.search(r"reason\s*:?.*(?:damaged|contradictory|incomplete).*(?:evidence|packet)", clean, re.I):
        return "NEEDS_REVIEW"
    return _supplementary_decision(case_id, pages)


def _parse_packet(case_id: str, pages: list[str]) -> dict:
    text = "\n\n".join(pages)

    applicant_candidates = _labeled_values(
        text, ("Applicant Name", "Applicant", "Registry Name")
    )
    applicant_candidates.extend(
        match.group(1).strip()
        for match in re.finditer(
            r"attests\s+that\s+([A-Za-z][A-Za-z' -]{2,60}?)\s+is\s+expected",
            text,
            re.I,
        )
    )
    cleaned_names = []
    document_words = {
        "applicant name", "species code", "home world", "visa class",
        "sponsor id", "arrival date", "declared purpose", "registry status",
        "passport image", "scan image",
    }
    for candidate in applicant_candidates:
        candidate = re.sub(r"\s{2,}.*$", "", candidate).strip()
        if (
            re.fullmatch(r"[A-Za-z][A-Za-z'-]+ [A-Za-z][A-Za-z'-]+", candidate)
            and candidate.lower() not in document_words
            and not re.search(r"cut out|unknown|whiteout", candidate, re.I)
        ):
            cleaned_names.append(candidate)
    applicant = Counter(cleaned_names).most_common(1)[0][0] if cleaned_names else None

    species = _fuzzy_closed_value(
        text, ("Species Code", "Species Match"), SPECIES, 0.67
    )
    home_world = _fuzzy_closed_value(text, ("Home World",), HOME_WORLDS, 0.66)
    visa = _fuzzy_closed_value(text, ("Visa Class",), VISAS, 0.64)

    attestation_sponsors = [
        re.sub(r"\D", "", match.group(1))
        for match in re.finditer(
            r"\bsponsor\s+SPN[-_ ]?((?:\d[\s-]*){4})\s+attests\b",
            text,
            flags=re.I,
        )
    ]
    sponsor_numbers = [
        re.sub(r"\D", "", match.group(1))
        for match in re.finditer(
            r"\bSPN[-_ ]?((?:\d[\s-]*){4})\b", text, flags=re.I
        )
    ]
    sponsor_numbers = [number for number in sponsor_numbers if len(number) == 4]
    correction = re.search(
        r"manual\s+correction\s*:\s*sponsor(?:\s+id)?\s+is\s+"
        r"SPN[-_ ]?((?:\d[\s-]*){4})",
        text,
        re.I,
    )
    if correction:
        sponsor_number = re.sub(r"\D", "", correction.group(1))
    elif attestation_sponsors:
        sponsor_number = Counter(attestation_sponsors).most_common(1)[0][0]
    elif sponsor_numbers:
        sponsor_number = Counter(sponsor_numbers).most_common(1)[0][0]
    else:
        sponsor_number = None
    sponsor = f"SPN-{sponsor_number}" if sponsor_number else None
    arrival = _extract_date(text, "Arrival Date")
    purpose = _fuzzy_closed_value(
        text, ("Declared Purpose", "Purpose"), PURPOSES, 0.66
    )
    flags, flags_state = _extract_scoped_flags(case_id, pages)
    visible_flags = _extract_visible_flags(text)

    fee = None
    for page in pages:
        if not re.search(r"fee|receipt|payment", page, re.I):
            continue
        status_match = re.search(r"\b(paid|unpaid|waived|unknown)\b", page, re.I)
        if status_match:
            fee = status_match.group(1).lower()
            break
        if re.search(r"(?:\$\s*)?809(?:[.,]00)?\b", page):
            fee = "paid"
            break
        if (
            re.search(r"(?:\$\s*)?0[.,]00\b", page)
            and re.search(r"\bwaiver\b", page, re.I)
        ):
            fee = "waived"
            break
    if re.search(r"reason\s*:?.*mandatory\s+fee\s+unpaid", text, re.I):
        fee = "unpaid"

    revoked_mentions = {
        f"SPN-{re.sub(r'\\D', '', match.group(1))}"
        for match in re.finditer(
            r"revoked\s+sponsor\s*[:#-]?\s*SPN[-_ ]?((?:\d[\s-]*){4})",
            text,
            re.I,
        )
    }

    decision = _explicit_decision(case_id, pages)
    direct_decision = decision is not None
    if decision is None:
        if set(flags) & DISQUALIFYING:
            decision = "DENIED"
        elif visa == "TRANSIT-7":
            decision = "DENIED"
        elif sponsor in (REVOKED_SPONSORS | revoked_mentions) and visa != "DIP-1":
            decision = "DENIED"
        elif fee == "unpaid":
            decision = "DENIED"
        elif set(flags) & REVIEW_ONLY:
            decision = "NEEDS_REVIEW"
        elif fee == "waived" and visa != "DIP-1" and not re.search(
            r"(?:hardship|authorized)\s+waiver|waiver\s+(?:approved|granted)",
            text,
            re.I,
        ):
            decision = "NEEDS_REVIEW"
        elif fee in (None, "unknown"):
            decision = "NEEDS_REVIEW"
        elif flags_state == "unknown":
            decision = "NEEDS_REVIEW"
        elif not all((applicant, species, home_world, visa, arrival, purpose)):
            decision = "NEEDS_REVIEW"
        else:
            decision = "APPROVED"

    modeled_confidence = None
    if not direct_decision and decision != "DENIED":
        model_features = _model_feature_row(
            applicant,
            species,
            home_world,
            visa,
            sponsor,
            arrival,
            purpose,
            visible_flags,
            fee,
            decision,
        )
        decision, modeled_confidence = _model_decision(model_features)

    if modeled_confidence is not None:
        confidence = modeled_confidence
    elif direct_decision:
        confidence = 0.99
    elif decision == "DENIED":
        confidence = 0.94
    elif decision == "NEEDS_REVIEW":
        confidence = 0.38
    else:
        confidence = 0.58

    # Keep unresolved fee evidence unknown to the adjudication head.  For the
    # extraction output only, use the public-training modal class as a bounded
    # candidate-trained fallback.
    output_fee = fee or "paid"

    return {
        "case_id": case_id,
        "applicant_name": applicant or "unknown",
        "species_code": species or "unknown",
        "home_world": home_world or "unknown",
        "visa_class": visa or "unknown",
        "sponsor_id": sponsor or "SPN-0000",
        "arrival_date": arrival or "1900-01-01",
        "declared_purpose": purpose or "unknown",
        "risk_flags": "|".join(visible_flags) if visible_flags else "none",
        "fee_status": output_fee,
        "adjudication": decision,
        "confidence": confidence,
    }


def _process(pdf: Path) -> dict:
    try:
        return _parse_packet(pdf.stem, _render_and_ocr(pdf))
    except Exception as error:
        with _PRINT_LOCK:
            print(f"warning: {pdf.stem}: {type(error).__name__}: {error}", file=sys.stderr)
        return {
            "case_id": pdf.stem,
            "applicant_name": "unknown",
            "species_code": "unknown",
            "home_world": "unknown",
            "visa_class": "unknown",
            "sponsor_id": "SPN-0000",
            "arrival_date": "1900-01-01",
            "declared_purpose": "unknown",
            "risk_flags": "none",
            "fee_status": "unknown",
            "adjudication": "NEEDS_REVIEW",
            "confidence": 0.15,
        }


def main(input_dir: str, output_path: str) -> None:
    pdfs = sorted(Path(input_dir).glob("*.pdf"))
    workers = max(1, min(int(os.environ.get("MIB_MAX_WORKERS", "4")), 4))
    started = time.monotonic()
    predictions: dict[str, dict] = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(_process, pdf): pdf for pdf in pdfs}
        for completed, future in enumerate(concurrent.futures.as_completed(futures), 1):
            pdf = futures[future]
            predictions[pdf.stem] = future.result()
            with _PRINT_LOCK:
                elapsed = time.monotonic() - started
                print(
                    f"[{completed}/{len(pdfs)}] {pdf.stem} "
                    f"elapsed={elapsed:.1f}s rate={completed / max(elapsed, 0.01):.2f}/s",
                    file=sys.stderr,
                    flush=True,
                )

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for pdf in pdfs:
            handle.write(json.dumps(predictions[pdf.stem], sort_keys=True) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: solution.py <input_pdf_dir> <output_path>")
    main(sys.argv[1], sys.argv[2])
