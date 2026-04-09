# MD → Telegraph Bot

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/package%20manager-uv-6e56cf.svg)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/badge/lint-ruff-46a758.svg)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/types-mypy-2a6db2.svg)](https://mypy-lang.org/)
[![Pytest](https://img.shields.io/badge/tests-pytest-0a9edc.svg)](https://pytest.org/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Telegram bot built with [aiogram](https://docs.aiogram.dev/) that:

- Accepts raw Markdown in a message;
- Safely converts it to Telegraph-compatible HTML;
- Publishes one or more pages when content is large;
- Returns ready-to-use links.

Supported modes:

- Direct messages to the bot;
- Inline mode (`@your_bot <markdown>`);
- Optional per-user Telegraph accounts.

## Table of contents

- [Features](#features)
- [Quick start](#quick-start)
- [Bot commands](#bot-commands)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Development](#development)
- [License](#license)

## Features

- Markdown → Telegraph-safe HTML with sanitization.
- Publishing via a shared `access_token`.
- Automatic splitting of long content across multiple pages.
- Inline publishing with a short in-memory cache.
- Audit metadata without storing raw Markdown.
- Optional personal mode (`/myaccount ...`) publishing under the user’s name.

## Quick start

1. Install `uv`.
2. Copy the environment template:
   - PowerShell: `Copy-Item .env.example .env`
   - Unix: `cp .env.example .env`
3. Fill in `.env` (minimum: `BOT_TOKEN`, `TELEGRAPH_ACCESS_TOKEN`).
4. Install dependencies: `uv sync --frozen --dev`
5. Run: `uv run python -m app.main`

## Bot commands

- `/start` — how the bot works.
- Send any Markdown message — publish to Telegraph.
- `/myaccount status` — personal vs shared mode.
- `/myaccount on` — enable personal mode (creates a Telegraph account).
- `/myaccount off` — switch back to shared mode.
- `/myaccount rotate` — rotate the personal access token.

## Configuration

Key variables:

- `BOT_TOKEN`
- `TELEGRAPH_ACCESS_TOKEN`
- `MAX_MD_SIZE`
- `ENABLE_PERSONAL_ACCOUNTS`
- `ACCOUNTS_DB_PATH`

Full list: [docs/configuration.md](docs/configuration.md).

## Documentation

- Setup: [docs/getting-started.md](docs/getting-started.md)
- Tokens and secrets: [docs/tokens-and-secrets.md](docs/tokens-and-secrets.md)
- Configuration: [docs/configuration.md](docs/configuration.md)
- Run locally: [docs/run-local.md](docs/run-local.md)
- Docker: [docs/run-docker.md](docs/run-docker.md)
- Usage: [docs/usage.md](docs/usage.md)
- User flow: [docs/user-flow.md](docs/user-flow.md)
- Architecture: [docs/architecture.md](docs/architecture.md)
- Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)
- Release and operations: [docs/release-and-ops.md](docs/release-and-ops.md)

## Development

Quality checks:

- `uv run ruff check .`
- `uv run mypy app`
- `uv run pytest`

Docker image:

- `docker build -t md-telegraph:local .`

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).
