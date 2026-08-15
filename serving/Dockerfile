FROM python:3.11-slim-bookworm

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential cmake \
    && rm -rf /var/lib/apt/lists/*

COPY serving/requirements.txt .
# Prebuilt wheels enable OpenMP and deadlock on Railway's CPU; compile without it.
ENV CMAKE_ARGS="-DGGML_OPENMP=OFF -DGGML_BLAS=OFF" \
    FORCE_CMAKE=1
RUN pip install --no-cache-dir -r requirements.txt

COPY serving/server.py .

ENV PORT=8080 \
    PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port ${PORT:-8080}"]
