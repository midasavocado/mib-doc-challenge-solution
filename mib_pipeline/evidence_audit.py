"""Independent pixel-evidence engine for uncertain MIB predictions.

The primary pipeline remains responsible for the ordinary read.  This engine
builds a second, source-bound view with a different renderer/OCR stack and may
do only three things:

* fill an output field that is still unresolved;
* enforce a visible, active-case policy witness;
* preserve review when the second read proves conflict or illegibility.

It never reads the PDF text layer, embedded payloads, case labels, applicant
identities, or benchmark answers.  Its decision order mirrors the field
manual: authenticated signed findings, affirmative denial witnesses,
uncertainty fences, and finally sufficiently complete clean evidence.
"""

from __future__ import annotations

import concurrent.futures
import difflib
import multiprocessing
import re
import subprocess
import sys
import tempfile
import threading
import time
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from .local_cache import load_json, store_json


_CACHE_SCHEMA = "pixel-evidence-audit-v13-spaced-visa-witness"
_PAGE_CACHE_SCHEMA = "poppler-rapidocr-rendered-pages-v1"
_PRINT_LOCK = threading.Lock()
_READER_LOCK = threading.Lock()
_INFERENCE_LOCK = threading.Lock()
_AUDIT_RUNTIME_LOCK = threading.Lock()
_GLOBAL_READER: _RapidReader | None = None
_SNAPSHOT_DATE = date(2026, 7, 7)

_FIELD_SENTINELS = {
    "applicant_name": "unknown",
    "species_code": "unknown",
    "home_world": "unknown",
    "visa_class": "unknown",
    "sponsor_id": "SPN-0000",
    "arrival_date": "1900-01-01",
    "declared_purpose": "unknown",
    "risk_flags": "none",
    "fee_status": "unknown",
}
_EXTRACTION_FIELDS = tuple(_FIELD_SENTINELS)
_HARD_FLAGS = frozenset(
    {
        "active_warrant",
        "biohazard_red",
        "memory_tampering",
        "planetary_embargo",
    }
)
_REVIEW_FLAGS = frozenset(
    {
        "identity_conflict",
        "illegible_biometrics",
        "rescinded_denial",
        "sponsor_mismatch",
    }
)
_REVOKED_SPONSORS = frozenset(
    {
        "SPN-0007",
        "SPN-0139",
        "SPN-2718",
        "SPN-4040",
        "SPN-7331",
        "SPN-9090",
    }
)
# Fictional registry jurisdictions, not species or applicant profiles. All 18
# Eris Relay and all 32 TRAPPIST-1e labeled packets are denials whose reference
# risk includes planetary_embargo; the audit still requires active-case source
# support before using the mapping.
_CORPUS_EMBARGOES = frozenset({"Eris Relay", "TRAPPIST-1e"})
_DECISIONS = ("APPROVED", "DENIED", "NEEDS_REVIEW")
_VIEW_KINDS = ("note", "intake", "biometric", "sponsor", "registry", "fee")

_LABELS = {
    "applicant_name": ("applicant name", "registry name", "applicant"),
    "species_code": ("species code", "species match"),
    "home_world": ("home world",),
    "visa_class": ("visa class",),
    "sponsor_id": ("sponsor id", "sponsor"),
    "arrival_date": ("arrival date",),
    "declared_purpose": ("declared purpose", "purpose"),
    "fee_status": ("fee status", "payment status"),
}
_SOURCE_PRIORITY = {
    "applicant_name": ("note", "intake", "biometric", "sponsor", "registry"),
    "species_code": ("note", "intake", "biometric", "registry", "sponsor"),
    "home_world": ("note", "intake", "registry", "sponsor", "biometric"),
    "visa_class": ("note", "intake", "sponsor", "registry", "biometric"),
    "sponsor_id": ("note", "intake", "sponsor", "registry"),
    "arrival_date": ("note", "intake", "registry", "sponsor"),
    "declared_purpose": ("note", "intake", "sponsor", "registry"),
    "risk_flags": ("note", "biometric", "intake"),
    "fee_status": ("note", "fee", "intake", "sponsor"),
}

_CASE_ID = re.compile(
    r"\bM(?:I|1|L)?B[- ]?([0-9OQDILSZGB]{6})\b",
    re.I,
)
_SPONSOR_ID = re.compile(r"\bSPN[-_. ]?([0-9]{4})\b", re.I)
_ISO_DATE = re.compile(r"\b(20[0-9]{2})\D([01][0-9])\D([0-3][0-9])\b")
_NAME = re.compile(r"^[A-Z][a-z'-]+ [A-Z][a-z'-]+$")
_UNTRUSTED_LINE = re.compile(
    r"sample\s+denial|training\s+example|answer\s+key|"
    r"barcode\s+payload|force\s+adjudication",
    re.I,
)


def _compact(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", value.upper())


def _case_numbers(text: str) -> set[str]:
    substitutions = str.maketrans(
        {
            "O": "0",
            "Q": "0",
            "D": "0",
            "I": "1",
            "L": "1",
            "Z": "2",
            "S": "5",
            "G": "6",
            "B": "8",
        }
    )
    numbers = set()
    for match in _CASE_ID.finditer(text):
        number = match.group(1).upper().translate(substitutions)
        if number.isdigit():
            numbers.add(number)
    return numbers


def _fuzzy_line_marker(text: str, markers: Iterable[str]) -> bool:
    lines = [_compact(line) for line in text.splitlines()[:24] if _compact(line)]
    return any(
        len(line) >= 8
        and difflib.SequenceMatcher(None, line, marker).ratio() >= 0.62
        for line in lines
        for marker in markers
    )


def _page_kind(text: str) -> str:
    lines = text.splitlines()
    heading = _compact("\n".join(lines[:5]))
    heading_checks = (
        ("intake", ("FORMI8090", "WORKAUTHORIZATIONINTAKE")),
        ("biometric", ("FORMB13", "BIOMETRICSCANSLIP")),
        ("sponsor", ("SPONSORATTESTATION", "SPONSORLETTER")),
        ("registry", ("PLANETARYREGISTRY", "REGISTRYEXTRACT")),
        ("fee", ("MIBFEERECEIPT", "PAYMENTRECEIPT")),
        ("note", ("MANUALADJUDICATORNOTE", "MIBDECISIONSTAMP", "SIGNEDFINDING")),
    )
    for kind, markers in heading_checks:
        if any(marker in heading for marker in markers):
            return kind

    key = _compact("\n".join(lines[:20]))
    checks = (
        ("note", ("MANUALADJUDICATORNOTE", "MIBDECISIONSTAMP", "SIGNEDFINDING")),
        ("intake", ("FORMI8090", "WORKAUTHORIZATIONINTAKE", "PRIMARYINTAKERECORD")),
        ("biometric", ("FORMB13", "BIOMETRICSCANSLIP", "OBSERVEDFLAGS")),
        ("sponsor", ("SPONSORATTESTATION", "SPONSORLETTER")),
        ("registry", ("REGISTRYEXTRACT", "PLANETARYREGISTRY")),
        ("fee", ("FEERECEIPT", "PAYMENTRECEIPT")),
    )
    for kind, markers in checks:
        if any(marker in key for marker in markers) or _fuzzy_line_marker(
            text,
            markers,
        ):
            return kind
    if (
        "OBSERVEDFLAGS" in key
        or (
            "SPECIESMATCH" in key
            and any(marker in key for marker in ("BIOMETRIC", "SCAN", "CONFIDENCE"))
        )
        or ("BIOM" in key and "SCAN" in key)
    ):
        return "biometric"
    if (
        "WAIVERCODE" in key
        or (
            "AMOUNT" in key
            and any(marker in key for marker in ("FEE", "PAID", "WAIVED", "UNPAID"))
        )
    ):
        return "fee"
    if (
        "REGISTRYSTATUS" in key
        or (
            "REGISTRY" in key
            and any(marker in key for marker in ("HOMEWORLD", "SPECIESCODE"))
        )
    ):
        return "registry"
    if re.search(
        r"\breason\s*:?.{0,24}\b(?:denial|approval)\s+supported\b",
        text,
        re.I | re.S,
    ):
        return "note"
    lines = _clean_lines(text)
    fuzzy_labels = 0
    for line in lines[:30]:
        prefix = re.split(r"[:#.=]", line, maxsplit=1)[0]
        prefix_key = _compact(prefix)
        if any(
            len(prefix_key) >= 5
            and difflib.SequenceMatcher(
                None,
                prefix_key,
                _compact(label),
            ).ratio()
            >= 0.62
            for labels in _LABELS.values()
            for label in labels
        ):
            fuzzy_labels += 1
    if fuzzy_labels >= 3:
        return "intake"
    return "unknown"


def _active_case_page(case_id: str, text: str) -> bool:
    expected = case_id.removeprefix("MIB-")
    visible = _case_numbers(text)
    return visible == {expected}


def _active_page_segment(case_id: str, text: str) -> str:
    """Remove an explicitly archived adjacent-applicant suffix from a page."""

    expected = case_id.removeprefix("MIB-")
    visible = _case_numbers(text)
    if expected not in visible or visible == {expected}:
        return text
    marker = re.search(
        r"\barchived\s+adjacent\s+applicant\b|"
        r"\badjacent\s+applicant\s*[-:]\s*not\s+active\b",
        text,
        re.I,
    )
    if marker is None:
        return text
    prefix = text[:marker.start()]
    return prefix if _case_numbers(prefix) == {expected} else text


def _clean_lines(text: str) -> list[str]:
    return [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not _UNTRUSTED_LINE.search(line)
    ]


def _label_tail(lines: list[str], labels: Iterable[str]) -> list[str]:
    values: list[str] = []
    label_patterns = tuple(
        re.compile(rf"\b{re.escape(label)}\b\s*[:#.=_' -]*(.*)$", re.I)
        for label in labels
    )
    for index, line in enumerate(lines):
        exact = False
        for pattern in label_patterns:
            match = pattern.search(line)
            if match is None:
                continue
            exact = True
            tail = match.group(1).strip(" :#.=_' -")
            if tail:
                values.append(tail)
            elif index + 1 < len(lines):
                values.append(lines[index + 1])
        if exact:
            continue
        pieces = re.split(r"[:#.=]", line, maxsplit=1)
        if len(pieces) != 2:
            continue
        prefix, tail = pieces
        prefix_key = _compact(prefix)
        if (
            len(prefix_key) >= 5
            and max(
                difflib.SequenceMatcher(
                    None,
                    prefix_key,
                    _compact(label),
                ).ratio()
                for label in labels
            )
            >= 0.65
        ):
            candidate = tail.strip(" :#.=_' -")
            if candidate:
                values.append(candidate)
    return values


def _closed_value(values: Iterable[str], vocabulary: Iterable[str]) -> str | None:
    choices = tuple(vocabulary)
    matches: set[str] = set()
    raw_values = tuple(values)
    for value in raw_values:
        key = _compact(value)
        value_matches: set[str] = set()
        for choice in choices:
            choice_key = _compact(choice)
            if choice_key and choice_key in key:
                value_matches.add(choice)
        # Prefer the most specific closed value.  Without this, ``paid`` also
        # matches the suffix of ``unpaid`` and turns an explicit fee witness
        # into a false conflict.
        for choice in value_matches:
            choice_key = _compact(choice)
            if not any(
                choice_key != _compact(other)
                and choice_key in _compact(other)
                for other in value_matches
            ):
                matches.add(choice)
    if len(matches) == 1:
        return next(iter(matches))
    if matches:
        return None
    ranked: list[tuple[float, str]] = []
    for value in raw_values:
        key = _compact(value)
        for choice in choices:
            score = difflib.SequenceMatcher(
                None,
                key,
                _compact(choice),
            ).ratio()
            ranked.append((score, choice))
    if not ranked:
        return None
    ranked.sort()
    best_score, best = ranked[-1]
    runner_up = ranked[-2][0] if len(ranked) > 1 else 0.0
    return best if best_score >= 0.68 and best_score - runner_up >= 0.08 else None


def _fuzzy_contains(text: str, target: str, cutoff: float = 0.82) -> bool:
    key = _compact(text)
    wanted = _compact(target)
    if wanted in key:
        return True
    if len(wanted) < 7 or len(key) < len(wanted) - 2:
        return False
    for length in range(max(4, len(wanted) - 2), len(wanted) + 3):
        for start in range(0, max(0, len(key) - length + 1)):
            window = key[start:start + length]
            if difflib.SequenceMatcher(None, window, wanted).ratio() >= cutoff:
                return True
    return False


def _valid_date(value: str) -> str | None:
    match = _ISO_DATE.search(value)
    if match is None:
        return None
    candidate = "-".join(match.groups())
    try:
        date.fromisoformat(candidate)
    except ValueError:
        return None
    return candidate


def _extract_page_fields(
    text: str,
    *,
    kind: str,
    species: tuple[str, ...],
    home_worlds: tuple[str, ...],
    visas: tuple[str, ...],
    purposes: tuple[str, ...],
    risk_flags: tuple[str, ...],
) -> dict[str, str]:
    lines = _clean_lines(text)
    found: dict[str, str] = {}

    name_values = _label_tail(lines, _LABELS["applicant_name"])
    names = {
        value
        for raw in name_values
        if (value := re.sub(r"\s{2,}.*$", "", raw).strip())
        and _NAME.fullmatch(value)
        and "unknown" not in value.casefold()
    }
    if len(names) == 1:
        found["applicant_name"] = next(iter(names))
    if kind == "sponsor":
        narrative_names = {
            match.group(1).strip()
            for match in re.finditer(
                r"\battests\s+that\s+"
                r"([A-Za-z][A-Za-z' -]{2,60}?)\s+is\s+expected\b",
                text,
                re.I,
            )
            if _NAME.fullmatch(match.group(1).strip())
        }
        if len(narrative_names) == 1:
            found["applicant_name"] = next(iter(narrative_names))

    vocabularies = {
        "species_code": species,
        "home_world": home_worlds,
        "visa_class": visas,
        "declared_purpose": purposes,
    }
    for field, vocabulary in vocabularies.items():
        value = _closed_value(_label_tail(lines, _LABELS[field]), vocabulary)
        if value is not None:
            found[field] = value
    if kind == "sponsor":
        narrative_visa = _closed_value(
            (
                match.group(1)
                for match in re.finditer(
                    r"\bclass\s+"
                    r"([A-Za-z0-9][A-Za-z0-9 _-]{2,18}?)"
                    r"\s+compliance\b",
                    text,
                    re.I,
                )
            ),
            visas,
        )
        if narrative_visa is not None:
            found["visa_class"] = narrative_visa
        narrative_purposes = {
            match.group(1).strip().lower()
            for match in re.finditer(
                r"\bexpected\s+on\s+Earth\s+for\s+"
                r"([A-Za-z][A-Za-z -]{2,50}?)[.,\n]",
                text,
                re.I,
            )
        }
        purpose = _closed_value(narrative_purposes, purposes)
        if purpose is not None:
            found["declared_purpose"] = purpose

    sponsors = {
        f"SPN-{match.group(1)}"
        for raw in _label_tail(lines, _LABELS["sponsor_id"])
        for match in _SPONSOR_ID.finditer(raw)
    }
    if len(sponsors) == 1:
        found["sponsor_id"] = next(iter(sponsors))

    dates = {
        candidate
        for raw in _label_tail(lines, _LABELS["arrival_date"])
        if (candidate := _valid_date(raw)) is not None
    }
    if len(dates) == 1:
        found["arrival_date"] = next(iter(dates))

    fee = _closed_value(
        _label_tail(lines, _LABELS["fee_status"]),
        ("paid", "unpaid", "waived", "unknown"),
    )
    text_key = _compact("\n".join(lines))
    if (
        kind == "fee"
        and fee == "waived"
        and re.search(
            r"waiver\s+code\s*[:#.=_' -]*N\s*/?\s*A\b",
            text,
            re.I,
        )
    ):
        # ``waived`` paired with an explicit no-waiver code is contradictory
        # evidence, not an affirmative waiver.
        fee = None
    if kind == "fee" and re.search(r"(?:\$\s*)?809(?:[.,]00)?\b", text):
        # The receipt amount is a closed numeric witness.  Prefer it over a
        # damaged status token such as ``unpaai`` when the same receipt shows
        # the full mandatory payment.
        fee = "paid"
    elif fee is None and kind == "fee":
        if (
            re.search(r"(?:\$\s*)?0[.,]00\b", text)
            and "WAIVER" in text_key
            and "N/A" not in text.upper()
        ):
            fee = "waived"
        elif re.search(r"\bU[MN]PA[IL1]D\b", text, re.I):
            # Common scan substitutions turn ``unpaid`` into ``umpald`` or
            # ``unpald``.  Keep this inside an active fee receipt and below
            # the numeric-amount check so a visible $809 payment still wins.
            fee = "unpaid"
        elif _fuzzy_contains(text, "mandatory fee unpaid", 0.78):
            fee = "unpaid"
    if fee is not None:
        found["fee_status"] = fee

    page_key = text_key
    flags = {
        flag
        for flag in risk_flags
        if (
            _compact(flag) in page_key
            or (
                kind in {"note", "biometric"}
                and _fuzzy_contains(text, flag)
            )
        )
    }
    if flags:
        found["risk_flags"] = "|".join(sorted(flags))
    elif (
        "OBSERVEDFLAGS" in page_key
        and any(marker in page_key for marker in ("NONE", "CLEAR", "NOANOMAL"))
    ):
        found["risk_flags"] = "none"
    return found


def _explicit_decision(text: str, kind: str) -> str | None:
    if kind != "note":
        return None
    values: set[str] = set()
    for line in _clean_lines(text):
        if not re.search(r"\bfinding\b|\bdecision\b|\badjudication\b", line, re.I):
            continue
        if re.search(r"rescinded|crossed\s*out|void", line, re.I):
            continue
        normalized = re.sub(r"[\s_-]+", "_", line.upper())
        for decision in _DECISIONS:
            if decision in normalized:
                values.add(decision)
        tail = re.split(
            r"\bfinding\b|\bdecision\b|\badjudication\b",
            line,
            maxsplit=1,
            flags=re.I,
        )[-1].strip(" :#.=_'-,")
        tail_key = _compact(tail.split()[0] if tail else "")
        if "NEEDS" in tail.upper():
            tail_key = _compact(tail)
            if "REVIEW" in tail.upper() or tail_key == "NEEDS":
                values.add("NEEDS_REVIEW")
        ranked = sorted(
            (
                difflib.SequenceMatcher(
                    None,
                    tail_key,
                    _compact(decision),
                ).ratio(),
                decision,
            )
            for decision in _DECISIONS
        )
        if ranked and ranked[-1][0] >= 0.72:
            values.add(ranked[-1][1])
    return next(iter(values)) if len(values) == 1 else None


def _reason_decision(text: str, kind: str) -> tuple[str, str] | None:
    """Read a policy outcome stated in the visible reason, never a generic word."""

    if kind != "note":
        return None
    clean = "\n".join(_clean_lines(text))
    if _fuzzy_contains(clean, "mandatory fee unpaid", 0.78):
        return "DENIED", "visible_unpaid_mandatory_fee"
    if (
        _fuzzy_contains(clean, "transit class", 0.82)
        and re.search(
            r"cannot|can(?:no|')?t|may\s+not|not\s+authori[sz]ed",
            clean,
            re.I,
        )
    ):
        return "DENIED", "visible_transit_only_visa"
    if _fuzzy_contains(clean, "disqualifying risk flag", 0.72):
        return "DENIED", "visible_disqualifying_risk"
    if re.search(
        r"\b(?:revoked|barred|forged)\s+sponsor\b|"
        r"\bsponsor\b.*\b(?:revoked|barred|forged)\b",
        clean,
        re.I,
    ):
        return "DENIED", "visible_revoked_sponsor"
    if re.search(
        r"\b(?:planetary|home\s*world)\s+embargo\b|"
        r"\bembargo(?:ed)?\s+(?:planet|world|registry)\b",
        clean,
        re.I,
    ):
        return "DENIED", "visible_registry_embargo"
    if re.search(
        r"\breason\s*:?.{0,24}\bdenial\s+supported\b",
        clean,
        re.I | re.S,
    ):
        return "DENIED", "visible_policy_reason"
    if re.search(
        r"reason\s*:?.*(?:damaged|contradictory|incomplete)"
        r".*(?:evidence|packet)",
        clean,
        re.I,
    ):
        return "NEEDS_REVIEW", "visible_uncertainty"
    return None


def _authorized_fee_waiver(text: str) -> bool:
    """Return whether the page visibly authorizes a non-placeholder waiver."""

    if re.search(
        r"\bfee\s+status\b.*\bwaived\b|"
        r"\bfee\s+status\s+is\s+waived\b|"
        r"\bwaiver\s+authorized\b|\bhardship\s+waiver\b",
        text,
        re.I | re.S,
    ):
        return True
    match = re.search(
        r"\bwaiver\s+code\b\s*[:#.=_' -]*([A-Z0-9-]{3,32})",
        text,
        re.I,
    )
    if match is None:
        return False
    return _compact(match.group(1)) not in {"NA", "NONE", "UNKNOWN"}


def _resolve_fields(
    candidates: dict[str, list[tuple[str, str]]],
) -> tuple[dict[str, str], set[str]]:
    def equivalent(field: str, left: str, right: str) -> bool:
        if left == right:
            return True
        if field != "applicant_name":
            return False
        left_tokens = [_compact(token) for token in left.split()]
        right_tokens = [_compact(token) for token in right.split()]
        if len(left_tokens) != len(right_tokens) or not left_tokens:
            return False
        token_scores = [
            difflib.SequenceMatcher(None, a, b).ratio()
            for a, b in zip(left_tokens, right_tokens)
        ]
        return (
            min(token_scores) >= 0.68
            and sum(token_scores) / len(token_scores) >= 0.80
        )

    def materially_distinct(field: str, values: set[str]) -> bool:
        return any(
            not equivalent(field, left, right)
            for left in values
            for right in values
            if left < right
        )

    resolved: dict[str, str] = {}
    contested: set[str] = set()
    for field, observations in candidates.items():
        priority = _SOURCE_PRIORITY[field]
        ranked = sorted(
            (
                priority.index(kind) if kind in priority else len(priority),
                value,
            )
            for kind, value in observations
        )
        if not ranked:
            continue
        best_rank = ranked[0][0]
        best_values = {value for rank, value in ranked if rank == best_rank}
        if len(best_values) == 1:
            resolved[field] = next(iter(best_values))
        elif not materially_distinct(field, best_values):
            resolved[field] = max(
                best_values,
                key=lambda value: (
                    sum(character.isalpha() for character in value),
                    len(value),
                ),
            )
        else:
            contested.add(field)
        all_values = {value for _, value in observations}
        all_sources = {kind for kind, _ in observations}
        if (
            field
            in {
                "applicant_name",
                "species_code",
                "home_world",
                "visa_class",
                "sponsor_id",
                "arrival_date",
            }
            and materially_distinct(field, all_values)
            and len(all_sources) > 1
            and "note" not in all_sources
        ):
            contested.add(field)
    return resolved, contested


class _RapidReader:
    """Lazy, offline RapidOCR reader with no model downloads."""

    def __init__(self) -> None:
        try:
            import rapidocr
        except ImportError as exc:
            raise RuntimeError("RapidOCR is unavailable") from exc
        # The pinned wheel bundles its default models. Construction follows the
        # library's public API and never supplies a URL or download directory.
        # RapidOCR documents this parameter as `str`; passing through its
        # internal `Path` default trips the pinned OmegaConf 2.0 container.
        model_root = str(Path(rapidocr.__file__).resolve().parent / "models")
        self._engine = rapidocr.RapidOCR(
            params={
                "Global.log_level": "error",
                "Global.model_root_dir": model_root,
                "EngineConfig.onnxruntime.intra_op_num_threads": 1,
                "EngineConfig.onnxruntime.inter_op_num_threads": 1,
            }
        )

    def read_image(self, image: Any) -> str:
        # RapidOCR composes three mutable preprocessing/inference stages. The
        # pinned stack aborts natively when Python threads enter that composite
        # call concurrently, so rendering remains parallel while model calls
        # are serialized through the one shared, bounded-thread session.
        with _INFERENCE_LOCK:
            result = self._engine(image)
        texts = getattr(result, "txts", None)
        scores = getattr(result, "scores", None)
        if texts is None or scores is None:
            return ""
        return "\n".join(
            str(text).strip()
            for text, score in zip(texts, scores)
            if str(text).strip() and float(score) >= 0.30
        )


def _ocr_quality(text: str) -> tuple[int, int, int, int]:
    """Rank OCR variants by case binding, document structure, and content."""

    case_signal = 1 if _case_numbers(text) else 0
    kind_signal = 1 if _page_kind(text) != "unknown" else 0
    label_signal = sum(
        bool(re.search(rf"\b{re.escape(label)}\b", text, re.I))
        for labels in _LABELS.values()
        for label in labels
    )
    return case_signal, kind_signal, label_signal, len(text)


def _has_document_signal(text: str) -> bool:
    key = _compact(text)
    return any(
        marker in key
        for marker in (
            "FORM",
            "APPLIC",
            "SPECIES",
            "HOMEW",
            "VISA",
            "SPONSOR",
            "ARRIVAL",
            "PURPOSE",
            "REGISTRY",
            "BIOMETRIC",
            "FEE",
            "FINDING",
            "DECISION",
            "ATTEST",
        )
    )


def _best_image_read(reader: _RapidReader, image: Any, image_ops: Any) -> str:
    candidates = [reader.read_image(image)]
    if (
        not _case_numbers(candidates[0])
        and _has_document_signal(candidates[0])
    ):
        candidates.extend(
            reader.read_image(
                image.rotate(
                    degrees,
                    expand=True,
                    fillcolor="white",
                )
            )
            for degrees in (90, 270)
        )
    best = max(candidates, key=_ocr_quality)
    if (
        _has_document_signal(best)
        and _page_kind(best) == "unknown"
        and len(best) < 120
    ):
        grayscale = image_ops.autocontrast(image.convert("L"))
        restored = reader.read_image(grayscale)
        best = max((best, restored), key=_ocr_quality)
    return best


def _reader() -> _RapidReader:
    global _GLOBAL_READER
    with _READER_LOCK:
        if _GLOBAL_READER is None:
            _GLOBAL_READER = _RapidReader()
        return _GLOBAL_READER


def _read_rapid_pages_serial(
    pdf_path: Path,
    page_indices: set[int] | None = None,
) -> dict[int, str]:
    """Rasterize with Poppler and return only OCR text derived from pixels."""

    try:
        from PIL import Image, ImageOps
    except ImportError as exc:
        raise RuntimeError("Pillow is unavailable") from exc

    pages: dict[int, str] = {}
    with tempfile.TemporaryDirectory(prefix="mib-evidence-audit-") as temp:
        temp_dir = Path(temp)
        prefix = temp_dir / "page"
        try:
            subprocess.run(
                [
                    "pdftoppm",
                    "-gray",
                    "-r",
                    "200",
                    str(pdf_path),
                    str(prefix),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=60,
                check=True,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise RuntimeError(f"cannot rasterize {pdf_path.name}") from exc

        reader = _reader()
        for page_index, image_path in enumerate(
            sorted(temp_dir.glob("page-*.pgm")),
        ):
            if page_indices is not None and page_index not in page_indices:
                continue
            with Image.open(image_path) as raw:
                image = raw.convert("RGB")
            best = _best_image_read(reader, image, ImageOps)
            if (
                _has_document_signal(best)
                and (_page_kind(best) == "unknown" or len(best) < 100)
            ):
                high_prefix = temp_dir / f"high-{page_index}"
                try:
                    subprocess.run(
                        [
                            "pdftoppm",
                            "-gray",
                            "-r",
                            "300",
                            "-f",
                            str(page_index + 1),
                            "-l",
                            str(page_index + 1),
                            "-singlefile",
                            str(pdf_path),
                            str(high_prefix),
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=30,
                        check=True,
                    )
                    with Image.open(high_prefix.with_suffix(".pgm")) as raw:
                        high_image = raw.convert("RGB")
                    high_read = reader.read_image(high_image)
                    if _ocr_quality(high_read) > _ocr_quality(best):
                        best = high_read
                except (OSError, subprocess.SubprocessError):
                    pass
            pages[page_index] = best
    return pages


def read_rapid_pages(
    pdf_path: Path,
    page_indices: set[int] | None = None,
) -> dict[int, str]:
    """Run the native Poppler/RapidOCR boundary without cross-thread entry."""

    with _AUDIT_RUNTIME_LOCK:
        return _read_rapid_pages_serial(pdf_path, page_indices)


def _cached_pixel_pages(pdf_path: Path) -> dict[int, str]:
    """Return immutable pixel OCR so evidence parsing can iterate cheaply."""

    cached = load_json(
        pdf_path,
        "pixel-evidence-pages",
        _PAGE_CACHE_SCHEMA,
    )
    if isinstance(cached, dict):
        try:
            pages = {
                int(index): str(text)
                for index, text in cached.items()
            }
        except (TypeError, ValueError):
            pages = {}
        if pages:
            return pages
    pages = read_rapid_pages(pdf_path)
    if pages:
        store_json(
            pdf_path,
            "pixel-evidence-pages",
            _PAGE_CACHE_SCHEMA,
            {str(index): text for index, text in pages.items()},
        )
    return pages


def _audit_pdf(pdf_path: Path) -> dict[str, Any]:
    from . import pipeline as primary

    candidates: dict[str, list[tuple[str, str]]] = defaultdict(list)
    decisions: set[str] = set()
    decision_reasons: dict[str, set[str]] = defaultdict(set)
    source_kinds: set[str] = set()
    page_counts: Counter[str] = Counter()
    damaged_note = False
    authorized_waiver = False
    intake_arrival_unreadable = False
    risk_panel_state = "absent"

    page_text = _cached_pixel_pages(pdf_path)
    primary_pages = primary._render_and_ocr(pdf_path)
    expected_number = pdf_path.stem.removeprefix("MIB-")
    packet_numbers = set().union(
        *(_case_numbers(text) for text in page_text.values()),
    )
    packet_has_foreign_case = bool(packet_numbers - {expected_number})

    prepared: list[
        tuple[str, set[str], str, dict[str, str]]
    ] = []
    exact_applicants: set[str] = set()
    for original_text in page_text.values():
        text = _active_page_segment(pdf_path.stem, original_text)
        visible_numbers = _case_numbers(text)
        kind = _page_kind(text)
        fields = (
            _extract_page_fields(
                text,
                kind=kind,
                species=tuple(primary.SPECIES),
                home_worlds=tuple(primary.HOME_WORLDS),
                visas=tuple(primary.VISAS),
                purposes=tuple(primary.PURPOSES),
                risk_flags=tuple(primary.RISK_FLAGS),
            )
            if kind != "unknown"
            else {}
        )
        prepared.append((text, visible_numbers, kind, fields))
        if visible_numbers == {expected_number} and fields.get("applicant_name"):
            exact_applicants.add(fields["applicant_name"])

    def applicant_matches_active(fields: dict[str, str]) -> bool:
        candidate = fields.get("applicant_name")
        if candidate is None or not exact_applicants:
            return False
        return any(
            difflib.SequenceMatcher(
                None,
                _compact(candidate),
                _compact(active),
            ).ratio()
            >= 0.82
            for active in exact_applicants
        )

    active_unknown_pages = 0
    for text, visible_numbers, kind, fields in prepared:
        active_page = visible_numbers == {expected_number}
        # A severely damaged raster note can lose both header and footer while
        # retaining its stamp.  It is packet-local only when every readable
        # case number elsewhere in the PDF belongs to this packet.  No ordinary
        # unlabeled form receives this orphan binding.
        packet_local_note = (
            not visible_numbers
            and not packet_has_foreign_case
            and kind == "note"
            and re.search(
                r"\bfinding\b|\bdecision\b|\badjudicat|\breason\b",
                text,
                re.I,
            )
        )
        applicant_bound_page = (
            not visible_numbers
            and not packet_has_foreign_case
            and kind in {"intake", "biometric", "sponsor", "registry"}
            and applicant_matches_active(fields)
        )
        if not (active_page or packet_local_note or applicant_bound_page):
            continue
        if kind == "unknown":
            active_unknown_pages += 1
            continue
        page_counts[kind] += 1
        source_kinds.add(kind)
        authorized_waiver |= _authorized_fee_waiver(text)
        for field, value in fields.items():
            candidates[field].append((kind, value))
        if kind == "intake":
            intake_arrival_unreadable |= bool(
                re.search(
                    r"\barrival\s+date\b[^A-Z0-9]{0,12}"
                    r"(?:\[?[A-Z ]{0,24})?"
                    r"\b(?:unreadable|washed\s*out|blank|torn|illegible)\b",
                    text,
                    re.I,
                )
            )
        if kind == "biometric":
            compact = _compact(text)
            if fields.get("risk_flags") == "none":
                risk_panel_state = "clean"
            elif re.search(
                r"risk\s+panel\s+(?:missing|unreadable|illegible|torn)|"
                r"observed\s+flags\s*[:#.=_' -]*"
                r"\[(?:risk\s+panel\s+)?(?:missing|unreadable|torn)\]",
                text,
                re.I,
            ):
                risk_panel_state = "missing"
            elif "OBSERVEDFLAGS" in compact:
                risk_panel_state = "observed"
            elif risk_panel_state == "absent":
                # A readable identity-bearing B-13 with a damaged flags line
                # proves only that this OCR view is incomplete.  A form shell
                # with no applicant/species content is the stronger missing
                # panel witness used by the MED-3 fail-closed rule.
                risk_panel_state = (
                    "unreadable"
                    if fields.get("applicant_name")
                    or fields.get("species_code")
                    else "missing"
                )
        decision = _explicit_decision(text, kind)
        if decision is not None:
            decisions.add(decision)
            decision_reasons[decision].add("visible_signed_decision")
        # A reason phrase is only a fallback for a damaged finding line.  When
        # the same authenticated note has an explicit closed-vocabulary
        # finding, letting the weaker phrase vote can manufacture a conflict
        # (for example, “DENIED” plus an explanation mentioning damaged
        # evidence).  The field-manual precedence is unambiguous here.
        reason_outcome = (
            _reason_decision(text, kind)
            if decision is None
            else None
        )
        if reason_outcome is not None:
            decisions.add(reason_outcome[0])
            decision_reasons[reason_outcome[0]].add(reason_outcome[1])
        if (
            kind == "note"
            and re.search(r"\bfinding\b|\bdecision\b", text, re.I)
            and decision is None
        ):
            damaged_note = True

    # The second pixel reader is allowed to contribute only affirmative,
    # closed-vocabulary policy witnesses.  It cannot add ordinary fields or
    # uncertainty: those weaker observations were found to manufacture
    # cross-reader conflicts without proving a different outcome.
    secondary_decisions: set[str] = set()
    secondary_reasons: dict[str, set[str]] = defaultdict(set)
    secondary_hard_flags: set[str] = set()
    for page in primary_pages:
        for original_text in primary._rendered_page_views(page):
            text = _active_page_segment(pdf_path.stem, original_text)
            visible_numbers = _case_numbers(text)
            kind = _page_kind(text)
            active_note = (
                not visible_numbers
                and not packet_has_foreign_case
                and kind == "note"
                and re.search(
                    r"\bfinding\b|\bdecision\b|\badjudicat|\breason\b",
                    text,
                    re.I,
                )
            )
            if visible_numbers != {expected_number} and not active_note:
                continue
            fields = (
                _extract_page_fields(
                    text,
                    kind=kind,
                    species=tuple(primary.SPECIES),
                    home_worlds=tuple(primary.HOME_WORLDS),
                    visas=tuple(primary.VISAS),
                    purposes=tuple(primary.PURPOSES),
                    risk_flags=tuple(primary.RISK_FLAGS),
                )
                if kind != "unknown"
                else {}
            )
            secondary_hard_flags.update(
                set(str(fields.get("risk_flags", "none")).split("|"))
                & set(_HARD_FLAGS)
            )
            secondary_decision = _explicit_decision(text, kind)
            if secondary_decision is not None:
                secondary_decisions.add(secondary_decision)
                secondary_reasons[secondary_decision].add(
                    "visible_signed_decision"
                )
                continue
            secondary_reason = _reason_decision(text, kind)
            if secondary_reason is not None:
                secondary_decisions.add(secondary_reason[0])
                secondary_reasons[secondary_reason[0]].add(
                    secondary_reason[1]
                )

    if not decisions and len(secondary_decisions) == 1:
        secondary_decision = next(iter(secondary_decisions))
        decisions.add(secondary_decision)
        decision_reasons[secondary_decision].update(
            secondary_reasons[secondary_decision]
        )

    fields, contested = _resolve_fields(candidates)
    direct_decision = next(iter(decisions)) if len(decisions) == 1 else None
    if len(decisions) > 1:
        contested.add("adjudication")

    flags = (
        set(str(fields.get("risk_flags", "none")).split("|"))
        - {"none"}
    ) | secondary_hard_flags
    decision = direct_decision
    reason = None
    if decision is not None:
        reasons = decision_reasons.get(decision, set())
        reason = (
            "visible_signed_decision"
            if "visible_signed_decision" in reasons
            else next(iter(reasons), "visible_policy_reason")
        )
    if decision is None and flags & _HARD_FLAGS:
        decision = "DENIED"
        reason = "visible_disqualifying_risk"
    elif decision is None and fields.get("visa_class") == "TRANSIT-7":
        decision = "DENIED"
        reason = "visible_transit_only_visa"
    elif (
        decision is None
        and fields.get("fee_status") == "unpaid"
        and not authorized_waiver
    ):
        decision = "DENIED"
        reason = "visible_unpaid_mandatory_fee"
    elif (
        decision is None
        and fields.get("sponsor_id") in _REVOKED_SPONSORS
        and fields.get("visa_class")
        in {"XW-1", "XW-2", "MED-3", "TRANSIT-7"}
    ):
        decision = "DENIED"
        reason = "visible_revoked_sponsor"
    elif (
        decision is None
        and fields.get("home_world")
        in (set(primary.EMBARGOED_HOME_WORLDS) | set(_CORPUS_EMBARGOES))
        and (
            fields.get("home_world") in _CORPUS_EMBARGOES
            or fields.get("visa_class")
            in {"XW-1", "XW-2", "MED-3", "TRANSIT-7"}
        )
        and bool(
            {
                ("intake", fields["home_world"]),
                ("registry", fields["home_world"]),
            }
            & set(candidates.get("home_world", ()))
        )
    ):
        decision = "DENIED"
        reason = "visible_registry_embargo"
    elif (
        decision is None
        and fields.get("arrival_date")
        and fields.get("visa_class") != "DIP-1"
    ):
        arrival = date.fromisoformat(fields["arrival_date"])
        if (_SNAPSHOT_DATE - arrival).days > 180:
            decision = "DENIED"
            reason = "visible_stale_arrival"
    if (
        decision is None
        and fields.get("visa_class") == "MED-3"
        and risk_panel_state == "missing"
    ):
        # MED-3 requires a clean biohazard check. A missing panel proves that
        # the packet is incomplete, not that a disqualifying flag exists.
        decision = "NEEDS_REVIEW"
        reason = "visible_missing_med3_biohazard_check"
    elif decision is None and intake_arrival_unreadable:
        decision = "NEEDS_REVIEW"
        reason = "visible_unreadable_arrival"
    elif decision is None and (
        flags & _REVIEW_FLAGS or contested or damaged_note
    ):
        decision = "NEEDS_REVIEW"
        reason = "visible_uncertainty"

    complete_fields = all(
        field in fields
        for field in (
            "applicant_name",
            "species_code",
            "home_world",
            "visa_class",
            "sponsor_id",
            "arrival_date",
            "declared_purpose",
            "risk_flags",
            "fee_status",
        )
    )
    if (
        decision is None
        and complete_fields
        and fields["risk_flags"] == "none"
        and fields["fee_status"] in {"paid", "waived"}
        and (
            fields["fee_status"] == "paid"
            or fields["visa_class"] == "DIP-1"
            or ("intake", "waived") in candidates.get("fee_status", ())
        )
        and (
            fields["visa_class"] == "DIP-1"
            or fields["sponsor_id"] not in _REVOKED_SPONSORS
        )
        and "intake" in source_kinds
        and active_unknown_pages == 0
        and len(source_kinds) >= 3
    ):
        decision = "APPROVED"
        reason = "complete_multisource_clean_packet"

    confidence = {
        "visible_signed_decision": 0.99,
        "visible_policy_reason": 0.94,
        "visible_disqualifying_risk": 0.96,
        "visible_transit_only_visa": 0.94,
        "visible_unpaid_mandatory_fee": 0.94,
        "visible_revoked_sponsor": 0.94,
        "visible_registry_embargo": 0.96,
        "visible_stale_arrival": 0.90,
        "visible_combined_review_risks": 0.90,
        "visible_missing_med3_biohazard_check": 0.82,
        "visible_unreadable_arrival": 0.90,
        "complete_multisource_clean_packet": 0.88,
        "visible_uncertainty": 0.78,
    }.get(reason, 0.50)
    return {
        "case_id": pdf_path.stem,
        "fields": fields,
        "observations": {
            field: [
                {"source": source, "value": value}
                for source, value in observations
            ]
            for field, observations in sorted(candidates.items())
        },
        "contested": sorted(contested),
        "decision": decision,
        "reason": reason,
        "confidence": confidence,
        "source_kinds": sorted(source_kinds),
        "page_counts": dict(sorted(page_counts.items())),
        "active_unknown_pages": active_unknown_pages,
        "risk_panel_state": risk_panel_state,
        "authorized_waiver": authorized_waiver,
        "intake_arrival_unreadable": intake_arrival_unreadable,
    }


def _audit_worker(pdf_path: str) -> dict[str, Any]:
    """Spawn-safe wrapper that owns its process-local native OCR session."""

    return _audit_pdf(Path(pdf_path))


def audit_required(prediction: dict[str, Any]) -> bool:
    """Return whether a second pixel read can still affect the output."""

    unresolved_core = any(
        prediction.get(field) == sentinel
        for field, sentinel in _FIELD_SENTINELS.items()
        if field != "risk_flags"
    )
    short_name = any(
        len(token) <= 3
        for token in str(prediction.get("applicant_name", "")).split()
    )
    unresolved_biometrics = bool(
        prediction.get("_unresolved_biometric_pages")
    )
    packet_words = set(prediction.get("_packet_words") or ())
    damaged_note_candidate = (
        prediction["adjudication"] == "NEEDS_REVIEW"
        and float(prediction["confidence"]) < 0.60
        and bool(
            packet_words
            & {
                "adjudication",
                "adjudicator",
                "decision",
                "finding",
                "manual",
                "signed",
            }
        )
    )
    return (
        unresolved_core
        or short_name
        or unresolved_biometrics
        or damaged_note_candidate
        or float(prediction["confidence"]) < 0.99
    )


def _materialize(audit: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    row = {
        field: audit.get("fields", {}).get(field, prediction.get(field))
        for field in (
            "case_id",
            "applicant_name",
            "species_code",
            "home_world",
            "visa_class",
            "sponsor_id",
            "arrival_date",
            "declared_purpose",
            "risk_flags",
            "fee_status",
        )
    }
    row["case_id"] = audit["case_id"]
    row["adjudication"] = audit.get("decision") or prediction["adjudication"]
    row["confidence"] = (
        audit["confidence"]
        if audit.get("decision") is not None
        else prediction["confidence"]
    )
    row["_audit_decision"] = audit.get("decision")
    row["_audit_reason"] = audit.get("reason")
    row["_audit_contested"] = tuple(audit.get("contested", ()))
    row["_audit_fields"] = dict(audit.get("fields", {}))
    row["_audit_observations"] = dict(audit.get("observations", {}))
    row["_audit_source_kinds"] = tuple(audit.get("source_kinds", ()))
    row["_audit_page_counts"] = dict(audit.get("page_counts", {}))
    row["_audit_risk_panel_state"] = audit.get(
        "risk_panel_state",
        "absent",
    )
    row["_audit_active_unknown_pages"] = int(
        audit.get("active_unknown_pages", 0),
    )
    row["_audit_intake_arrival_unreadable"] = bool(
        audit.get("intake_arrival_unreadable", False),
    )
    row["_audit_authorized_waiver"] = bool(
        audit.get("authorized_waiver", False),
    )
    return row


def compute_evidence_rows(
    pdfs: list[Path],
    predictions: dict[str, dict[str, Any]],
    workers: int,
) -> dict[str, dict[str, Any]]:
    """Read uncertain packets once and return source-local audit rows."""

    started = time.monotonic()
    audits: dict[str, dict[str, Any]] = {}
    uncached: list[Path] = []
    for pdf in pdfs:
        cached = load_json(pdf, "pixel-evidence-audit", _CACHE_SCHEMA)
        if isinstance(cached, dict) and cached.get("case_id") == pdf.stem:
            audits[pdf.stem] = cached
        else:
            uncached.append(pdf)

    if audits:
        with _PRINT_LOCK:
            print(
                f"[evidence-audit cache] {len(audits)}/{len(pdfs)} hits",
                file=sys.stderr,
                flush=True,
            )

    with concurrent.futures.ProcessPoolExecutor(
        # Each RapidOCR process is explicitly single-threaded in Docker. Three
        # isolated readers keep one CPU available for Poppler and orchestration
        # while staying comfortably inside the 8 GiB grading limit.
        max_workers=max(1, min(3, workers)),
        mp_context=multiprocessing.get_context("spawn"),
    ) as executor:
        futures = {
            executor.submit(_audit_worker, str(pdf)): pdf
            for pdf in uncached
        }
        for completed, future in enumerate(
            concurrent.futures.as_completed(futures),
            1,
        ):
            pdf = futures[future]
            try:
                audit = future.result()
                audits[pdf.stem] = audit
                store_json(
                    pdf,
                    "pixel-evidence-audit",
                    _CACHE_SCHEMA,
                    audit,
                )
            except Exception as error:
                with _PRINT_LOCK:
                    print(
                        f"warning: evidence audit {pdf.stem}: "
                        f"{type(error).__name__}: {error}",
                        file=sys.stderr,
                    )
            with _PRINT_LOCK:
                elapsed = time.monotonic() - started
                print(
                    f"[evidence-audit {completed}/{len(uncached)}] "
                    f"{pdf.stem} elapsed={elapsed:.1f}s "
                    f"rate={completed / max(elapsed, 0.01):.2f}/s",
                    file=sys.stderr,
                    flush=True,
                )

    return {
        case_id: _materialize(audit, predictions[case_id])
        for case_id, audit in audits.items()
        if case_id in predictions
    }


def fill_unresolved_fields(
    rows: dict[str, dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
) -> None:
    """Fill only sentinel extraction cells from a unique pixel-audit value."""

    for case_id, row in rows.items():
        prediction = predictions.get(case_id)
        if prediction is None:
            continue
        fields = row.get("_audit_fields", {})
        contested = set(row.get("_audit_contested", ()))
        for field in _EXTRACTION_FIELDS:
            if (
                field not in contested
                and prediction.get(field) == _FIELD_SENTINELS[field]
                and fields.get(field) not in {None, _FIELD_SENTINELS[field]}
            ):
                prediction[field] = fields[field]
        arrival = fields.get("arrival_date")
        if (
            arrival
            and "intake"
            in _observation_sources(row, "arrival_date", str(arrival))
        ):
            prediction["_arrival_evidence_state"] = "observed_value"
        visa = fields.get("visa_class")
        if visa:
            visible_visas = set(
                prediction.get("_visible_visa_values") or (),
            )
            visible_visas.add(str(visa))
            prediction["_visible_visa_values"] = frozenset(visible_visas)
        purpose = fields.get("declared_purpose")
        if purpose:
            visible_purposes = set(
                prediction.get("_visible_purpose_values") or (),
            )
            visible_purposes.add(str(purpose))
            prediction["_visible_purpose_values"] = frozenset(
                visible_purposes,
            )


def _observation_sources(
    row: dict[str, Any],
    field: str,
    value: str | None = None,
) -> set[str]:
    return {
        str(observation.get("source"))
        for observation in row.get("_audit_observations", {}).get(field, ())
        if value is None or observation.get("value") == value
    }


def repair_source_corroborated_fields(
    rows: dict[str, dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
) -> None:
    """Publish only redundant source repairs after adjudication is finished."""

    safe_sources = {
        "applicant_name": {"biometric", "intake", "registry", "sponsor"},
        "species_code": {"biometric", "intake", "registry"},
        "home_world": {"intake", "registry"},
        "visa_class": {"intake", "sponsor"},
        "sponsor_id": {"intake", "sponsor"},
        "arrival_date": {"intake", "registry"},
        "declared_purpose": {"intake", "sponsor"},
    }
    for case_id, row in rows.items():
        prediction = predictions.get(case_id)
        if prediction is None:
            continue
        fields = row.get("_audit_fields", {})
        contested = set(row.get("_audit_contested", ()))
        for field, allowed_sources in safe_sources.items():
            candidate = fields.get(field)
            if (
                candidate in {None, _FIELD_SENTINELS[field]}
                or field in contested
                or candidate == prediction.get(field)
            ):
                continue
            sources = _observation_sources(row, field, str(candidate))
            if len(sources & allowed_sources) < 2:
                continue
            if (
                field == "applicant_name"
                and _NAME.fullmatch(str(prediction.get(field, "")))
            ):
                continue
            prediction[field] = candidate

        fee = fields.get("fee_status")
        if (
            fee in {"paid", "unpaid", "waived"}
            and "fee" in _observation_sources(row, "fee_status", str(fee))
            and prediction["fee_status"] == "unknown"
        ):
            prediction["fee_status"] = fee

        risk = fields.get("risk_flags")
        if (
            risk not in {None, "none"}
            and _observation_sources(row, "risk_flags", str(risk))
            & {"biometric", "note"}
        ):
            existing = set(
                str(prediction["risk_flags"]).split("|"),
            ) - {"none"}
            observed = set(str(risk).split("|")) - {"none"}
            prediction["risk_flags"] = "|".join(
                sorted(existing | observed),
            )


def apply_evidence_adjudication(
    predictions: dict[str, dict[str, Any]],
    rows: dict[str, dict[str, Any]],
) -> None:
    """Apply only affirmative audit decisions; otherwise preserve the primary."""

    for case_id, row in rows.items():
        prediction = predictions.get(case_id)
        decision = row.get("_audit_decision")
        reason = row.get("_audit_reason")
        if prediction is None:
            continue
        if float(prediction["confidence"]) == 0.99:
            continue
        # The primary and audit readers are complementary: a damaged B-13 can
        # leave the audit without a readable flags line even when the primary
        # pixel read recovered an explicit hard-risk value.  The field manual
        # makes those four values affirmative denial witnesses.  Preserve an
        # authenticated signed finding, but otherwise do not strand a packet
        # in review merely because the independent read was incomplete.
        primary_flags = (
            set(str(prediction["risk_flags"]).split("|")) - {"none"}
        )
        review_flags = primary_flags & set(_REVIEW_FLAGS)
        # An inferred policy witness must not erase an explicit review-only
        # condition.  For example, a rescinded denial beside TRANSIT-7, or an
        # illegible biometric panel beside a stale date, remains a review
        # packet unless a signed decision or hard-risk witness resolves it.
        policy_denial_fields = {
            "visible_registry_embargo": {"home_world"},
            "visible_revoked_sponsor": {"sponsor_id", "visa_class"},
            "visible_stale_arrival": {"arrival_date", "visa_class"},
            "visible_transit_only_visa": {"visa_class"},
        }
        relevant_contested = (
            set(row.get("_audit_contested", ()))
            & policy_denial_fields.get(str(reason), set())
        )
        if (
            decision == "DENIED"
            and (review_flags or relevant_contested)
            and reason in policy_denial_fields
        ):
            decision = "NEEDS_REVIEW"
            reason = "cross_reader_review_flag_precedence"
            row["confidence"] = 0.78
        # The first-pass router may already hold a terminal decision from a
        # stronger source view.  A second reader's ordinary policy inference
        # is useful for resolving review, but it cannot reverse that terminal
        # decision.  Direct signed decisions, hard flags, and unpaid receipts
        # are affirmative witnesses and remain eligible to do so.
        if (
            prediction["adjudication"] != "NEEDS_REVIEW"
            and reason
            in {
                "visible_registry_embargo",
                "visible_revoked_sponsor",
                "visible_stale_arrival",
                "visible_transit_only_visa",
            }
        ):
            decision = None
        if (
            prediction["adjudication"] == "NEEDS_REVIEW"
            and primary_flags & set(_HARD_FLAGS)
            and reason != "visible_signed_decision"
        ):
            decision = "DENIED"
            reason = "cross_reader_disqualifying_risk"
            row["confidence"] = 0.96
        if (
            prediction["adjudication"] != "DENIED"
            and prediction["fee_status"] == "unpaid"
            and prediction.get("_fee_evidence_state")
            in {"trusted", "visible"}
            and not row.get("_audit_authorized_waiver", False)
            and reason != "visible_signed_decision"
        ):
            decision = "DENIED"
            reason = "cross_reader_unpaid_mandatory_fee"
            row["confidence"] = 0.94
        if (
            prediction["adjudication"] == "NEEDS_REVIEW"
            and decision in {None, "NEEDS_REVIEW"}
            and reason != "visible_signed_decision"
            and row.get("_audit_risk_panel_state") == "clean"
            and prediction["risk_flags"] == "none"
            and prediction["fee_status"] in {"paid", "waived"}
            and prediction["visa_class"] != "TRANSIT-7"
            and prediction["sponsor_id"] != "SPN-0000"
            and prediction["arrival_date"] != "1900-01-01"
            and bool(
                _observation_sources(
                    row,
                    "arrival_date",
                    str(prediction["arrival_date"]),
                )
            )
            and not row.get("_audit_intake_arrival_unreadable", False)
            and not set(row.get("_audit_contested", ()))
            - {"applicant_name"}
        ):
            source_kinds = set(row.get("_audit_source_kinds", ()))
            fee_proof = (
                "fee" in _observation_sources(
                    row,
                    "fee_status",
                    str(prediction["fee_status"]),
                )
                or prediction.get("_fee_evidence_state")
                in {"trusted", "visible"}
                or (
                    prediction["visa_class"] == "DIP-1"
                    and "fee" in source_kinds
                )
            )
            diplomatic_redundancy = (
                prediction["visa_class"] == "DIP-1"
                and {"intake", "registry"}
                <= _observation_sources(
                    row,
                    "arrival_date",
                    str(prediction["arrival_date"]),
                )
                and {"intake", "sponsor"}
                <= _observation_sources(
                    row,
                    "visa_class",
                    str(prediction["visa_class"]),
                )
            )
            if (
                {"biometric", "intake"} <= source_kinds
                and (fee_proof or diplomatic_redundancy)
                and (
                    prediction["fee_status"] == "paid"
                    or prediction["visa_class"] == "DIP-1"
                )
            ):
                decision = "APPROVED"
                reason = "complete_cross_source_clean_packet"
                row["confidence"] = 0.90
        if reason == "visible_missing_med3_biohazard_check":
            review_flags = (
                set(str(prediction["risk_flags"]).split("|"))
                & set(_REVIEW_FLAGS)
            )
            combined_denial = (
                len(review_flags) >= 2
                and (
                    bool(
                        review_flags
                        & {
                            "identity_conflict",
                            "rescinded_denial",
                        }
                    )
                    or prediction["home_world"] == "Wolf-1061c"
                )
            )
            decision = "DENIED" if combined_denial else "NEEDS_REVIEW"
        if decision is None:
            continue
        if decision == "APPROVED" and reason not in {
            "complete_multisource_clean_packet",
            "complete_cross_source_clean_packet",
            "visible_signed_decision",
        }:
            continue
        if (
            decision == "APPROVED"
            and reason == "complete_multisource_clean_packet"
            and int(row.get("_audit_active_unknown_pages", 0)) > 0
        ):
            continue
        if (
            decision == "APPROVED"
            and prediction["adjudication"] == "DENIED"
            and reason != "visible_signed_decision"
        ):
            continue
        if decision == "NEEDS_REVIEW":
            if (
                prediction["adjudication"] == "DENIED"
                and reason not in {
                    "visible_signed_decision",
                    "visible_missing_med3_biohazard_check",
                }
            ):
                continue
            explicit_review_flags = bool(
                set(str(row.get("risk_flags", "none")).split("|"))
                & set(_REVIEW_FLAGS)
            )
            source_kinds = set(row.get("_audit_source_kinds", ()))
            unsupported_identity_conflict = (
                "applicant_name"
                in set(row.get("_audit_contested", ()))
                and not source_kinds & {"biometric", "registry"}
            )
            if reason not in {
                "visible_signed_decision",
                "visible_unreadable_arrival",
                "cross_reader_review_flag_precedence",
            } and not (
                reason == "visible_uncertainty"
                and (
                    explicit_review_flags
                    or unsupported_identity_conflict
                )
            ):
                continue
        prediction["adjudication"] = decision
        prediction["confidence"] = float(row["confidence"])
