FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends poppler-utils tesseract-ocr \
    && apt-get clean \
    && find /var/lib/apt/lists -mindepth 1 -delete

WORKDIR /app
COPY run.sh solution.py /app/
RUN chmod +x /app/run.sh

ENTRYPOINT ["/app/run.sh"]
