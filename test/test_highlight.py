from unittest.mock import patch

import pytest

from md2html.core import markdown_to_nodes
from md2html.html import markdown_to_html as _markdown_to_html


def markdown_to_html(md: str) -> str:
    return _markdown_to_html(markdown_to_nodes(md))


# TODO: fix needing extra newline
def make_code_block(body: str, language: str = "") -> str:
    return f"```{language}\n{body}\n```\n"


def test_convert_code_block_language_set() -> None:
    with patch("md2html.html.hightlight_code") as highlight:
        block = make_code_block("hello world", language="python")

        highlight.return_value = "anything"

        markdown_to_html(block)

        highlight.assert_called_with("hello world", "python")


def test_highlighter_escapes_backslashes() -> None:
    with patch("md2html.html.hightlight_code") as highlight:
        block = make_code_block("hello\\nworld", language="python")

        highlight.return_value = "anything"

        markdown_to_html(block)

        highlight.assert_called_with("hello\\\\nworld", "python")


def test_invalid_language_throws_error() -> None:
    block = make_code_block("hello world", language="not a language")

    with pytest.raises(ChildProcessError):
        markdown_to_html(block)


def test_converter_is_actually_ran() -> None:
    block = make_code_block("1", language="python")

    html = markdown_to_html(block)

    # "hljs-number" is one of the CSS styles that is applied as part of
    # the syntax highlighing. There is a probably better way to check
    # that it actually ran, but this should be good enough for now.
    assert "hljs-number" in html


def test_codeblocks_are_not_doubly_escaped() -> None:
    block = make_code_block("<p>some text</p>", language="html")

    html = markdown_to_html(block)

    assert "amp" not in html
