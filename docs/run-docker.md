# Run with Docker

1. Prepare `.env`.
2. Build and start:
   - `docker compose up -d --build`
   - After Dockerfile changes, a clean rebuild helps: `docker compose build --no-cache`
3. Logs:
   - `docker compose logs -f bot`
4. Healthcheck:
   - `docker compose ps`
   - Status should become `healthy` after startup.
5. SQLite persistence uses a volume:
   - `./data:/app/data`
   - Set `ACCOUNTS_DB_PATH=data/accounts.db` in `.env`.
6. Stop:
   - `docker compose down`
