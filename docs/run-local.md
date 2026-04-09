# Run Locally

1. `uv sync --frozen --dev`
2. Prepare `.env`
3. `uv run python -m app.main`

Linting and tests:

- `uv run ruff check .`
- `uv run mypy app`
- `uv run pytest`
