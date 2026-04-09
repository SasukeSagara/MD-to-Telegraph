import bleach
from markdown_it import MarkdownIt

ALLOWED_TAGS = [
    "a",
    "aside",
    "b",
    "blockquote",
    "br",
    "code",
    "em",
    "figcaption",
    "figure",
    "h3",
    "h4",
    "hr",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "strong",
    "u",
    "ul",
]

ALLOWED_ATTRS = {
    "a": ["href"],
    "img": ["src"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


class MarkdownConverter:
    def __init__(self) -> None:
        self._md = MarkdownIt("commonmark", {"html": False, "linkify": True, "typographer": False})
        self._md.enable("strikethrough")

    def to_telegraph_html(self, markdown_text: str) -> str:
        raw_html = self._md.render(markdown_text)
        # Telegraph supports only h3/h4, so we keep heading semantics
        # by mapping unsupported heading levels into allowed ones.
        raw_html = (
            raw_html
            .replace("<h1>", "<h3>")
            .replace("</h1>", "</h3>")
            .replace("<h2>", "<h3>")
            .replace("</h2>", "</h3>")
            .replace("<h5>", "<h4>")
            .replace("</h5>", "</h4>")
            .replace("<h6>", "<h4>")
            .replace("</h6>", "</h4>")
        )
        clean_html = bleach.clean(
            raw_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRS,
            protocols=ALLOWED_PROTOCOLS,
            strip=True,
        )
        if not clean_html.strip():
            return "<p>(empty)</p>"
        return clean_html

