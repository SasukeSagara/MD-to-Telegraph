# Release and Operations

## Release checklist

1. `uv lock --check`
2. `uv run ruff check .`
3. `uv run mypy app`
4. `uv run pytest`
5. `docker build -t md-telegraph:release .`

## Deploy

- `docker compose up -d --build`

## Operations

- Watch logs: `docker compose logs -f bot`
- Monitor rate limits and publish errors
- Rotate tokens and restart the service after upgrades
