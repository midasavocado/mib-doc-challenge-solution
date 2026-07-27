"""Visible OCR repairs for fee / purpose / deny-findings when native text is empty.

Runs a cheap pdftoppm + Tesseract pass only when needed. Fail-closed on
approvals: may set DENIED from an explicit Finding, and may fix fee/purpose
fields, but never invents APPROVED.
"""

from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

from .arjun_heads import _pdf_layout_text, _strip_answer_key_lines
from .models import PredictionRow

_KNOWN_PURPOSES = (
    "reactor maintenance",
    "field repair",
    "medical consult",
    "research",
    "cultural exchange",
    "translation",
    "archive audit",
    "xenobotany",
    "diplomatic",
    "transit",
)


def _layout_text(pdf_path: Path) -> str:
    """Cheap selectable-text path before raster OCR."""

    try:
        return _strip_answer_key_lines(_pdf_layout_text(pdf_path) or "")
    except Exception:  # pragma: no cover
        return ""


def _ocr_packet(pdf_path: Path, dpi: int = 160) -> str:
    with tempfile.TemporaryDirectory(prefix="mib-vis-") as tmp:
        work = Path(tmp)
        prefix = work / "page"
        try:
            subprocess.run(
                [
                    "pdftoppm",
                    "-jpeg",
                    "-jpegopt",
                    "quality=85",
                    "-r",
                    str(dpi),
                    str(pdf_path),
                    str(prefix),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=50,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return ""
        chunks: list[str] = []
        for image in sorted(work.glob("page-*.jpg")):
            # psm 6 at 160dpi recovers Finding:DENIED; 4/11 add little on train.
            try:
                cp = subprocess.run(
                    ["tesseract", image.name, "stdout", "--psm", "6"],
                    cwd=work,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    errors="replace",
                    timeout=25,
                    check=False,
                )
                chunks.append(cp.stdout if cp.returncode == 0 else "")
            except (OSError, subprocess.TimeoutExpired):
                chunks.append("")
        return "\n".join(chunks)


def _fee_from_ocr(text: str) -> str | None:
    if re.search(r"Fee\s*Status\s*[: ]\s*waived", text, re.I):
        return "waived"
    if re.search(r"Amount\s*\$?\s*0(?:[.,]00)?", text, re.I) and re.search(
        r"(?:DIP[\s\-]?WAIVER|Waiver\s*Code\s*[:#]?\s*DIP|Waiver\s*Code\s*[:#]?\s*\w*WAIV)",
        text,
        re.I,
    ):
        return "waived"
    if re.search(r"Fee\s*Status\s*[: ]\s*unpaid", text, re.I):
        return "unpaid"
    if re.search(r"Fee\s*Status\s*[: ]\s*paid", text, re.I):
        return "paid"
    if re.search(r"Amount\s*\$?\s*809(?:[.,]00)?", text, re.I):
        return "paid"
    if re.search(r"Fee\s*Status\s*[: ]\s*unknown", text, re.I):
        return "unknown"
    return None


def _purpose_from_ocr(text: str) -> str | None:
    # Sponsor attestation sentence.
    for match in re.finditer(
        r"attests that [A-Z][a-z]+(?:\s+[A-Z][a-z]+)+ is expected on Earth for ([a-z \n]+?)(?:\.|,|\n)",
        text,
        re.I,
    ):
        blob = " ".join(match.group(1).casefold().split())
        for purpose in _KNOWN_PURPOSES:
            if blob == purpose or blob.startswith(purpose):
                return purpose
    for purpose in _KNOWN_PURPOSES:
        if purpose == "reactor maintenance":
            continue
        if re.search(
            rf"(?:declared\s+purpose\s*[:#.=_-]\s*{re.escape(purpose)}"
            rf"|purpose\s+of\s+visit\s*[:#.=_-]\s*{re.escape(purpose)})",
            text,
            re.I,
        ):
            return purpose
    return None


def _finding_denied(text: str) -> bool:
    # Accept common OCR damage: DENIED / DENED / DEN'ED.
    if re.search(r"Finding\s*[: ]\s*DEN[\'`]?I?ED\b", text, re.I):
        return True
    # Avoid SAMPLE DENIAL watermarks.
    cleaned = re.sub(r"\bSAMPLE[- ]+DENIAL\b", "", text, flags=re.I)
    return bool(
        re.search(r"\bFinding\b.{0,20}\bDEN[\'`]?I?ED\b", cleaned, re.I | re.S)
    )


def _finding_needs_review(text: str) -> bool:
    cleaned = re.sub(r"\bSAMPLE[- ]+DENIAL\b", "", text, flags=re.I)
    return bool(re.search(r"Finding\s*[: ]\s*NEEDS[_\s]?REVIEW\b", cleaned, re.I))


def _risk_tokens(text: str) -> str | None:
    flags: list[str] = []
    lowered = text.lower().replace(" ", "_")
    for flag in (
        "biohazard_red",
        "memory_tampering",
        "active_warrant",
        "planetary_embargo",
        "illegible_biometrics",
        "identity_conflict",
        "sponsor_mismatch",
        "rescinded_denial",
    ):
        if flag in lowered:
            flags.append(flag)
    if re.search(r"Registry\s+Status\s*[: ]\s*EMBARGO", text, re.I):
        flags.append("planetary_embargo")
    if not flags:
        return None
    return "|".join(sorted(set(flags)))


def _norm_risk(value: str | None) -> str:
    raw = " ".join(str(value or "").strip().split()).casefold()
    if raw in {"", "none", "null", "unknown"}:
        return "none"
    return raw


def _apply_repairs_from_text(
    row: PredictionRow,
    text: str,
    *,
    needs_fee: bool,
    needs_purpose: bool,
    needs_deny: bool,
    needs_review_finding: bool,
) -> PredictionRow:
    if not text.strip():
        return row

    payload = row.to_dict()
    changed = False

    # Fee OCR from raster text is net-negative on public train (hallucinated
    # waived/paid). Keep Amount/$809 repairs in layout heads instead.
    _ = needs_fee

    if needs_purpose:
        purpose = _purpose_from_ocr(text)
        if purpose and purpose != payload.get("declared_purpose"):
            payload["declared_purpose"] = purpose
            changed = True

    # Do not invent risk tokens from OCR noise (EMBARGO false positives).
    # Finding stamps below remain the high-precision deny/review channel.

    if needs_deny and _finding_denied(text):
        payload["adjudication"] = "DENIED"
        payload["confidence"] = 0.98
        changed = True
    elif needs_review_finding and _finding_needs_review(text):
        # Exact Finding:NEEDS_REVIEW only — demote DENIED → REVIEW, never approve.
        payload["adjudication"] = "NEEDS_REVIEW"
        payload["confidence"] = max(float(payload.get("confidence") or 0), 0.85)
        changed = True

    if not changed:
        return row
    return PredictionRow.from_mapping(payload, fallback_case_id=row.case_id)


def apply_visible_ocr_repairs(
    row: PredictionRow,
    pdf_path: Path,
    *,
    force: bool = False,
) -> PredictionRow:
    """OCR fallback for fee/purpose/deny findings when native path is weak."""

    # Finding stamps only — fee/risk/purpose raster fills measured net-negative
    # or low-EV on public train. Layout heads still repair Amount/$809 / purpose.
    needs_fee = False
    needs_purpose = False
    needs_deny = (
        row.adjudication == "NEEDS_REVIEW" and _norm_risk(row.risk_flags) == "none"
    ) or force
    # Only probe Finding:NEEDS_REVIEW when the deny is risk-empty (image stamp /
    # finding path). Skip DENIED rows that already carry disqualifying flags.
    needs_review_finding = (
        row.adjudication == "DENIED" and _norm_risk(row.risk_flags) == "none"
    ) or force
    if not (needs_deny or needs_review_finding):
        return row

    # Prefer selectable layout text; rasterize only when needs remain.
    layout = _layout_text(pdf_path)
    repaired = _apply_repairs_from_text(
        row,
        layout,
        needs_fee=False,
        needs_purpose=False,
        needs_deny=needs_deny,
        needs_review_finding=needs_review_finding,
    )
    needs_deny = (
        repaired.adjudication == "NEEDS_REVIEW"
        and _norm_risk(repaired.risk_flags) == "none"
    ) or force
    needs_review_finding = (
        repaired.adjudication == "DENIED"
        and _norm_risk(repaired.risk_flags) == "none"
    ) or force
    if not (needs_deny or needs_review_finding):
        return repaired

    text = _ocr_packet(pdf_path)
    return _apply_repairs_from_text(
        repaired,
        text,
        needs_fee=False,
        needs_purpose=False,
        needs_deny=needs_deny,
        needs_review_finding=needs_review_finding,
    )
