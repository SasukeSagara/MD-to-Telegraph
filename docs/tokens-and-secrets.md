# Tokens and Secrets

## BOT_TOKEN

1. Открыть [@BotFather](https://t.me/BotFather)
2. Создать бота через `/newbot`
3. Сохранить токен в `.env` как `BOT_TOKEN`
4. Включить inline-режим через `/setinline` (выбрать бота и задать placeholder)

## TELEGRAPH_ACCESS_TOKEN

1. Открыть документацию Telegraph API: [https://telegra.ph/api#createAccount](https://telegra.ph/api#createAccount).
2. Выполнить запрос `createAccount` (можно прямо из терминала):

- PowerShell:
  - `Invoke-RestMethod -Method Post -Uri "https://api.telegra.ph/createAccount" -Body @{ short_name = "mdtelegraph"; author_name = "MD Telegraph Bot"; author_url = "https://t.me/your_username" }`
- или `curl`:
  - `curl -X POST "https://api.telegra.ph/createAccount" -d "short_name=mdtelegraph" -d "author_name=MD Telegraph Bot" -d "author_url=https://t.me/your_username"`

3. Убедиться, что в ответе `ok: true`, а в `result` есть `access_token`.
2. Если в PowerShell видно только `access_tok…`, это нормально — консоль сокращает таблицу вывода.

- Выведите токен явно:

  - ```powershell

    $resp = Invoke-RestMethod -Method Post -Uri "<https://api.telegra.ph/createAccount>" -Body @{
      short_name  = "mdtelegraph"
      author_name = "MD Telegraph Bot"
      author_url  = "<https://t.me/your_username>"
    }

    $resp.ok
    $resp.result.access_token

    ```
- Однострочный вариант:

  - ```powershell

    (Invoke-RestMethod -Method Post -Uri "<https://api.telegra.ph/createAccount>" -Body @{ short_name="mdtelegraph"; author_name="MD Telegraph Bot"; author_url="<https://t.me/your_username>" }).result.access_token

    ```

5. Скопировать `result.access_token` и сохранить в `.env`:

- `TELEGRAPH_ACCESS_TOKEN=...`

6. (Опционально) Проверить токен через `getAccountInfo`:

- `https://api.telegra.ph/getAccountInfo?access_token=<TOKEN>&fields=["short_name","author_name","page_count"]`

7. Если токен скомпрометирован, перевыпустить через `revokeAccessToken` (или командой бота `/myaccount rotate` для персонального аккаунта).

### Пример ожидаемого ответа `createAccount`

```json
{
  "ok": true,
  "result": {
    "short_name": "mdtelegraph",
    "author_name": "MD Telegraph Bot",
    "author_url": "https://t.me/your_username",
    "access_token": "xxxxxxxxxxxxxxxx",
    "auth_url": "https://telegra.ph/auth/..."
  }
}
```

## Безопасность

- Не коммитить `.env`
- Не логировать токены
- Ротировать токены при утечке
