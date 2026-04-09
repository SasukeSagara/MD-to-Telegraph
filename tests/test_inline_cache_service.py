import time

from app.services.inline_cache_service import InlineCacheValue, InMemoryInlineCache


def test_inline_cache_set_and_get() -> None:
    cache = InMemoryInlineCache(ttl_seconds=10)
    cache.set("k", InlineCacheValue(text="hello", urls=["https://telegra.ph/x"], page_count=1))
    value = cache.get("k")
    assert value is not None
    assert value.page_count == 1


def test_inline_cache_expires() -> None:
    cache = InMemoryInlineCache(ttl_seconds=1)
    cache.set("k", InlineCacheValue(text="hello", urls=["https://telegra.ph/x"], page_count=1))
    time.sleep(1.1)
    assert cache.get("k") is None

