FROM python:3.11-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git nodejs npm \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && python --version \
    && git --version \
    && node -e "const major = Number(process.versions.node.split('.')[0]); if (major < 18) process.exit(1)"

WORKDIR /workspace

COPY docker/certs/ /usr/local/share/ca-certificates/extra/
RUN update-ca-certificates

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BIBLIO_DATABASE_URL=sqlite:////workspace/data/biblio.db \
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt

COPY requirements.txt .
RUN pip install --no-cache-dir --cert /etc/ssl/certs/ca-certificates.crt -r requirements.txt

COPY . .
RUN mkdir -p /workspace/data

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
