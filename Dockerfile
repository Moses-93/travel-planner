FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/src \
    UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

FROM base AS builder



COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock* README.md ./
COPY src ./src
RUN uv sync --no-dev

FROM base AS production

RUN groupadd -r appuser && useradd -r -g appuser -m -s /sbin/nologin appuser

WORKDIR /app
COPY --from=builder /usr/local /usr/local

COPY . .
RUN chown -R appuser:appuser /app

USER appuser

CMD ["uvicorn", "travel_planner.main:app", "--host", "0.0.0.0", "--port", "8000"]
