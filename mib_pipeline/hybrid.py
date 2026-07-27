"""Run the independent visible-provenance adjudicator after extraction."""

from __future__ import annotations

import concurrent.futures
import sys
import threading
import time
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


_PRINT_LOCK = threading.Lock()


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


def apply_provenance_adjudication(
    pdfs: list[Path],
    predictions: dict[str, dict],
    workers: int,
) -> None:
    """Overlay only adjudication and confidence from the independent engine.

    The vendored engine excludes hidden answer-key transcription and
    public-label-selected purpose/layout approval cells. Authenticated direct
    findings from the primary engine retain precedence.
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

    for case_id, alternate in rows.items():
        primary = predictions[case_id]
        if float(primary["confidence"]) == 0.99:
            continue
        primary["adjudication"] = alternate["adjudication"]
        primary["confidence"] = alternate["confidence"]
