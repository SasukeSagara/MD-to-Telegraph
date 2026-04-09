# Troubleshooting

## Token errors

Check `BOT_TOKEN` and `TELEGRAPH_ACCESS_TOKEN` in `.env`.

## Publish failures

- Check reachability of `api.telegra.ph`.
- Ensure content complies with Telegraph limits.

## Telegraph page looks truncated after inline

Telegram passes at most **256 characters** of text after `@botname` to the bot. The rest never arrives, so the published page is only a fragment. **Send the full Markdown as a normal message to the bot** (private chat). See [Usage — Inline mode](usage.md#inline-mode).

## CI failures

- Refresh the lockfile: `uv lock`.
- Run linters, types, and tests locally with `uv run ...`.
