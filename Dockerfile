FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV UV_INSTALL_DIR="/usr/local/bin"
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY app ./app
COPY docker ./docker
COPY main.py ./main.py
COPY .env.example ./.env.example

RUN useradd -m appuser
RUN chown -R appuser:appuser /app
RUN chmod +x /app/docker/entrypoint.sh
USER appuser

ENTRYPOINT ["/app/docker/entrypoint.sh"]
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 CMD ["uv", "run", "--no-sync", "python", "-m", "app.healthcheck"]

