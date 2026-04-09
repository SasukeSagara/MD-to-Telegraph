# Run Local

1. `uv sync --frozen --dev`
2. Подготовить `.env`
3. `uv run python -m app.main`

Проверка линтеров и тестов:

- `uv run ruff check .`
- `uv run mypy app`
- `uv run pytest`
