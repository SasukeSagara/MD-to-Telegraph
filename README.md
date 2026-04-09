# MD -> Telegraph Bot

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/package%20manager-uv-6e56cf.svg)](https://docs.astral.sh/uv/)
[![Ruff](https://img.shields.io/badge/lint-ruff-46a758.svg)](https://github.com/astral-sh/ruff)
[![Mypy](https://img.shields.io/badge/types-mypy-2a6db2.svg)](https://mypy-lang.org/)
[![Pytest](https://img.shields.io/badge/tests-pytest-0a9edc.svg)](https://pytest.org/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Telegram-бот на `aiogram`, который:

- принимает сырой Markdown;
- безопасно конвертирует его в совместимый с Telegraph формат;
- публикует страницу (или несколько страниц при большом объеме);
- возвращает пользователю готовые ссылки.

Поддерживаются:

- обычный режим (сообщение боту);
- inline-режим (`@your_bot <markdown>`);
- опциональные персональные Telegraph-аккаунты на пользователя.

## Оглавление

- [MD -\> Telegraph Bot](#md---telegraph-bot)
  - [Оглавление](#оглавление)
  - [Возможности](#возможности)
  - [Быстрый старт](#быстрый-старт)
  - [Команды бота](#команды-бота)
  - [Конфигурация](#конфигурация)
  - [Документация](#документация)
  - [Разработка](#разработка)

## Возможности

- Конвертация Markdown -> Telegraph-compatible HTML с sanitization.
- Публикация через общий `access_token`.
- Fallback-шардинг длинного текста на несколько страниц.
- Inline-публикация с кратким in-memory cache.
- Аудит метаданных без хранения исходного Markdown.
- Опциональный personal-режим (`/myaccount ...`) с публикацией от имени пользователя.

## Быстрый старт

1. Установите `uv`.
2. Скопируйте пример окружения:
   - `Copy-Item .env.example .env` (PowerShell)
3. Заполните `.env` (минимум: `BOT_TOKEN`, `TELEGRAPH_ACCESS_TOKEN`).
4. Установите зависимости:
   - `uv sync --frozen --dev`
5. Запустите бота:
   - `uv run python -m app.main`

## Команды бота

- `/start` — инструкция по работе.
- отправка любого Markdown-сообщения — публикация в Telegraph.
- `/myaccount status` — статус personal/shared режима.
- `/myaccount on` — включить personal-режим (создать Telegraph-аккаунт).
- `/myaccount off` — вернуться к shared-режиму.
- `/myaccount rotate` — перевыпустить personal access token.

## Конфигурация

Ключевые переменные:

- `BOT_TOKEN`
- `TELEGRAPH_ACCESS_TOKEN`
- `MAX_MD_SIZE`
- `ENABLE_PERSONAL_ACCOUNTS`
- `ACCOUNTS_DB_PATH`

Полный список и описание: [docs/configuration.md](docs/configuration.md).

## Документация

- Старт и установка: [docs/getting-started.md](docs/getting-started.md)
- Токены и секреты: [docs/tokens-and-secrets.md](docs/tokens-and-secrets.md)
- Конфигурация: [docs/configuration.md](docs/configuration.md)
- Локальный запуск: [docs/run-local.md](docs/run-local.md)
- Запуск в Docker: [docs/run-docker.md](docs/run-docker.md)
- Использование: [docs/usage.md](docs/usage.md)
- Пользовательский флоу: [docs/user-flow.md](docs/user-flow.md)
- Архитектура: [docs/architecture.md](docs/architecture.md)
- Troubleshooting: [docs/troubleshooting.md](docs/troubleshooting.md)
- Релиз и эксплуатация: [docs/release-and-ops.md](docs/release-and-ops.md)

## Разработка

Проверки качества:

- `uv run ruff check .`
- `uv run mypy app`
- `uv run pytest`

Сборка контейнера:

- `docker build -t md-telegraph:local .`
