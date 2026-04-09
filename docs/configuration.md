# Configuration

Все настройки считываются классом `Settings` из `app/config.py` через `.env`.

- `BOT_TOKEN` (обязательный)
- `TELEGRAPH_ACCESS_TOKEN` (обязательный)
- `DEFAULT_AUTHOR_NAME` (по умолчанию `MD Telegraph Bot`)
- `DEFAULT_AUTHOR_URL` (опционально)
- `MAX_MD_SIZE` (по умолчанию `30000`)
- `MAX_PAGES_PER_REQUEST` (по умолчанию `5`)
- `USER_RATE_LIMIT_PER_MINUTE` (по умолчанию `6`)
- `ENABLE_PERSONAL_ACCOUNTS` (`false` по умолчанию, включает персональные аккаунты Telegraph)
- `ACCOUNTS_DB_PATH` (путь к SQLite БД, по умолчанию `data/accounts.db`)
- `DEFAULT_LOCALE` (fallback-локаль бота, по умолчанию `en`)
- `LOCALES_DIR` (путь к JSON-файлам локалей, по умолчанию `app/locales`)
- `LOG_LEVEL` (`INFO` по умолчанию)
