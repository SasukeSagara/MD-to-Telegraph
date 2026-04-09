# Release and Ops

## Чеклист релиза

1. `uv lock --check`
2. `uv run ruff check .`
3. `uv run mypy app`
4. `uv run pytest`
5. `docker build -t md-telegraph:release .`

## Деплой

- `docker compose up -d --build`

## Операционка

- Мониторить логи `docker compose logs -f bot`
- Следить за rate-limit и ошибками публикаций
- Ротировать токены и перезапускать сервис при обновлениях
