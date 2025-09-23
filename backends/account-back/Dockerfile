# Stage 1: Build
FROM python:3.12-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .

RUN pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim
RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./src /app

ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app\
    DJANGO_SETTINGS_MODULE=core.settings.development

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "core.asgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]