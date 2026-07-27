FROM python:3.12-slim

ENV OMP_THREAD_LIMIT=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends poppler-utils tesseract-ocr \
    && apt-get clean \
    && find /var/lib/apt/lists -mindepth 1 -delete

RUN pip install --no-cache-dir "numpy==2.3.1"

WORKDIR /app
COPY run.sh solution.py /app/
COPY mib_pipeline /app/mib_pipeline
RUN chmod +x /app/run.sh

ENTRYPOINT ["/app/run.sh"]
