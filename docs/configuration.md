# Configuration

All settings are loaded by the `Settings` class in `app/config.py` from `.env`.

- `BOT_TOKEN` (required)
- `TELEGRAPH_ACCESS_TOKEN` (required)
- `DEFAULT_AUTHOR_NAME` (default: `MD Telegraph Bot`)
- `DEFAULT_AUTHOR_URL` (optional)
- `MAX_MD_SIZE` (default: `30000`)
- `MAX_PAGES_PER_REQUEST` (default: `5`)
- `USER_RATE_LIMIT_PER_MINUTE` (default: `6`)
- `ENABLE_PERSONAL_ACCOUNTS` (default: `false` — enables per-user Telegraph accounts)
- `ACCOUNTS_DB_PATH` (SQLite database path, default: `data/accounts.db`)
- `DEFAULT_LOCALE` (fallback locale, default: `en`)
- `LOCALES_DIR` (directory with locale JSON files, default: `app/locales`)
- `LOG_LEVEL` (default: `INFO`)
