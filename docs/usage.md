# Usage

## Basic flow

1. User sends `/start`.
2. The bot explains how it works.
3. User sends full Markdown in a single message.
4. The bot publishes to Telegraph.
5. The bot returns one or more links.

## Inline mode

- In any chat: `@your_bot <markdown>`
- The bot publishes to Telegraph and returns an inline result with the link.
- Identical queries use a short in-memory cache to reduce API load.

## Personal Telegraph accounts (optional)

- `/myaccount status` — show the current mode.
- `/myaccount on` — create or enable a personal account for the user.
- `/myaccount off` — switch back to the shared account.
- `/myaccount rotate` — rotate the personal access token.
- Author name: `@username`, otherwise `first_name last_name`.
- Author link: `https://t.me/<username>`, otherwise `tg://user?id=<id>`.

## Limits

- Message length is capped (`MAX_MD_SIZE`).
- Telegraph allows only a limited set of HTML tags.
- Large content is split across multiple pages.
- Inline mode uses the same size limits and rate limiting.

## Localization

- Bot copy comes from locale files (`app/locales/*.json`). The repository includes `en` and `ru`.
- Locale is chosen from the user’s `language_code` in Telegram (e.g. `ru`, `ru-RU` → Russian).
- If no matching file exists, the bot falls back to `DEFAULT_LOCALE`.
