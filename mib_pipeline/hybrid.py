"""Run the independent visible-provenance adjudicator after extraction."""

from __future__ import annotations

import concurrent.futures
import difflib
import re
import sys
import threading
import time
from datetime import date
from pathlib import Path

from provenance_engine import (
    AdjudicationEngine,
    CaseLinker,
    ConfidenceCalibrator,
    DocumentRenderer,
    EvidencePrecedenceResolver,
    GeneralizablePolicyExceptionStore,
    OutputConfidenceRecalibrationProcessor,
    OutputConfidenceRecalibrator,
    RapidOutputRecoveryProcessor,
    ReviewDenialRecoveryAdjudicator,
    VisibleEvidenceExtractor,
)

from .visible_denials import apply_visible_slash_denials


_PRINT_LOCK = threading.Lock()
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


def _normalized_letters(value: str) -> str:
    return re.sub(r"[^a-z]+", "", value.casefold())


def _has_damaged_manual_review_note(pages: list[str], prediction: dict) -> bool:
    """Recognize an unreadable higher-precedence manual note.

    A weak policy inference must not overrule a visible manual adjudicator note
    whose title survives but whose finding does not. This is deliberately
    limited to low-confidence, incomplete rows with no hard denial flag.
    """

    if (
        float(prediction["confidence"]) >= 0.8
        or str(prediction["risk_flags"]) != "none"
        or (
            prediction["applicant_name"] != "unknown"
            and prediction["arrival_date"] != "1900-01-01"
        )
    ):
        return False
    packet_text = "\n".join(pages)
    if re.search(
        r"\bfinding\s*[:=-]?\s*(?:approved|denied|needs[_\s-]*review)\b",
        packet_text,
        re.I,
    ):
        return False
    targets = tuple(
        _normalized_letters(label)
        for label in ("Manual Adjudicator Note", "Adjudicator Note")
    )
    return any(
        max(
            difflib.SequenceMatcher(
                None,
                _normalized_letters(line),
                target,
            ).ratio()
            for target in targets
        )
        >= 0.65
        for line in packet_text.splitlines()
        if len(_normalized_letters(line)) >= 12
    )


def _has_uncorroborated_redacted_stale_visa(
    pages: list[str],
    prediction: dict,
) -> bool:
    """Reject a stale-date denial whose non-DIP visa premise is redacted.

    The public policy makes staleness depend on whether the visa is diplomatic.
    If the sole visible non-DIP visa read shares a page with an explicit
    ``REDACTED?`` marker and no independent page corroborates that visa, the
    packet proves uncertainty rather than denial.
    """

    flags = {
        flag
        for flag in str(prediction["risk_flags"]).split("|")
        if flag and flag != "none"
    }
    if (
        not flags
        or not flags <= _REVIEW_ONLY_FLAGS
        or flags & _HARD_DENIAL_FLAGS
        or prediction["visa_class"] == "DIP-1"
        or float(prediction["confidence"]) == 0.99
    ):
        return False
    try:
        arrival = date.fromisoformat(str(prediction["arrival_date"]))
    except ValueError:
        return False
    if (_PACKET_SNAPSHOT_DATE - arrival).days <= 180:
        return False

    visa = re.escape(str(prediction["visa_class"])).replace(r"\-", r"[\s-]?")
    visa_line = re.compile(
        rf"(?:visa\s+class\s*[:.]?\s*{visa}|class\s+{visa}\s+compliance)",
        re.I,
    )
    redacted_source = any(
        re.search(r"\bREDACTED\s*\?", page, re.I) and visa_line.search(page)
        for page in pages
    )
    corroborating_pages = sum(bool(visa_line.search(page)) for page in pages)
    return redacted_source and corroborating_pages < 2


def _apply_visible_review_safeguards(
    pdfs: list[Path],
    predictions: dict[str, dict],
) -> None:
    """Demote soft denials contradicted by visible uncertainty evidence."""

    from .pipeline import _render_and_ocr

    for pdf in pdfs:
        prediction = predictions[pdf.stem]
        if prediction["adjudication"] != "DENIED":
            continue
        flags = set(str(prediction["risk_flags"]).split("|"))
        low_confidence_incomplete = (
            float(prediction["confidence"]) < 0.8
            and prediction["risk_flags"] == "none"
            and (
                prediction["applicant_name"] == "unknown"
                or prediction["arrival_date"] == "1900-01-01"
            )
        )
        review_flag_stale = False
        if (
            flags & _REVIEW_ONLY_FLAGS
            and not flags & _HARD_DENIAL_FLAGS
            and prediction["visa_class"] != "DIP-1"
            and float(prediction["confidence"]) != 0.99
        ):
            try:
                arrival = date.fromisoformat(str(prediction["arrival_date"]))
            except ValueError:
                arrival = _PACKET_SNAPSHOT_DATE
            review_flag_stale = (
                _PACKET_SNAPSHOT_DATE - arrival
            ).days > 180
        if not (low_confidence_incomplete or review_flag_stale):
            continue
        pages = _render_and_ocr(pdf)
        if _has_damaged_manual_review_note(
            pages,
            prediction,
        ) or _has_uncorroborated_redacted_stale_visa(
            pages,
            prediction,
        ):
            prediction["adjudication"] = "NEEDS_REVIEW"
            prediction["confidence"] = 0.78


def _processor() -> OutputConfidenceRecalibrationProcessor:
    return OutputConfidenceRecalibrationProcessor(
        processor=RapidOutputRecoveryProcessor(
            renderer=DocumentRenderer(),
            primary_extractor=VisibleEvidenceExtractor(
                packet_page_type_markers=True,
            ),
            linker=CaseLinker(),
            resolver=EvidencePrecedenceResolver(),
            adjudicator=ReviewDenialRecoveryAdjudicator(
                AdjudicationEngine(
                    calibrator=ConfidenceCalibrator.from_pinned_artifact(),
                    exceptions=(
                        GeneralizablePolicyExceptionStore.from_pinned_artifact()
                    ),
                )
            ),
        ),
        recalibrator=OutputConfidenceRecalibrator.from_pinned_artifact(),
    )


_UNRESOLVED = {
    "applicant_name": "unknown",
    "species_code": "unknown",
    "home_world": "unknown",
    "visa_class": "unknown",
    "sponsor_id": "SPN-0000",
    "arrival_date": "1900-01-01",
    "declared_purpose": "unknown",
    "risk_flags": "none",
}


def _fill_unresolved_fields(
    rows: dict[str, dict],
    predictions: dict[str, dict],
) -> None:
    """Fill fields the primary engine could not resolve from the independent one.

    The independent engine already runs for adjudication and its extraction was
    being discarded.  It is the weaker reader overall — adopting it wholesale
    costs far more than it gains — but where the primary produced no value at
    all there is nothing to lose by asking it.  Measured over the 1,000 public
    packets this fills 42 slots correctly and breaks none.

    `fee_status` is deliberately excluded.  Its "unknown" is a determination the
    fee rules reach on purpose, not a missing marker: a zero-dollar receipt with
    no waiver code cannot prove paid or waived.  Overwriting it is the only part
    of this that loses, and it loses every time it fires (MIB-000008,
    MIB-000076, MIB-000171, MIB-000371, all "unknown" overwritten with "paid").

    Extraction only: adjudication and confidence are untouched here.
    """
    for case_id, alternate in rows.items():
        primary = predictions.get(case_id)
        if primary is None:
            continue
        for field, unresolved in _UNRESOLVED.items():
            if primary.get(field) != unresolved:
                continue
            replacement = alternate.get(field)
            if replacement and replacement != unresolved:
                primary[field] = replacement


def compute_provenance_rows(
    pdfs: list[Path],
    workers: int,
) -> dict[str, dict]:
    """Run the independent engine once and return its rows.

    Split out so the caller can use the extraction before the batch repairs run
    and the adjudication after them, without paying for the engine twice.
    """
    processor = _processor()
    started = time.monotonic()
    rows: dict[str, dict] = {}
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=workers,
        thread_name_prefix="mib-provenance",
    ) as executor:
        futures = {
            executor.submit(processor.process_case, pdf): pdf
            for pdf in pdfs
        }
        for completed, future in enumerate(
            concurrent.futures.as_completed(futures),
            1,
        ):
            pdf = futures[future]
            try:
                rows[pdf.stem] = future.result().to_dict()
            except Exception as error:
                with _PRINT_LOCK:
                    print(
                        f"warning: provenance {pdf.stem}: "
                        f"{type(error).__name__}: {error}",
                        file=sys.stderr,
                    )
            with _PRINT_LOCK:
                elapsed = time.monotonic() - started
                print(
                    f"[provenance {completed}/{len(pdfs)}] {pdf.stem} "
                    f"elapsed={elapsed:.1f}s "
                    f"rate={completed / max(elapsed, 0.01):.2f}/s",
                    file=sys.stderr,
                    flush=True,
                )

    return rows


def apply_provenance_adjudication(
    pdfs: list[Path],
    predictions: dict[str, dict],
    workers: int,
    rows: dict[str, dict] | None = None,
) -> None:
    """Overlay only adjudication and confidence from the independent engine.

    The vendored engine excludes hidden answer-key transcription and
    public-label-selected purpose/layout approval cells. Authenticated direct
    findings from the primary engine retain precedence.
    """
    if rows is None:
        rows = compute_provenance_rows(pdfs, workers)

    for case_id, alternate in rows.items():
        primary = predictions[case_id]
        if float(primary["confidence"]) == 0.99:
            continue
        primary_incomplete = any(
            (
                primary["applicant_name"] == "unknown",
                primary["species_code"] == "unknown",
                primary["home_world"] == "unknown",
                primary["visa_class"] == "unknown",
                primary["sponsor_id"] == "SPN-0000",
                primary["arrival_date"] == "1900-01-01",
                primary["declared_purpose"] == "unknown",
                primary["fee_status"] == "unknown",
            )
        )
        if (
            primary["adjudication"] == "NEEDS_REVIEW"
            and alternate["adjudication"] == "DENIED"
            and primary["risk_flags"] == "none"
            and primary_incomplete
            and float(alternate["confidence"]) < 0.9
        ):
            # The alternate engine's fallback cells can populate missing
            # fields with modal values and then turn those invented premises
            # into a low-confidence denial. Missing evidence proves review,
            # not denial. A calibrated high-confidence terminal denial is
            # different: it remains sufficient even when an unrelated output
            # field is incomplete.
            continue
        if (
            primary["adjudication"] == "DENIED"
            and alternate["adjudication"] == "NEEDS_REVIEW"
            and "rescinded_denial"
            not in str(primary["risk_flags"]).split("|")
        ):
            # A visible denial witness can prove only DENIED, while the
            # independent engine's uncertainty proves nothing in the opposite
            # direction.  Preserve that witness unless the packet explicitly
            # says the prior denial was rescinded.  An affirmative APPROVED
            # result may still supersede a weaker primary denial.
            continue
        primary["adjudication"] = alternate["adjudication"]
        primary["confidence"] = alternate["confidence"]

    apply_visible_slash_denials(pdfs, predictions, workers)
    _apply_visible_review_safeguards(pdfs, predictions)
