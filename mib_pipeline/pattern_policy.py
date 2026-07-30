"""Visible evidence-state helpers shared by terminal policy stages."""

from __future__ import annotations

import difflib
import re
_VIEW_SEPARATOR = re.compile(
    r"\n\[(?:OCR VIEW 6|PIXEL-VERIFIED NATIVE TEXT|"
    r"ROTATED OCR VIEW|DESKEWED OCR VIEW)\]\n"
)
_ARRIVAL_LABEL = "ARRIVALDATE"
_INTAKE_HEADINGS = (
    "FORMI8090EXTRATERRESTRIALWORKAUTHORIZATIONINTAKE",
    "PRIMARYINTAKERECORD",
)
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
