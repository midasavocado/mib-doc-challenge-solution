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

Unresolved fee evidence remains unknown to the adjudication rules. Output-only
fallbacks use either the public-training fee prior or modes learned from the
current input batch for closed-vocabulary fields. These estimates are applied
after adjudication and can never become approval evidence.

Trusted visible findings and strong policy denials remain authoritative. Only
the lower-confidence approve/review fallback is refined by a small offline
candidate-trained histogram model. Its features exclude case IDs, applicant
names, raw sponsor IDs, filenames, hashes, and document fingerprints.
Fallback confidence is estimated by a separately cross-fitted logistic
calibrator using only model probabilities and decision-path metadata.

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

## Structure

```text
solution.py                         challenge entrypoint
mib_pipeline/
  pipeline.py                      OCR, extraction, and adjudication pipeline
  adjudication_model.json          offline fallback classifier
  adjudication_calibrator.json     cross-fitted confidence calibrator
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
