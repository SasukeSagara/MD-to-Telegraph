# Contributing

Thanks for your interest in improving this project.

## Development setup

1. Install [uv](https://docs.astral.sh/uv/).
2. Copy `.env.example` to `.env` and set `BOT_TOKEN` and `TELEGRAPH_ACCESS_TOKEN`.
3. Install dependencies: `uv sync --frozen --dev`
4. Run the bot: `uv run python -m app.main`

## Pull requests

- Keep changes focused on a single topic.
- Run checks locally before opening a PR:

  ```bash
  uv run ruff check .
  uv run mypy app
  uv run pytest
  ```

- Add or update tests when behavior changes.

## Style

- Python 3.11+, type hints where it helps clarity.
- Match existing formatting; Ruff is the source of truth for lint rules.

## Bot strings (i18n)

User-visible strings live in `app/locales/<locale>.json`. The default fallback is `en` (`DEFAULT_LOCALE`). The repo ships `en` and `ru`; to add another language, copy `en.json` to a new file (e.g. `es.json`) and translate all values. Keep keys identical across files.
