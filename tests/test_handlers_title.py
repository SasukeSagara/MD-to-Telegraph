from app.bot.handlers import _build_page_title, _extract_markdown_h1_title, _extract_title_and_body


def test_extract_markdown_h1_title_from_first_non_empty_line() -> None:
    text = "\n\n# Usage\n\nBody text"
    assert _extract_markdown_h1_title(text) == "Usage"


def test_extract_markdown_h1_title_returns_none_for_non_h1_first_line() -> None:
    text = "## Usage\n\nBody text"
    assert _extract_markdown_h1_title(text) is None


def test_extract_markdown_h1_title_returns_none_for_plain_text_first_line() -> None:
    text = "Usage\n\n# Not first"
    assert _extract_markdown_h1_title(text) is None


def test_build_page_title_fallback_contains_user_label() -> None:
    title = _build_page_title("@SasukeSagara")
    assert title.startswith("@SasukeSagara - ")


def test_extract_title_and_body_removes_first_h1_from_body() -> None:
    title, body = _extract_title_and_body("# Usage\n\n## Section\n\nText")
    assert title == "Usage"
    assert body.startswith("## Section")
    assert "# Usage" not in body


def test_extract_title_and_body_keeps_original_when_no_h1() -> None:
    source = "## Usage\n\nText"
    title, body = _extract_title_and_body(source)
    assert title is None
    assert body == source
