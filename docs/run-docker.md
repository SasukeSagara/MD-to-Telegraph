# Run Docker

1. Подготовить `.env`
2. Собрать и запустить:
   - `docker compose up -d --build`
   - при изменениях Dockerfile лучше пересобрать без кэша: `docker compose build --no-cache`
3. Логи:
   - `docker compose logs -f bot`
4. Проверка статуса healthcheck:
   - `docker compose ps`
   - статус должен стать `healthy` после старта.
5. Для хранения SQLite-базы используется volume:
   - `./data:/app/data`
   - рекомендуется `ACCOUNTS_DB_PATH=data/accounts.db` в `.env`.
6. Остановка:
   - `docker compose down`
