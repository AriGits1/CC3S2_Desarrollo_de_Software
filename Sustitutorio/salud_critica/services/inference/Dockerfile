FROM python:3.11-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.11-slim
RUN useradd -m -u 1001 app
WORKDIR /app
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN pip install --no-cache --no-index --find-links=/wheels -r requirements.txt && rm -rf /wheels
COPY app.py .
USER app
HEALTHCHECK CMD python -c "import requests; requests.get('http://localhost:8001/health')"
CMD ["python", "app.py"]
