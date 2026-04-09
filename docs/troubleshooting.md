# Troubleshooting

## Ошибка токена

Проверьте `BOT_TOKEN` и `TELEGRAPH_ACCESS_TOKEN` в `.env`.

## Публикация не проходит

- Проверьте доступность `api.telegra.ph`.
- Убедитесь, что контент не нарушает ограничения Telegraph.

## Ошибки в CI

- Обновите lockfile: `uv lock`.
- Проверьте линтеры/типы/тесты локально через `uv run`.
