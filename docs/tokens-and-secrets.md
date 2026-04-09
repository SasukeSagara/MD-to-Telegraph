# Tokens and Secrets

## BOT_TOKEN

1. Open [@BotFather](https://t.me/BotFather).
2. Create a bot with `/newbot`.
3. Save the token in `.env` as `BOT_TOKEN`.
4. Enable inline mode with `/setinline` (pick the bot and set a placeholder).

## TELEGRAPH_ACCESS_TOKEN

1. Read the Telegraph API docs: [createAccount](https://telegra.ph/api#createAccount).
2. Call `createAccount` (from a terminal, for example):

**PowerShell:**

```powershell
Invoke-RestMethod -Method Post -Uri "https://api.telegra.ph/createAccount" -Body @{
  short_name  = "mdtelegraph"
  author_name = "MD Telegraph Bot"
  author_url  = "https://t.me/your_username"
}
```

**curl:**

```bash
curl -X POST "https://api.telegra.ph/createAccount" \
  -d "short_name=mdtelegraph" \
  -d "author_name=MD Telegraph Bot" \
  -d "author_url=https://t.me/your_username"
```

3. Confirm the response has `ok: true` and `result.access_token`.

4. If PowerShell truncates output (e.g. `access_tok…`), print the token explicitly:

```powershell
$resp = Invoke-RestMethod -Method Post -Uri "https://api.telegra.ph/createAccount" -Body @{
  short_name  = "mdtelegraph"
  author_name = "MD Telegraph Bot"
  author_url  = "https://t.me/your_username"
}
$resp.ok
$resp.result.access_token
```

One-liner:

```powershell
(Invoke-RestMethod -Method Post -Uri "https://api.telegra.ph/createAccount" -Body @{
  short_name="mdtelegraph"; author_name="MD Telegraph Bot"; author_url="https://t.me/your_username"
}).result.access_token
```

5. Copy `result.access_token` into `.env`:

```env
TELEGRAPH_ACCESS_TOKEN=...
```

6. (Optional) Verify with `getAccountInfo`:

`https://api.telegra.ph/getAccountInfo?access_token=<TOKEN>&fields=["short_name","author_name","page_count"]`

7. If the token is compromised, rotate it with `revokeAccessToken`, or use `/myaccount rotate` for a personal account.

### Example `createAccount` response

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

## Security

- Do not commit `.env`.
- Do not log tokens.
- Rotate tokens after a leak.
