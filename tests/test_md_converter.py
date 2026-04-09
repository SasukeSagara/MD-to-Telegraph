from app.services.md_converter import MarkdownConverter


def test_markdown_converter_keeps_supported_tags() -> None:
    converter = MarkdownConverter()
    html = converter.to_telegraph_html("### Title\n\n**bold** and [link](https://example.com)")
    assert "<h3>Title</h3>" in html
    assert "<strong>bold</strong>" in html
    assert 'href="https://example.com"' in html


def test_markdown_converter_strips_unsafe_html() -> None:
    converter = MarkdownConverter()
    html = converter.to_telegraph_html('<script>alert(1)</script><p>Hello</p>')
    assert "<script>" not in html
    assert "alert(1)" in html
    assert "Hello" in html


def test_markdown_converter_maps_unsupported_headings() -> None:
    converter = MarkdownConverter()
    html = converter.to_telegraph_html("# H1\n\n## H2\n\n##### H5\n\n###### H6")
    assert "<h1>" not in html
    assert "<h2>" not in html
    assert "<h5>" not in html
    assert "<h6>" not in html
    assert "<h3>H1</h3>" in html
    assert "<h3>H2</h3>" in html
    assert "<h4>H5</h4>" in html
    assert "<h4>H6</h4>" in html


def test_markdown_converter_supports_strikethrough() -> None:
    converter = MarkdownConverter()
    html = converter.to_telegraph_html("~~deprecated~~")
    assert "<s>deprecated</s>" in html
