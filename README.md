# MIB Document Challenge Solution

An independent, offline solution for the
[8090 MIB Document Challenge](https://github.com/8090-inc/mib-doc-challenge).

The runtime renders every PDF page before reading it, then uses Tesseract OCR
and deterministic evidence-resolution rules. It does not trust the native PDF
text layer, hidden text, barcode instructions, or fake answer keys.

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

## Provenance

This repository started from the organizer's MIT-licensed offline baseline and
was developed only against the official public challenge kit and training data.
It contains no participant solution code or copied participant artifacts.
