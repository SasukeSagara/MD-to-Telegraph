from __future__ import annotations

from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
from typing import Any

from telegraph.aio import Telegraph


class TelegraphError(Exception):
    """Raised when Telegraph publication fails."""


@dataclass(slots=True)
class PublishResult:
    urls: list[str]
    page_count: int


class _ParagraphExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._buffer: list[str] = []
        self._depth = 0
        self._pre_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"p", "blockquote", "pre", "ul", "ol", "h3", "h4", "figure"}:
            self._depth += 1
        if tag == "pre":
            self._pre_depth += 1
        if self._depth > 0:
            attr_str = "".join(f' {k}="{escape(v, quote=True)}"' for k, v in attrs if v)
            self._buffer.append(f"<{tag}{attr_str}>")

    def handle_endtag(self, tag: str) -> None:
        if self._depth > 0:
            self._buffer.append(f"</{tag}>")
        if tag == "pre" and self._pre_depth > 0:
            self._pre_depth -= 1
        if tag in {"p", "blockquote", "pre", "ul", "ol", "h3", "h4", "figure"} and self._depth > 0:
            self._depth -= 1
            if self._depth == 0:
                snippet = "".join(self._buffer).strip()
                if snippet:
                    self._parts.append(snippet)
                self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._depth > 0:
            if self._pre_depth == 0 and not data.strip():
                # Ignore indentation/newline-only text nodes so Telegraph
                # doesn't render them as empty list items in browser view.
                return
            # HTMLParser decodes entities in text nodes; escape again so plain
            # text like "<markdown>" doesn't become an actual HTML tag.
            self._buffer.append(escape(data, quote=False))

    def chunks(self) -> list[str]:
        return self._parts


class TelegraphService:
    def __init__(
        self,
        *,
        access_token: str,
        author_name: str,
        author_url: str | None,
        max_pages_per_request: int,
        client: Telegraph | None = None,
    ) -> None:
        self._client = client or Telegraph(access_token=access_token)
        self._default_access_token = access_token
        self._author_name = author_name
        self._author_url = author_url
        self._max_pages_per_request = max_pages_per_request

    @staticmethod
    def split_html(html: str, max_chunk_size: int = 60000) -> list[str]:
        parser = _ParagraphExtractor()
        parser.feed(html)
        parts = parser.chunks() or [f"<p>{html}</p>"]
        chunks: list[str] = []
        current = ""

        for part in parts:
            if len(part) > max_chunk_size:
                # Last-resort split for very long code blocks or paragraphs.
                for i in range(0, len(part), max_chunk_size):
                    chunks.append(part[i : i + max_chunk_size])
                continue
            if len(current) + len(part) > max_chunk_size:
                if current:
                    chunks.append(current)
                current = part
            else:
                current += part
        if current:
            chunks.append(current)
        return chunks

    async def publish_html(
        self,
        title: str,
        html: str,
        *,
        access_token: str | None = None,
        author_name: str | None = None,
        author_url: str | None = None,
    ) -> PublishResult:
        chunks = self.split_html(html)
        if len(chunks) > self._max_pages_per_request:
            raise TelegraphError("TOO_MANY_PAGES_REQUIRED")

        token = access_token or self._default_access_token
        current_author_name = author_name or self._author_name
        current_author_url = author_url if author_url is not None else self._author_url
        client = (
            self._client
            if token == self._default_access_token
            else Telegraph(access_token=token)
        )

        urls: list[str] = []
        for idx, chunk in enumerate(chunks, start=1):
            page_title = title if len(chunks) == 1 else f"{title} (part {idx}/{len(chunks)})"
            try:
                response: dict[str, Any] = await client.create_page(
                    title=page_title,
                    html_content=chunk,
                    author_name=current_author_name,
                    author_url=current_author_url,
                    return_content=False,
                )
            except Exception as exc:  # noqa: BLE001
                raise TelegraphError(str(exc)) from exc

            page_url = response.get("url")
            if not page_url:
                raise TelegraphError("NO_URL_RETURNED")
            urls.append(str(page_url))
        return PublishResult(urls=urls, page_count=len(urls))

