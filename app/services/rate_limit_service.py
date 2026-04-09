from collections import defaultdict, deque
from datetime import datetime, timedelta, timezone


class InMemoryRateLimiter:
    def __init__(self, per_minute: int) -> None:
        self._per_minute = per_minute
        self._storage: dict[int, deque[datetime]] = defaultdict(deque)

    def allow(self, user_id: int) -> bool:
        now = datetime.now(timezone.utc)
        window_start = now - timedelta(minutes=1)
        bucket = self._storage[user_id]
        while bucket and bucket[0] < window_start:
            bucket.popleft()
        if len(bucket) >= self._per_minute:
            return False
        bucket.append(now)
        return True

