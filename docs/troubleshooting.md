# Troubleshooting

## Token errors

Check `BOT_TOKEN` and `TELEGRAPH_ACCESS_TOKEN` in `.env`.

## Publish failures

- Check reachability of `api.telegra.ph`.
- Ensure content complies with Telegraph limits.

## CI failures

- Refresh the lockfile: `uv lock`.
- Run linters, types, and tests locally with `uv run ...`.
