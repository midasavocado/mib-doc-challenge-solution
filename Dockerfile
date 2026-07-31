FROM python:3.12-slim

ENV BLIS_NUM_THREADS=4 \
    MIB_MAX_WORKERS=4 \
    MKL_NUM_THREADS=4 \
    MIB_LOCAL_CACHE_DIR=/tmp/mib-doc-challenge \
    NUMEXPR_NUM_THREADS=4 \
    OMP_NUM_THREADS=4 \
    OMP_THREAD_LIMIT=1 \
    OPENBLAS_NUM_THREADS=4 \
    OC_DISABLE_DOT_ACCESS_WARNING=1 \
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
COPY third_party_licenses /app/third_party_licenses
RUN chmod +x /app/run.sh

ENTRYPOINT ["/app/run.sh"]
