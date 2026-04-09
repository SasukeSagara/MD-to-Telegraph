import pytest
from typing import Any, cast

from app.services.telegraph_service import PublishResult, TelegraphError, TelegraphService


class FakeTelegraphClient:
    async def create_page(self, **kwargs):
        return {"url": f"https://telegra.ph/{kwargs['title'].replace(' ', '-')}"}


def test_split_html_into_chunks() -> None:
    html = "<p>" + ("x" * 70000) + "</p>"
    chunks = TelegraphService.split_html(html, max_chunk_size=60000)
    assert len(chunks) >= 2
    assert all(len(chunk) <= 60000 for chunk in chunks)


def test_split_html_keeps_escaped_tag_like_text() -> None:
    html = "<p>@your_bot &lt;markdown&gt; and https://t.me/&lt;username&gt;</p>"
    chunks = TelegraphService.split_html(html, max_chunk_size=60000)
    assert len(chunks) == 1
    assert "&lt;markdown&gt;" in chunks[0]
    assert "&lt;username&gt;" in chunks[0]
    assert "<markdown>" not in chunks[0]
    assert "<username>" not in chunks[0]


def test_split_html_omits_whitespace_only_nodes_in_lists() -> None:
    html = "<ol>\n<li>one</li>\n<li>two</li>\n</ol>"
    chunks = TelegraphService.split_html(html, max_chunk_size=60000)
    assert len(chunks) == 1
    assert chunks[0] == "<ol><li>one</li><li>two</li></ol>"


def test_split_html_preserves_whitespace_inside_pre() -> None:
    html = "<pre><code>line1\n  line2\n</code></pre>"
    chunks = TelegraphService.split_html(html, max_chunk_size=60000)
    assert len(chunks) == 1
    assert "line1\n  line2\n" in chunks[0]


@pytest.mark.asyncio
async def test_publish_respects_max_pages() -> None:
    service = TelegraphService(
        access_token="token",
        author_name="author",
        author_url=None,
        max_pages_per_request=1,
    )

    with pytest.raises(TelegraphError):
        await service.publish_html("title", "<p>" + ("x" * 70000) + "</p>")


@pytest.mark.asyncio
async def test_publish_html_uses_client() -> None:
    service = TelegraphService(
        access_token="token",
        author_name="author",
        author_url=None,
        max_pages_per_request=5,
        client=cast(Any, FakeTelegraphClient()),
    )
    result: PublishResult = await service.publish_html("title", "<p>Hello</p>")
    assert result.page_count == 1
    assert result.urls[0].startswith("https://telegra.ph/")
