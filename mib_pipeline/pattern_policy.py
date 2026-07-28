"""Opt-in visible-evidence policy for the perfect-extraction experiment.

The ordinary pipeline stays unchanged unless ``MIB_EVIDENCE_PATTERN_POLICY=1``.
When enabled, this layer assumes the emitted fields are trustworthy and applies
the public policy to them.  It also retains one fact that a repaired field value
cannot represent: whether the active intake's arrival cell was actually blank
or explicitly unreadable.
"""

from __future__ import annotations

import difflib
import os
import re
from datetime import date


_PACKET_SNAPSHOT_DATE = date(2026, 7, 7)
_HARD_DENIAL_FLAGS = {
    "active_warrant",
    "biohazard_red",
    "memory_tampering",
    "planetary_embargo",
}
_REVIEW_ONLY_FLAGS = {
    "identity_conflict",
    "illegible_biometrics",
    "rescinded_denial",
    "sponsor_mismatch",
}
_REVOKED_SPONSORS = {
    "SPN-0007",
    "SPN-0139",
    "SPN-2718",
    "SPN-4040",
    "SPN-7331",
    "SPN-9090",
}
_VIEW_SEPARATOR = re.compile(
    r"\n\[(?:OCR VIEW 6|PIXEL-VERIFIED NATIVE TEXT|"
    r"ROTATED OCR VIEW|DESKEWED OCR VIEW)\]\n"
)
_ARRIVAL_LABEL = "ARRIVALDATE"
_INTAKE_HEADINGS = (
    "FORMI8090EXTRATERRESTRIALWORKAUTHORIZATIONINTAKE",
    "PRIMARYINTAKERECORD",
)
_UNRESOLVED = {
    "applicant_name": "unknown",
    "species_code": "unknown",
    "home_world": "unknown",
    "visa_class": "unknown",
    "sponsor_id": "SPN-0000",
    "arrival_date": "1900-01-01",
    "declared_purpose": "unknown",
    "fee_status": "unknown",
}


def _compact(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", value.upper())


def _case_numbers(text: str) -> set[str]:
    confusion = str.maketrans(
        {
            "O": "0",
            "C": "0",
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
    found = set()
    for token in re.findall(
        r"\bM(?:I|1|L)?B[- ]?([A-Z0-9]{6})\b",
        text,
        re.I,
    ):
        number = token.upper().translate(confusion)
        if number.isdigit():
            found.add(number)
    return found


def _is_intake_view(view: str) -> bool:
    lines = [_compact(line) for line in view.splitlines() if _compact(line)]
    return any(
        difflib.SequenceMatcher(None, line, target).ratio() >= 0.52
        for line in lines[:20]
        for target in _INTAKE_HEADINGS
    )


def _arrival_line_state(
    line: str,
    following_line: str = "",
) -> str | None:
    compact = _compact(line)
    prefix = compact[:max(len(_ARRIVAL_LABEL) + 4, 12)]
    if (
        _ARRIVAL_LABEL not in compact
        and difflib.SequenceMatcher(
            None,
            prefix,
            _ARRIVAL_LABEL,
        ).ratio() < 0.52
    ):
        return None
    if re.search(
        r"\bUNREADABLE\b",
        f"{line} {following_line}",
        re.I,
    ):
        return "explicit_unreadable"
    combined = f"{line} {following_line}"
    if re.search(r"\b20\d{2}\D+\d{2}\D+\d{2}\b", combined):
        return "observed_value"
    if sum(character.isdigit() for character in combined) >= 4:
        return "observed_value"
    words = [
        token
        for token in re.findall(r"[A-Za-z0-9]+", line)
        if len(token) > 1
    ]
    if any(
        len(token) >= 4 or (token.isdigit() and len(token) >= 2)
        for token in words[2:]
    ):
        return "observed_value"
    return "blank"


def intake_arrival_state(case_id: str, pages: list[str]) -> str:
    """Return the active I-8090 arrival cell's visible evidence state.

    A readable date wins over an OCR-only blank.  A pixel-verified native
    ``UNREADABLE`` marker wins over every OCR view because it is the literal
    content of the primary cell, not a failed transcription.  Pages carrying a
    foreign case id are ignored.
    """

    expected = case_id.removeprefix("MIB-")
    states: set[str] = set()
    for page in pages:
        page_ids = _case_numbers(page)
        if expected not in page_ids or any(
            number != expected for number in page_ids
        ):
            continue
        views = _VIEW_SEPARATOR.split(page)
        if not any(_is_intake_view(view) for view in views):
            continue
        for view in views:
            if not _is_intake_view(view):
                continue
            lines = [line.strip() for line in view.splitlines() if line.strip()]
            for index, line in enumerate(lines):
                following_line = (
                    lines[index + 1] if index + 1 < len(lines) else ""
                )
                state = _arrival_line_state(line, following_line)
                if state is not None:
                    states.add(state)
    if "explicit_unreadable" in states:
        return "explicit_unreadable"
    if "observed_value" in states:
        return "observed_value"
    if "blank" in states:
        return "blank"
    return "unknown"


def _field_policy(prediction: dict) -> tuple[str, str]:
    flags = {
        flag
        for flag in str(prediction["risk_flags"]).split("|")
        if flag and flag != "none"
    }
    visa = str(prediction["visa_class"])
    sponsor = str(prediction["sponsor_id"])
    fee = str(prediction["fee_status"])

    if flags & _HARD_DENIAL_FLAGS:
        return "DENIED", "hard_risk_flag"
    if visa == "TRANSIT-7":
        return "DENIED", "transit_only_visa"
    if sponsor in _REVOKED_SPONSORS and visa != "DIP-1":
        return "DENIED", "revoked_nondiplomatic_sponsor"
    if fee == "unpaid":
        return "DENIED", "mandatory_fee_unpaid"
    try:
        stale = (
            _PACKET_SNAPSHOT_DATE
            - date.fromisoformat(str(prediction["arrival_date"]))
        ).days > 180
    except ValueError:
        stale = False
    if stale and visa != "DIP-1":
        return "DENIED", "stale_nondiplomatic_arrival"

    arrival_state = str(
        prediction.get("_arrival_evidence_state", "unknown")
    )
    if arrival_state in {"explicit_unreadable", "blank", "destroyed"}:
        return "NEEDS_REVIEW", f"primary_arrival_{arrival_state}"
    if flags & _REVIEW_ONLY_FLAGS:
        return "NEEDS_REVIEW", "review_only_risk_flag"
    if any(
        prediction.get(field) == sentinel
        for field, sentinel in _UNRESOLVED.items()
    ):
        return "NEEDS_REVIEW", "unresolved_required_field"
    if sponsor == "SPN-0000" and visa != "DIP-1":
        return "NEEDS_REVIEW", "missing_required_sponsor"
    return "APPROVED", "complete_clean_visible_tuple"


def apply_evidence_pattern_policy(
    predictions: dict[str, dict],
) -> None:
    """Apply the opt-in field policy, then remove its internal evidence bit."""

    enabled = os.environ.get("MIB_EVIDENCE_PATTERN_POLICY") == "1"
    for prediction in predictions.values():
        if (
            enabled
            and prediction["adjudication"] == "NEEDS_REVIEW"
            and float(prediction["confidence"]) != 0.99
        ):
            decision, _ = _field_policy(prediction)
            prediction["adjudication"] = decision
            prediction["confidence"] = (
                0.78 if decision == "NEEDS_REVIEW" else 0.94
            )
        prediction.pop("_arrival_evidence_state", None)
