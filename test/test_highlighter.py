from unittest.mock import patch

import pytest

from md2html.core import run_pipeline


def make_code_block(body: str, language: str = "") -> str:
    return f"```{language}\n{body}\n```"


@patch("md2html.core.hightlight_code")
def test_convert_code_block_language_set(mocked):
    block = make_code_block("hello world", language="python")

    mocked.return_value = "anything"

    run_pipeline(block)

    mocked.assert_called_with("hello world\n", "python")


def test_invalid_language_throws_error():
    block = make_code_block("hello world", language="not a language")

    with pytest.raises(ChildProcessError):
        run_pipeline(block)


def test_converter_is_actually_ran():
    block = make_code_block("1", language="python")

    html = run_pipeline(block)

    # "hljs-number" is one of the CSS styles that is applied as part of
    # the syntax highlighing. There is a probably better way to check
    # that it actually ran, but this should be good enough for now.
    assert "hljs-number" in html
