from __future__ import annotations

import os
import sys

import httpx


def main() -> int:
    token = os.getenv("BOT_TOKEN")
    if not token:
        return 1

    url = f"https://api.telegram.org/bot{token}/getMe"
    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
    except Exception:
        return 1
    return 0 if data.get("ok") is True else 1


if __name__ == "__main__":
    sys.exit(main())

