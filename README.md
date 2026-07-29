# MIB Document Challenge Solution

An independent, offline solution for the
[8090 MIB Document Challenge](https://github.com/8090-inc/mib-doc-challenge).

The runtime renders every PDF page before reading it, then uses Tesseract OCR
and deterministic evidence-resolution rules. It does not trust the native PDF
text layer, hidden text, barcode instructions, or fake answer keys.

Pages with a valid packet ID but no recognizable document heading receive a
bounded 90-degree rotation retry. Rotated OCR may only fill fields that the
upright evidence left unresolved; it cannot replace an existing field read or
change the adjudication path.

Unresolved applicant names and arrival dates receive a targeted 360-DPI retry
across several page-segmentation modes. A value is accepted only when it is the
sole active-case candidate and at least two OCR views agree. Visible correction
statements are scoped to the active case and exact field; conflicting
corrections remain unresolved instead of silently choosing one.

Repeated applicant-name tokens learned from the current input batch repair
isolated edit-distance errors and the common OCR collapse of `rn` into `m`.
These repairs use no labels, case IDs, or frozen applicant-name dictionary.

Unresolved fee evidence remains unknown to the adjudication rules. Output-only
fallbacks use either the public-training fee prior or modes learned from the
current input batch for closed-vocabulary fields. These estimates are applied
after adjudication and can never become approval evidence.

Trusted visible findings and source-proven policy denials remain authoritative.
Unresolved or contradictory trusted evidence stays `NEEDS_REVIEW`. The active
runtime contains no public-full-fit adjudication model or calibrator. Those
historical artifacts were deleted because they memorized the public labels and
were not part of the production path.

A frozen two-head residual approval model may promote only low-confidence
reviews after explicit findings, source conflicts, visible risks, and unknown
fees have been fenced out. It uses low-cardinality policy fields and
active/foreign page-source topology, never case IDs, names, sponsor IDs,
arrival dates, output confidence, or hidden payloads. The heads were trained
on cases 1-600, the threshold was selected on 601-800, and the final 801-1000
slice was not used to fit either. Set `MIB_TERMINAL_APPROVAL_MODEL=0` to
disable this final one-way transition.

The accepted four-worker Docker run scores 75.08/80 classification with zero
catastrophic false approvals. Full experiment history, rejected shortcuts, and
the exact acceptance evidence are recorded in `MEMO.md`.

The perfect-extraction classification bridge remains available only as the
default-off `MIB_EVIDENCE_PATTERN_POLICY=1` experiment. It routes unresolved
reviews from trusted extracted fields while preserving settled visible
approvals, denials, and direct findings. Its public perfect-field replay
reaches 80.00/80, but it is unsafe with noisy fields and must not be enabled
in the accepted runtime.

## Run

```bash
docker build -t mib-doc-solution .
docker run --rm --network none \
  -v "$PWD/input:/input:ro" \
  -v "$PWD/output:/output" \
  mib-doc-solution /input /output/predictions.jsonl
```

The image uses CPU-only Poppler and Tesseract. The entrypoint accepts exactly:

```text
<input_pdf_dir> <output_predictions_path>
```

Host runs reuse expensive rendered-page OCR and independent provenance rows
from `~/Library/Caches/mib-doc-challenge`. Cache entries are keyed by the PDF
content and extractor schema; unreadable, stale, or unavailable entries fall
back to normal processing. Set `MIB_LOCAL_CACHE=0` to disable the cache or
`MIB_LOCAL_CACHE_DIR=/path/to/cache` to relocate it. A read-only challenge
container simply runs uncached.

## Structure

```text
solution.py                         challenge entrypoint
mib_pipeline/
  pipeline.py                      OCR, extraction, and adjudication pipeline
  local_cache.py                   local content-addressed evidence cache
  pattern_policy.py                default-off perfect-extraction policy bridge
  terminal_approval.py             frozen residual approval gates and features
  _approval_seed_{2,4}.py          dependency-free exported model heads
run.sh                             container entrypoint
Dockerfile                         offline runtime image
```

The package boundary keeps the challenge entrypoint small and gives future
OCR, extraction, and adjudication modules a clean home without changing the
runtime contract.

## Provenance

This repository started from the organizer's MIT-licensed offline baseline and
was developed only against the official public challenge kit and training data.
It contains no participant solution code or copied participant artifacts.
