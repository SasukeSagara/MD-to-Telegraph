from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(slots=True)
class InlineCacheValue:
    text: str
    urls: list[str]
    page_count: int


class InMemoryInlineCache:
    def __init__(self, ttl_seconds: int = 120) -> None:
        self._ttl = timedelta(seconds=ttl_seconds)
        self._storage: dict[str, tuple[datetime, InlineCacheValue]] = {}

    def get(self, key: str) -> InlineCacheValue | None:
        entry = self._storage.get(key)
        if entry is None:
            return None
        created_at, value = entry
        if datetime.now(timezone.utc) - created_at > self._ttl:
            self._storage.pop(key, None)
            return None
        return value

    def set(self, key: str, value: InlineCacheValue) -> None:
        self._storage[key] = (datetime.now(timezone.utc), value)

