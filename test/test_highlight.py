from unittest.mock import patch

import pytest

from md2html.core import markdown_to_html


# TODO: fix needing extra newline
def make_code_block(body: str, language: str = "") -> str:
    return f"```{language}\n{body}\n```\n"


@patch("md2html.core.hightlight_code")
def test_convert_code_block_language_set(mocked):
    block = make_code_block("hello world", language="python")

    mocked.return_value = "anything"

    markdown_to_html(block)

    mocked.assert_called_with("hello world", "python")


@patch("md2html.core.hightlight_code")
def test_highlighter_escapes_backslashes(mocked):
    block = make_code_block("hello\\nworld", language="python")

    mocked.return_value = "anything"

    markdown_to_html(block)

    mocked.assert_called_with("hello\\\\nworld", "python")


def test_invalid_language_throws_error():
    block = make_code_block("hello world", language="not a language")

    with pytest.raises(ChildProcessError):
        markdown_to_html(block)


def test_converter_is_actually_ran():
    block = make_code_block("1", language="python")

    html = markdown_to_html(block)

    # "hljs-number" is one of the CSS styles that is applied as part of
    # the syntax highlighing. There is a probably better way to check
    # that it actually ran, but this should be good enough for now.
    assert "hljs-number" in html