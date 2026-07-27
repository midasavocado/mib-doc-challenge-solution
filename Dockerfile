FROM python:3.12-slim

ENV BLIS_NUM_THREADS=4 \
    MIB_MAX_WORKERS=4 \
    MKL_NUM_THREADS=4 \
    NUMEXPR_NUM_THREADS=4 \
    OMP_NUM_THREADS=4 \
    OMP_THREAD_LIMIT=1 \
    OPENBLAS_NUM_THREADS=4 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TOKENIZERS_PARALLELISM=false \
    VECLIB_MAXIMUM_THREADS=4

RUN apt-get update \
    && apt-get install -y --no-install-recommends poppler-utils tesseract-ocr \
    && apt-get clean \
    && find /var/lib/apt/lists -mindepth 1 -delete

COPY requirements.lock /app/requirements.lock
RUN python3 -m pip install \
      --disable-pip-version-check \
      --no-cache-dir \
      --no-deps \
      --require-hashes \
      --requirement /app/requirements.lock

WORKDIR /app
COPY run.sh solution.py /app/
COPY mib_pipeline /app/mib_pipeline
COPY provenance_engine /app/provenance_engine
COPY third_party_licenses /app/third_party_licenses
RUN chmod +x /app/run.sh

ENTRYPOINT ["/app/run.sh"]
