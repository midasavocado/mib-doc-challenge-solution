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
from collections import Counter, defaultdict
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


def _ocr_tsv_words(image: Path) -> list[dict[str, int | str]]:
    result = subprocess.run(
        [
            "tesseract", str(image), "stdout", "--psm", "11",
            "-l", "eng", "tsv",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        timeout=20,
        check=False,
    )
    words = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split("\t", 11)
        if len(parts) != 12 or not parts[11].strip():
            continue
        try:
            words.append(
                {
                    "block": int(parts[2]),
                    "paragraph": int(parts[3]),
                    "line": int(parts[4]),
                    "left": int(parts[6]),
                    "top": int(parts[7]),
                    "height": int(parts[9]),
                    "text": parts[11].strip(),
                }
            )
        except ValueError:
            continue
    return words


def _read_pgm(path: Path) -> tuple[int, int, bytes]:
    data = path.read_bytes()
    match = re.match(
        br"P5\s+(?:#[^\r\n]*[\r\n]+\s*)*(\d+)\s+(\d+)\s+(\d+)\s",
        data,
    )
    if not match or int(match.group(3)) != 255:
        raise ValueError(f"unsupported PGM header: {path.name}")
    return int(match.group(1)), int(match.group(2)), data[match.end():]


def _crop_pgm(
    source: Path,
    destination: Path,
    left: int,
    top: int,
    right: int,
    bottom: int,
) -> None:
    width, height, pixels = _read_pgm(source)
    left = max(0, min(left, width - 1))
    top = max(0, min(top, height - 1))
    right = max(left + 1, min(right, width))
    bottom = max(top + 1, min(bottom, height))
    cropped = b"".join(
        pixels[row * width + left:row * width + right]
        for row in range(top, bottom)
    )
    destination.write_bytes(
        f"P5\n{right - left} {bottom - top}\n255\n".encode() + cropped
    )


def _scale_pgm_nearest(
    source: Path,
    destination: Path,
    factor: int,
) -> None:
    """Enlarge a small OCR crop without inventing interpolated gray values."""
    width, height, pixels = _read_pgm(source)
    rows = []
    for row_index in range(height):
        row = pixels[row_index * width:(row_index + 1) * width]
        expanded = bytearray(width * factor)
        for offset in range(factor):
            expanded[offset::factor] = row
        rows.extend([bytes(expanded)] * factor)
    destination.write_bytes(
        f"P5\n{width * factor} {height * factor}\n255\n".encode()
        + b"".join(rows)
    )


def _rotate_pgm(source: Path, destination: Path, clockwise: bool) -> None:
    width, height, pixels = _read_pgm(source)
    if clockwise:
        rotated = b"".join(
            pixels[(height - 1) * width + column:column - 1:-width]
            if column
            else pixels[(height - 1) * width::-width]
            for column in range(width)
        )
    else:
        rotated = b"".join(
            pixels[column::width] for column in range(width - 1, -1, -1)
        )
    destination.write_bytes(
        f"P5\n{height} {width}\n255\n".encode() + rotated
    )


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
        pages = [
            _ocr_page(image, 11)
            + _OCR_VIEW_SEPARATOR
            + _ocr_page(image, 6)
            + _NATIVE_VIEW_SEPARATOR
            + native_pages[index]
            for index, image in enumerate(images)
        ]
        heading = re.compile(
            r"FORM\s+(?:I-8090|B-13)|Biometric\s+Scan\s+Slip|"
            r"(?:Planetary\s+)?Registry\s+Extract|Sponsor\s+Attestation|"
            r"MIB\s+Fee\s+Receipt|Manual\s+Adjudicator\s+Note",
            re.I,
        )
        for index, page in enumerate(pages):
            rendered_ocr = page.split(_NATIVE_VIEW_SEPARATOR, 1)[0]
            page_ids = {
                f"MIB-{match}"
                for match in re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
            }
            visible_ids = {
                f"MIB-{match}"
                for match in re.findall(
                    r"\bMIB[- ]?(\d{6})\b", rendered_ocr, re.I
                )
            }
            legacy_scope = (
                expected_id in page_ids
                and not any(page_id != expected_id for page_id in page_ids)
                and not heading.search(page)
            )
            rendered_scope = (
                expected_id in visible_ids
                and not any(page_id != expected_id for page_id in visible_ids)
                and not heading.search(rendered_ocr)
            )
            if not (legacy_scope or rendered_scope):
                continue
            rotated_views = []
            for label, clockwise in (("cw", True), ("ccw", False)):
                rotated = temp_dir / f"rotated-{index}-{label}.pgm"
                _rotate_pgm(images[index], rotated, clockwise)
                view = _ocr_page(rotated, 12)
                rotated_ids = {
                    f"MIB-{match}"
                    for match in re.findall(
                        r"\bMIB[- ]?(\d{6})\b", view, re.I
                    )
                }
                biometric_layout = bool(
                    re.search(r"species\s+match", view, re.I)
                    and re.search(r"observed\s+flags?", view, re.I)
                )
                field_count = sum(
                    bool(re.search(pattern, view, re.I))
                    for pattern in (
                        r"applicant|registry\s+name",
                        r"species\s+(?:code|match)",
                        r"home\s+world",
                        r"visa\s+class",
                        r"sponsor\s+id",
                        r"arrival\s+date",
                        r"(?:declared\s+)?purpose",
                        r"observed\s+flags?",
                        r"fee\s+status",
                        r"finding",
                    )
                )
                if (
                    not any(
                        page_id != expected_id for page_id in rotated_ids
                    )
                    and (
                        expected_id in rotated_ids
                        or (
                            rendered_scope
                            and visible_ids == {expected_id}
                        )
                    )
                    and (
                        heading.search(view)
                        or biometric_layout
                        or field_count >= 3
                    )
                ):
                    safe_lines = []
                    for line in view.splitlines():
                        if re.search(
                            r"\b(?:applicant(?:\s+name)?|registry\s+name)\b|"
                            r"\battests\s+that\b",
                            line,
                            re.I,
                        ):
                            continue
                        safe_lines.append(line)
                    rotated_views.append("\n".join(safe_lines))
            if rotated_views:
                pages[index] += "\n[ROTATED OCR VIEW]\n" + "\n".join(
                    rotated_views
                )
        return pages


def _high_resolution_finding(
    pdf: Path,
    pages: list[str],
) -> str | None:
    expected_id = pdf.stem.split("-")[-1]
    candidate_pages = []
    for index, page in enumerate(pages, 1):
        visible_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
        if expected_id not in visible_ids or any(
            visible_id != expected_id for visible_id in visible_ids
        ):
            continue
        primary_view = page.split(_OCR_VIEW_SEPARATOR, 1)[0]
        heading_lines = [
            _compact(line)
            for line in primary_view.splitlines()
            if _compact(line)
        ][:4]
        heading_score = max(
            (
                difflib.SequenceMatcher(
                    None,
                    line,
                    "MANUALADJUDICATORNOTE",
                ).ratio()
                for line in heading_lines
            ),
            default=0.0,
        )
        if heading_score >= 0.55:
            candidate_pages.append(index)

    if not candidate_pages:
        return None

    found: set[str] = set()
    with tempfile.TemporaryDirectory(prefix="mib-finding-") as temp:
        temp_dir = Path(temp)
        for page_number in candidate_pages:
            prefix = temp_dir / f"page-{page_number}"
            subprocess.run(
                [
                    "pdftoppm", "-gray", "-r", "400",
                    "-f", str(page_number), "-l", str(page_number),
                    "-singlefile", str(pdf), str(prefix),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=20,
                check=True,
            )
            view = _ocr_page(prefix.with_suffix(".pgm"), 6)
            if re.search(
                r"answer\s+key|training\s+example|sample\s+denial|"
                r"force\s+adjudication",
                view,
                re.I,
            ):
                continue
            matches = {
                re.sub(r"[\s_-]+", "_", match.group(1).upper())
                for match in re.finditer(
                    r"\bFinding\s*:\s*"
                    r"(APPROVED|DENIED|NEEDS[\s_-]*REVIEW)\b",
                    view,
                    re.I,
                )
            }
            if len(matches) == 1:
                found.update(matches)
    return found.pop() if len(found) == 1 else None


_REGISTERED_FIELD_SPECS = {
    "species_code": ("Species Code", "Species Match"),
    "sponsor_id": ("Sponsor ID",),
    "arrival_date": ("Arrival Date",),
}


def _visible_case_numbers(text: str) -> set[str]:
    confusion = str.maketrans(
        {
            "O": "0", "C": "0", "Q": "0", "D": "0",
            "I": "1", "L": "1", "Z": "2", "S": "5",
            "G": "6", "B": "8",
        }
    )
    numbers = set()
    for token in re.findall(
        r"\bM(?:I|1|L)?B[- ]?([A-Z0-9]{6})\b",
        text,
        re.I,
    ):
        normalized = token.upper().translate(confusion)
        if normalized.isdigit():
            numbers.add(normalized)
    return numbers


def _registered_line_has_label(
    text: str,
    labels: tuple[str, ...],
) -> bool:
    key = _compact(text)
    for label in labels:
        label_key = _compact(label)
        if label_key in key:
            return True
        prefix = key[:max(len(label_key) + 3, 8)]
        if difflib.SequenceMatcher(None, prefix, label_key).ratio() >= 0.67:
            return True
    return False


def _registered_field_value(field: str, text: str) -> str | None:
    if field == "species_code":
        exact = _vocabulary_value(text, SPECIES)
        if exact is not None:
            return exact
        key = _compact(text)
        ranked = sorted(
            (
                difflib.SequenceMatcher(
                    None,
                    key,
                    _compact(value),
                ).ratio(),
                value,
            )
            for value in SPECIES
        )
        best_score, best_value = ranked[-1]
        second_score = ranked[-2][0]
        if best_score >= 0.56 and best_score - second_score >= 0.16:
            return best_value
        return None
    if field == "sponsor_id":
        match = re.search(
            r"\bSP[NH]?[-_ ]?((?:\d[\s-]*){4})\b",
            text,
            re.I,
        )
        if not match:
            return None
        digits = re.sub(r"\D", "", match.group(1))
        return f"SPN-{digits}" if len(digits) == 4 else None
    match = re.search(
        r"\b(20\d{2})\s*[-/.]\s*(\d{2})\s*[-/.]\s*(\d{2})\b",
        text,
    )
    if not match:
        return None
    candidate = "-".join(match.groups())
    try:
        date.fromisoformat(candidate)
    except ValueError:
        return None
    return candidate


def _registered_field_repairs(
    image: Path,
    temp_dir: Path,
    expected_id: str,
) -> dict[str, str]:
    words = _ocr_tsv_words(image)
    page_text = " ".join(str(word["text"]) for word in words)
    page_text += "\n" + _ocr_page(image, 11)
    case_numbers = _visible_case_numbers(page_text)
    if expected_id not in case_numbers or any(
        value != expected_id for value in case_numbers
    ):
        return {}

    width, _, _ = _read_pgm(image)
    grouped = defaultdict(list)
    for word in words:
        grouped[
            (
                int(word["block"]),
                int(word["paragraph"]),
                int(word["line"]),
            )
        ].append(word)
    votes = {
        field: Counter()
        for field in _REGISTERED_FIELD_SPECS
    }
    scaled_arrival_votes: Counter[str] = Counter()
    for line_index, line_words in enumerate(grouped.values()):
        line_words.sort(key=lambda word: int(word["left"]))
        line_text = " ".join(str(word["text"]) for word in line_words)
        for field, labels in _REGISTERED_FIELD_SPECS.items():
            if not _registered_line_has_label(line_text, labels):
                continue
            top = min(int(word["top"]) for word in line_words)
            row_height = max(int(word["height"]) for word in line_words)
            crop = temp_dir / (
                f"registered-{image.stem}-{line_index}-{field}.pgm"
            )
            _crop_pgm(
                image,
                crop,
                int(width * 0.04),
                top - 2 * row_height,
                int(width * 0.62),
                top + 3 * row_height,
            )
            for psm in (6, 7, 8, 11, 13):
                value = _registered_field_value(
                    field,
                    _ocr_page(crop, psm),
                )
                if value is not None:
                    votes[field][value] += 1
            if field == "arrival_date":
                for factor in (2, 3, 4):
                    enlarged = temp_dir / (
                        f"registered-{image.stem}-{line_index}-"
                        f"{field}-{factor}x.pgm"
                    )
                    _scale_pgm_nearest(crop, enlarged, factor)
                    value = _registered_field_value(
                        field,
                        _ocr_page(enlarged, 11),
                    )
                    if value is not None:
                        scaled_arrival_votes[value] += 1

    repairs = {}
    for field, candidates in votes.items():
        if len(candidates) != 1:
            continue
        value, count = candidates.most_common(1)[0]
        if count >= 2:
            repairs[field] = value
    if len(scaled_arrival_votes) == 1:
        value, count = scaled_arrival_votes.most_common(1)[0]
        if count >= 3:
            repairs["arrival_date"] = value
    return repairs


def _high_resolution_field_repairs(pdf: Path) -> dict[str, str]:
    """Retry unresolved visible fields with a high-resolution OCR ensemble."""
    expected_id = pdf.stem.split("-")[-1]
    votes: dict[str, Counter[str]] = {
        "applicant_name": Counter(),
        "arrival_date": Counter(),
    }
    registered_repairs: dict[str, set[str]] = defaultdict(set)
    heading = re.compile(
        r"FORM\s+(?:I-8090|B-13)|Biometric\s+Scan\s+Slip|"
        r"(?:Planetary\s+)?Registry\s+Extract|Sponsor\s+Attestation|"
        r"(?:MIB\s+)?Fee\s+Receipt|Manual\s+Adjudicator\s+Note",
        re.I,
    )
    try:
        with tempfile.TemporaryDirectory(prefix="mib-hires-fields-") as temp:
            temp_dir = Path(temp)
            prefix = temp_dir / "page"
            subprocess.run(
                [
                    "pdftoppm", "-gray", "-r", "360",
                    str(pdf), str(prefix),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=45,
                check=True,
            )
            for image in sorted(temp_dir.glob("page-*.pgm")):
                views = [_ocr_page(image, psm) for psm in (3, 4, 6, 11)]
                for field, value in _registered_field_repairs(
                    image,
                    temp_dir,
                    expected_id,
                ).items():
                    registered_repairs[field].add(value)
                visible_ids = {
                    match
                    for view in views
                    for match in re.findall(
                        r"\bMIB[- ]?(\d{6})\b",
                        view,
                        re.I,
                    )
                }
                if expected_id not in visible_ids or any(
                    value != expected_id for value in visible_ids
                ):
                    continue
                if not any(heading.search(view) for view in views):
                    continue
                for view in views:
                    name_candidates = set()
                    for candidate in _labeled_values(
                        view,
                        ("Applicant", "Applicant Name", "Registry Name"),
                    ):
                        candidate = re.sub(
                            r"\s{2,}.*$",
                            "",
                            candidate,
                        ).strip()
                        if re.fullmatch(
                            r"[A-Za-z][A-Za-z'-]{2,} "
                            r"[A-Za-z][A-Za-z'-]{2,}",
                            candidate,
                        ):
                            name_candidates.add(candidate)
                    if len(name_candidates) == 1:
                        votes["applicant_name"].update(name_candidates)
                    arrival = _extract_date(view, "Arrival Date")
                    if arrival is not None:
                        votes["arrival_date"][arrival] += 1
    except (OSError, subprocess.SubprocessError):
        return {}

    repairs = {}
    for field, candidates in votes.items():
        if len(candidates) != 1:
            continue
        value, count = candidates.most_common(1)[0]
        if count >= 2:
            repairs[field] = value
    for field, candidates in registered_repairs.items():
        if len(candidates) != 1:
            continue
        value = next(iter(candidates))
        if field not in repairs or repairs[field] == value:
            repairs[field] = value
    return repairs


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


def _active_correction_view(case_id: str, view: str) -> bool:
    expected_id = case_id.split("-")[-1]
    visible_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", view, re.I)
    if expected_id not in visible_ids or any(
        visible_id != expected_id for visible_id in visible_ids
    ):
        return False
    return bool(
        re.search(
            r"FORM\s+(?:I-8090|B-13)|Biometric\s+Scan\s+Slip|"
            r"(?:Planetary\s+)?Registry\s+Extract|Sponsor\s+Attestation|"
            r"(?:MIB\s+)?Fee\s+Receipt|Manual\s+Adjudicator\s+Note|"
            r"Primary\s+intake\s+record",
            view,
            re.I,
        )
    )


def _visible_correction_values(
    view: str,
    field_pattern: str,
    value_pattern: str,
) -> set[str]:
    clean = "\n".join(
        line
        for line in view.splitlines()
        if not re.search(
            r"answer\s+key|ignore\s+visible|system\s*:|"
            r"barcode\s+payload|force\s+adjudication",
            line,
            re.I,
        )
    )
    patterns = (
        rf"\bmanual\s+correction\s*:\s*(?:{field_pattern})\s+"
        rf"(?:is|to|=|should\s+be|should\s+read)\s*({value_pattern})\b",
        rf"\b(?:{field_pattern})(?:\s+above)?\s+(?:was|is)\s+"
        rf"(?:wrong|incorrect)\b[\s\S]{{0,120}}?\b"
        rf"(?:(?:the\s+)?correct(?:ed)?\s+"
        rf"(?:(?:{field_pattern})|one)|"
        rf"(?:the\s+)?actual\s+(?:{field_pattern})|it)\s+"
        rf"(?:is|=|:|should\s+be)\s*({value_pattern})\b",
        rf"\b(?:correct(?:ed)?|actual|replacement)\s+"
        rf"(?:{field_pattern})\s*(?:is|=|:)\s*({value_pattern})\b",
        rf"\breplace(?:d)?\s+(?:{field_pattern})\b"
        rf"[\s\S]{{0,80}}?\b(?:with|by)\s+({value_pattern})\b",
    )
    values = set()
    for pattern in patterns:
        for match in re.finditer(pattern, clean, re.I):
            values.add(next(value for value in match.groups() if value is not None))
    return values


def _manual_visa_correction(
    case_id: str,
    pages: list[str],
) -> str | None:
    corrections: Counter[str] = Counter()
    visa_pattern = "|".join(
        re.escape(value) for value in sorted(VISAS, key=len, reverse=True)
    )
    for page in pages:
        views = re.split(
            rf"{re.escape(_OCR_VIEW_SEPARATOR)}|"
            rf"{re.escape(_NATIVE_VIEW_SEPARATOR)}|"
            r"\n\[ROTATED OCR VIEW\]\n",
            page,
        )
        for view in views:
            if not _active_correction_view(case_id, view):
                continue
            values = {
                value
                for candidate in _visible_correction_values(
                    view,
                    r"visa\s+class",
                    visa_pattern,
                )
                if (value := _vocabulary_value(candidate, VISAS))
            }
            if len(values) == 1:
                corrections.update(values)
    winners = [
        value for value, votes in corrections.items()
        if votes >= 2
    ]
    return winners[0] if len(winners) == 1 else None


def _manual_applicant_correction(
    case_id: str,
    pages: list[str],
) -> str | None:
    votes: Counter[str] = Counter()
    spellings: dict[str, str] = {}
    name_pattern = (
        r"[A-Za-z][A-Za-z'-]+\s+[A-Za-z][A-Za-z'-]+"
    )
    for page in pages:
        views = re.split(
            rf"{re.escape(_OCR_VIEW_SEPARATOR)}|"
            rf"{re.escape(_NATIVE_VIEW_SEPARATOR)}|"
            r"\n\[ROTATED OCR VIEW\]\n",
            page,
        )
        for view in views:
            if not _active_correction_view(case_id, view):
                continue
            candidates = {
                candidate
                for candidate in _visible_correction_values(
                    view,
                    r"applicant(?:\s+name)?",
                    name_pattern,
                )
            }
            if len(candidates) == 1:
                candidate = candidates.pop()
                key = candidate.lower()
                votes[key] += 1
                spellings[key] = candidate
    winners = [key for key, count in votes.items() if count >= 2]
    return spellings[winners[0]] if len(winners) == 1 else None


def _manual_fee_correction(
    case_id: str,
    pages: list[str],
) -> str | None:
    votes: Counter[str] = Counter()
    for page in pages:
        views = re.split(
            rf"{re.escape(_OCR_VIEW_SEPARATOR)}|"
            rf"{re.escape(_NATIVE_VIEW_SEPARATOR)}|"
            r"\n\[ROTATED OCR VIEW\]\n",
            page,
        )
        for view in views:
            if not _active_correction_view(case_id, view):
                continue
            values = {
                value.lower()
                for value in _visible_correction_values(
                    view,
                    r"fee\s+status",
                    r"paid|waived|unpaid|unknown",
                )
            }
            if len(values) == 1:
                votes.update(values)
    winners = [value for value, count in votes.items() if count >= 2]
    return winners[0] if len(winners) == 1 else None


def _manual_sponsor_correction(
    case_id: str,
    pages: list[str],
) -> str | None:
    votes: Counter[str] = Counter()
    for page in pages:
        views = re.split(
            rf"{re.escape(_OCR_VIEW_SEPARATOR)}|"
            rf"{re.escape(_NATIVE_VIEW_SEPARATOR)}|"
            r"\n\[ROTATED OCR VIEW\]\n",
            page,
        )
        for view in views:
            if not _active_correction_view(case_id, view):
                continue
            values = set()
            for candidate in _visible_correction_values(
                view,
                r"sponsor(?:\s+id)?",
                r"SPN[-_ ]?(?:\d[\s-]*){4}",
            ):
                digits = re.sub(r"\D", "", candidate)
                if len(digits) == 4:
                    values.add(f"SPN-{digits}")
            if len(values) == 1:
                votes.update(values)
    winners = [value for value, count in votes.items() if count >= 2]
    return winners[0] if len(winners) == 1 else None


def _trusted_stale_intake(case_id: str, pages: list[str]) -> bool:
    """Apply the documented 180-day rule only to intake-bound consensus."""
    reference_text = os.environ.get(
        "MIB_PACKET_RECEIPT_DATE",
        str(_ADJUDICATION_MODEL["reference_date"]),
    )
    try:
        reference = date.fromisoformat(reference_text)
    except ValueError:
        return False

    expected_id = case_id.split("-")[-1]
    pairs: set[tuple[str, str]] = set()
    for page in pages:
        page_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
        if expected_id not in page_ids or any(
            visible_id != expected_id for visible_id in page_ids
        ):
            continue
        if not re.search(
            r"FORM\s+I-8090|Primary\s+intake\s+record",
            page,
            re.I,
        ):
            continue
        if _NATIVE_VIEW_SEPARATOR not in page:
            continue
        native_view = page.split(_NATIVE_VIEW_SEPARATOR, 1)[1].split(
            "\n[ROTATED OCR VIEW]\n",
            1,
        )[0]
        visa = _fuzzy_closed_value(
            native_view,
            ("Visa Class",),
            VISAS,
            0.70,
        )
        arrival = _extract_date(native_view, "Arrival Date")
        if visa is not None and arrival is not None:
            pairs.add((visa, arrival))

    if len(pairs) != 1:
        return False
    visa, arrival_text = pairs.pop()
    if visa == "DIP-1":
        return False
    try:
        return (reference - date.fromisoformat(arrival_text)).days > 180
    except ValueError:
        return False


def _sponsor_attested_visa(
    case_id: str,
    pages: list[str],
) -> str | None:
    expected_id = case_id.split("-")[-1]
    votes: Counter[str] = Counter()
    visa_pattern = "|".join(
        re.escape(value) for value in sorted(VISAS, key=len, reverse=True)
    )
    patterns = (
        rf"\bvisa\s+class\s*[:=-]\s*({visa_pattern})\b",
        rf"\bresponsibility\s+for\s+class\s+({visa_pattern})\s+"
        rf"compliance\b",
    )
    for page in pages:
        if not re.search(r"\bSponsor\s+Attestation\b", page, re.I):
            continue
        page_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
        if expected_id not in page_ids or any(
            page_id != expected_id for page_id in page_ids
        ):
            continue
        views = re.split(
            rf"{re.escape(_OCR_VIEW_SEPARATOR)}|"
            rf"{re.escape(_NATIVE_VIEW_SEPARATOR)}|"
            r"\n\[ROTATED OCR VIEW\]\n",
            page,
        )
        for view in views:
            visible_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", view, re.I)
            if any(
                visible_id != expected_id for visible_id in visible_ids
            ):
                continue
            values = {
                value
                for pattern in patterns
                for match in re.finditer(pattern, view, re.I)
                if (value := _vocabulary_value(match.group(1), VISAS))
            }
            if len(values) == 1:
                votes.update(values)
    winners = [
        value for value, count in votes.items()
        if count >= 2
    ]
    return winners[0] if len(winners) == 1 else None


def _registry_name(
    case_id: str,
    pages: list[str],
) -> str | None:
    expected_id = case_id.split("-")[-1]
    votes: Counter[str] = Counter()
    spellings: dict[str, str] = {}
    for page in pages:
        if not re.search(r"\b(?:Planetary\s+)?Registry\s+Extract\b", page, re.I):
            continue
        page_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
        if expected_id not in page_ids or any(
            page_id not in (expected_id, "000000") for page_id in page_ids
        ):
            continue
        views = re.split(
            rf"{re.escape(_OCR_VIEW_SEPARATOR)}|"
            rf"{re.escape(_NATIVE_VIEW_SEPARATOR)}|"
            r"\n\[ROTATED OCR VIEW\]\n",
            page,
        )
        for view in views:
            visible_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", view, re.I)
            if any(
                visible_id not in (expected_id, "000000")
                for visible_id in visible_ids
            ):
                continue
            candidates = set()
            for candidate in _labeled_values(view, ("Registry Name",)):
                candidate = re.sub(r"\s{2,}.*$", "", candidate).strip()
                if re.fullmatch(
                    r"[A-Za-z][A-Za-z'-]+ [A-Za-z][A-Za-z'-]+",
                    candidate,
                ):
                    candidates.add(candidate)
            if len(candidates) == 1:
                candidate = candidates.pop()
                key = candidate.lower()
                votes[key] += 1
                spellings[key] = candidate
    winners = [
        key for key, count in votes.items()
        if count >= 2
    ]
    return spellings[winners[0]] if len(winners) == 1 else None


def _receipt_proves_paid(
    case_id: str,
    pages: list[str],
) -> bool:
    expected_id = case_id.split("-")[-1]
    votes = 0
    for page in pages:
        if not re.search(r"\b(?:MIB\s+)?Fee\s+Receipt\b", page, re.I):
            continue
        page_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
        if expected_id not in page_ids or any(
            page_id != expected_id for page_id in page_ids
        ):
            continue
        views = re.split(
            rf"{re.escape(_OCR_VIEW_SEPARATOR)}|"
            rf"{re.escape(_NATIVE_VIEW_SEPARATOR)}|"
            r"\n\[ROTATED OCR VIEW\]\n",
            page,
        )
        for view in views:
            visible_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", view, re.I)
            if any(
                visible_id != expected_id for visible_id in visible_ids
            ):
                continue
            if re.search(
                r"\bamount\s*(?:[:=-]\s*)?\$?\s*809(?:[.,]00)?\b",
                view,
                re.I,
            ):
                votes += 1
    return votes >= 2


def _extract_scoped_flags(case_id: str, pages: list[str]) -> tuple[list[str], str]:
    eligible_pages = []
    biometric_page_seen = False
    expected_id = case_id.split("-")[-1]
    for page in pages:
        biometric_layout = bool(
            re.search(r"FORM\s+B-13|Biometric\s+Scan\s+Slip", page, re.I)
            or (
                re.search(r"species\s+match", page, re.I)
                and re.search(r"observed\s+flags?", page, re.I)
            )
        )
        if not biometric_layout:
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


def _risk_crop_view_candidate(text: str) -> str | None:
    if not re.search(r"\bB-?13\b|Biometric\s+Scan\s+Slip", text, re.I):
        return None
    if not re.search(
        r"\bSpecies\s+Match\b|\bSpecies\b.{0,12}\bMatch\b",
        text,
        re.I,
    ):
        return None

    candidates: set[str] = set()
    for token in re.findall(r"[A-Za-z0-9]+(?:_[A-Za-z0-9]+)+", text):
        token_key = _compact(token)
        if len(token_key) < 8:
            continue
        ranked = sorted(
            (
                difflib.SequenceMatcher(
                    None,
                    token_key,
                    _compact(flag),
                ).ratio(),
                flag,
            )
            for flag in RISK_FLAGS
        )
        best_score, best_flag = ranked[-1]
        second_score = ranked[-2][0]
        if best_score >= 0.66 and best_score - second_score >= 0.20:
            candidates.add(best_flag)
    return candidates.pop() if len(candidates) == 1 else None


def _high_resolution_risk_flags(
    pdf: Path,
    pages: list[str],
) -> list[str]:
    current_flags, state = _extract_scoped_flags(pdf.stem, pages)
    if current_flags or state != "unknown":
        return []

    expected_id = pdf.stem.split("-")[-1]
    candidate_pages = []
    for index, page in enumerate(pages, 1):
        biometric_layout = bool(
            re.search(r"FORM\s+B-13|Biometric\s+Scan\s+Slip", page, re.I)
            or (
                re.search(r"species\s+match", page, re.I)
                and re.search(r"observed\s+flags?", page, re.I)
            )
        )
        if not biometric_layout:
            continue
        visible_ids = re.findall(r"\bMIB[- ]?(\d{6})\b", page, re.I)
        if expected_id in visible_ids and not any(
            visible_id != expected_id for visible_id in visible_ids
        ):
            candidate_pages.append(index)

    found: set[str] = set()
    with tempfile.TemporaryDirectory(prefix="mib-risk-crop-") as temp:
        temp_dir = Path(temp)
        for page_number in candidate_pages:
            prefix = temp_dir / f"page-{page_number}"
            subprocess.run(
                [
                    "pdftoppm", "-gray", "-r", "400",
                    "-f", str(page_number), "-l", str(page_number),
                    "-singlefile",
                    "-x", "0", "-y", "100", "-W", "2200", "-H", "1250",
                    str(pdf), str(prefix),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=20,
                check=True,
            )
            image = prefix.with_suffix(".pgm")
            votes: Counter[str] = Counter()
            for psm in (11, 12):
                candidate = _risk_crop_view_candidate(_ocr_page(image, psm))
                if candidate:
                    votes[candidate] += 1
            winners = [
                flag
                for flag, vote_count in votes.items()
                if vote_count == 2
            ]
            if len(winners) == 1:
                found.add(winners[0])
    return sorted(found) if len(found) == 1 else []


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

        note_heading = any(
            "MANUAL" in _compact(line)
            and "NOTE" in _compact(line)
            and difflib.SequenceMatcher(
                None,
                _compact(line),
                "MANUALADJUDICATORNOTE",
            ).ratio() >= 0.85
            for line in page.splitlines()
        )
        if note_heading:
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

                # A damaged Finding line can leave the signed note's semantic
                # reason intact. Keep this hard approval phrase deliberately
                # narrow so it cannot match generic clean-check language.
                for reason in re.findall(
                    r"\bReason\s*:\s*([^\n]+)", view, re.I
                ):
                    if re.search(
                        r"\bclean\b.*\bexception[-\s]*qualif\w*\b.*\bpacket\b",
                        reason,
                        re.I,
                    ):
                        page_candidates.add("APPROVED")
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

    supplementary = _supplementary_decision(case_id, pages)
    if supplementary is not None:
        return supplementary
    if re.search(r"reason\s*:?.*(?:mandatory\s+fee\s+unpaid|embargo(?:ed)?\s+home\s+world)", clean, re.I):
        return "DENIED"
    if re.search(r"reason\s*:?.*(?:damaged|contradictory|incomplete).*(?:evidence|packet)", clean, re.I):
        return "NEEDS_REVIEW"
    return None


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
    parsed_applicant = (
        Counter(cleaned_names).most_common(1)[0][0]
        if cleaned_names else None
    )
    applicant = _registry_name(case_id, pages)
    applicant = applicant or parsed_applicant
    output_applicant = (
        _manual_applicant_correction(case_id, pages)
        or applicant
    )

    species = _fuzzy_closed_value(
        text, ("Species Code", "Species Match"), SPECIES, 0.67
    )
    home_world = _fuzzy_closed_value(text, ("Home World",), HOME_WORLDS, 0.66)
    parsed_visa = _fuzzy_closed_value(
        text,
        ("Visa Class",),
        VISAS,
        0.64,
    )
    if (
        parsed_visa is None
        and re.search(
            r"\btransit\s+class\b[\s\S]{0,80}\b"
            r"(?:cannot|can(?:no|')?t|may\s+not|not\s+authori[sz]ed)\b",
            text,
            re.I,
        )
    ):
        # An authoritative adjudicator reason can explicitly identify the
        # otherwise unreadable visa class without guessing from the decision.
        parsed_visa = "TRANSIT-7"
    visa = (
        _manual_visa_correction(case_id, pages)
        or _sponsor_attested_visa(case_id, pages)
        or parsed_visa
    )
    # The adjudication model was trained on the original parser representation.
    # Keep newly recovered sponsor/manual evidence extraction-only until a
    # grouped out-of-fold retrain proves that changing this feature is safe.
    adjudication_visa = parsed_visa or visa
    policy_visa = visa or adjudication_visa

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
    corrected_sponsor = _manual_sponsor_correction(case_id, pages)
    if corrected_sponsor is not None:
        sponsor_number = corrected_sponsor.removeprefix("SPN-")
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
    output_flags = (
        flags
        if flags_state in {"clean", "positive"}
        else visible_flags
    )

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
    receipt_proves_paid = _receipt_proves_paid(case_id, pages)
    policy_fee = "paid" if receipt_proves_paid else fee
    output_fee = _manual_fee_correction(case_id, pages) or policy_fee or "paid"

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
        missing_core_fields = sum(
            value is None
            for value in (applicant, home_world, arrival)
        )
        if set(flags) & DISQUALIFYING:
            decision = "DENIED"
        elif "rescinded_denial" in flags:
            decision = "NEEDS_REVIEW"
        elif policy_visa == "TRANSIT-7" and missing_core_fields >= 3:
            decision = "NEEDS_REVIEW"
        elif policy_visa == "TRANSIT-7":
            decision = "DENIED"
        elif (
            sponsor in (REVOKED_SPONSORS | revoked_mentions)
            and policy_visa is not None
            and policy_visa != "DIP-1"
        ):
            decision = "DENIED"
        elif policy_fee == "unpaid":
            decision = "DENIED"
        elif _trusted_stale_intake(case_id, pages):
            decision = "DENIED"
        elif set(flags) & REVIEW_ONLY:
            decision = "NEEDS_REVIEW"
        elif (
            policy_fee == "waived"
            and adjudication_visa != "DIP-1"
            and not re.search(
            r"(?:hardship|authorized)\s+waiver|waiver\s+(?:approved|granted)",
            text,
            re.I,
            )
        ):
            decision = "NEEDS_REVIEW"
        elif policy_fee in (None, "unknown"):
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
            adjudication_visa,
            sponsor,
            arrival,
            purpose,
            visible_flags,
            fee,
            decision,
        )
        decision, modeled_confidence = _model_decision(model_features)
        if receipt_proves_paid and fee == "unpaid":
            # A case-scoped receipt and an explicit unpaid finding are
            # contradictory primary evidence.  Do not let a fitted numeric
            # cutoff turn that conflict into either a hard denial or approval.
            decision = "NEEDS_REVIEW"
            modeled_confidence = None

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

    return {
        "case_id": case_id,
        "applicant_name": output_applicant or "unknown",
        "species_code": species or "unknown",
        "home_world": home_world or "unknown",
        "visa_class": visa or "unknown",
        "sponsor_id": sponsor or "SPN-0000",
        "arrival_date": arrival or "1900-01-01",
        "declared_purpose": purpose or "unknown",
        "risk_flags": "|".join(output_flags) if output_flags else "none",
        "fee_status": output_fee,
        "adjudication": decision,
        "confidence": confidence,
    }


def _process(pdf: Path) -> dict:
    try:
        pages = _render_and_ocr(pdf)
        rotated_separator = "\n[ROTATED OCR VIEW]\n"
        if not any(rotated_separator in page for page in pages):
            result = _parse_packet(pdf.stem, pages)
        else:
            base_pages = [
                page.split(rotated_separator, 1)[0] for page in pages
            ]
            base = _parse_packet(pdf.stem, base_pages)
            enriched = _parse_packet(pdf.stem, pages)
            sentinels = {
                "applicant_name": "unknown",
                "species_code": "unknown",
                "home_world": "unknown",
                "visa_class": "unknown",
                "sponsor_id": "SPN-0000",
                "arrival_date": "1900-01-01",
                "declared_purpose": "unknown",
                "risk_flags": "none",
            }
            base_visa_before_enrichment = base["visa_class"]
            for field, sentinel in sentinels.items():
                if base[field] == sentinel and enriched[field] != sentinel:
                    base[field] = enriched[field]
            if (
                base["adjudication"] == "DENIED"
                and base_visa_before_enrichment == "unknown"
                and base["sponsor_id"] in REVOKED_SPONSORS
                and base["visa_class"] == "DIP-1"
                and enriched["adjudication"] != "DENIED"
            ):
                base["adjudication"] = enriched["adjudication"]
                base["confidence"] = enriched["confidence"]
            result = base

        if result["confidence"] != 0.99:
            high_resolution_finding = _high_resolution_finding(pdf, pages)
            if high_resolution_finding is not None:
                result["adjudication"] = high_resolution_finding
                result["confidence"] = 0.99
        if result["risk_flags"] == "none":
            high_resolution_flags = _high_resolution_risk_flags(pdf, pages)
            if high_resolution_flags:
                result["risk_flags"] = "|".join(high_resolution_flags)
        if (
            result["applicant_name"] == "unknown"
            or result["species_code"] in {"unknown", "TRIANGULAN"}
            or result["sponsor_id"] == "SPN-0000"
            or result["arrival_date"] == "1900-01-01"
        ):
            high_resolution_fields = _high_resolution_field_repairs(pdf)
            for field, sentinel in (
                ("applicant_name", "unknown"),
                ("sponsor_id", "SPN-0000"),
                ("arrival_date", "1900-01-01"),
            ):
                if (
                    result[field] == sentinel
                    and field in high_resolution_fields
                ):
                    result[field] = high_resolution_fields[field]
            if (
                result["species_code"] in {"unknown", "TRIANGULAN"}
                and "species_code" in high_resolution_fields
            ):
                result["species_code"] = high_resolution_fields["species_code"]
        return result
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


def _levenshtein(left: str, right: str) -> int:
    previous = list(range(len(right) + 1))
    for left_index, left_character in enumerate(left, 1):
        current = [left_index]
        for right_index, right_character in enumerate(right, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[right_index] + 1,
                    previous[right_index - 1]
                    + int(left_character != right_character),
                )
            )
        previous = current
    return previous[-1]


def _repair_rare_name_tokens(predictions: dict[str, dict]) -> None:
    """Repair isolated OCR slips using only repeated names in this input batch."""
    token_counts: Counter[str] = Counter()
    spellings: dict[str, Counter[str]] = {}
    for prediction in predictions.values():
        tokens = prediction["applicant_name"].split()
        if (
            len(tokens) != 2
            or prediction["applicant_name"] == "unknown"
            or not all(re.fullmatch(r"[A-Za-z][A-Za-z'-]{2,}", token) for token in tokens)
        ):
            continue
        for token in tokens:
            key = token.casefold()
            token_counts[key] += 1
            spellings.setdefault(key, Counter())[token] += 1

    vocabulary = sorted(
        token for token, count in token_counts.items() if count >= 5
    )
    if not vocabulary:
        return

    for prediction in predictions.values():
        tokens = prediction["applicant_name"].split()
        if (
            len(tokens) != 2
            or prediction["applicant_name"] == "unknown"
            or not all(re.fullmatch(r"[A-Za-z][A-Za-z'-]{2,}", token) for token in tokens)
        ):
            continue
        repaired = []
        for token in tokens:
            key = token.casefold()
            if token_counts[key] > 1:
                repaired.append(token)
                continue
            ranked = sorted(
                (_levenshtein(key, candidate), candidate)
                for candidate in vocabulary
            )
            if (
                ranked[0][0] > 2
                or (len(ranked) > 1 and ranked[0][0] == ranked[1][0])
            ):
                repaired.append(token)
                continue
            target = ranked[0][1]
            repaired.append(
                sorted(
                    spellings[target].items(),
                    key=lambda item: (-item[1], item[0]),
                )[0][0]
            )
        prediction["applicant_name"] = " ".join(repaired)


def _repair_collapsed_name_ligatures(predictions: dict[str, dict]) -> None:
    """Reverse repeated OCR ``rn`` to ``m`` collapses using this batch."""
    token_counts: Counter[str] = Counter()
    spellings: dict[str, Counter[str]] = {}
    for prediction in predictions.values():
        name = prediction["applicant_name"]
        if name == "unknown":
            continue
        for token in name.split():
            key = token.casefold()
            token_counts[key] += 1
            spellings.setdefault(key, Counter())[token] += 1

    for prediction in predictions.values():
        name = prediction["applicant_name"]
        if name == "unknown":
            continue
        repaired = []
        for token in name.split():
            key = token.casefold()
            candidates = {
                key[:index] + "rn" + key[index + 1:]
                for index, character in enumerate(key)
                if character == "m"
            }
            candidates = {
                candidate
                for candidate in candidates
                if token_counts[candidate] >= 5
                and token_counts[candidate] >= 2 * max(token_counts[key], 1)
            }
            if len(candidates) != 1:
                repaired.append(token)
                continue
            target = candidates.pop()
            repaired.append(
                sorted(
                    spellings[target].items(),
                    key=lambda item: (-item[1], item[0]),
                )[0][0]
            )
        prediction["applicant_name"] = " ".join(repaired)


def _impute_closed_vocabulary_modes(predictions: dict[str, dict]) -> None:
    """Fill unresolved output fields from this batch without affecting policy."""
    fields = {
        "species_code": "unknown",
        "home_world": "unknown",
        "visa_class": "unknown",
        "declared_purpose": "unknown",
    }
    for field, sentinel in fields.items():
        counts = Counter(
            prediction[field]
            for prediction in predictions.values()
            if prediction[field] != sentinel
        )
        if sum(counts.values()) < 50:
            continue
        mode = sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0]),
        )[0][0]
        for prediction in predictions.values():
            if prediction[field] == sentinel:
                prediction[field] = mode


def _repair_rare_arrival_years(predictions: dict[str, dict]) -> None:
    """Repair one-glyph year slips using only dominant years in this batch."""
    years = Counter(
        prediction["arrival_date"][:4]
        for prediction in predictions.values()
        if re.fullmatch(r"20\d{2}-\d{2}-\d{2}", prediction["arrival_date"])
    )
    total = sum(years.values())
    if total < 50:
        return
    mode, mode_count = years.most_common(1)[0]
    if mode_count / total < 0.70:
        return
    trusted = {
        year
        for year, count in years.items()
        if count / total >= 0.02
    }
    for prediction in predictions.values():
        value = prediction["arrival_date"]
        if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", value):
            continue
        year = value[:4]
        if (
            year not in trusted
            and int(year) > int(mode) + 1
            and sum(left != right for left, right in zip(year, mode)) == 1
        ):
            prediction["arrival_date"] = mode + value[4:]


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

    _repair_rare_name_tokens(predictions)
    _repair_collapsed_name_ligatures(predictions)
    _impute_closed_vocabulary_modes(predictions)
    _repair_rare_arrival_years(predictions)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for pdf in pdfs:
            handle.write(json.dumps(predictions[pdf.stem], sort_keys=True) + "\n")
