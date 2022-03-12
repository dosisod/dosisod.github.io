from tempfile import mkstemp
from unittest.mock import patch
from pathlib import Path

import pytest

from md2html.core import convert_file, main


@patch("builtins.print")
def test_print_usage_if_not_enough_args(mocked_print):
    main(["argv0"])
    assert mocked_print.call_args[0][0].startswith("usage:")


@patch("builtins.print")
def test_print_usage_if_too_many_args(mocked_print):
    main(["argv0", "too many", "args"])
    assert mocked_print.call_args[0][0].startswith("usage:")


@pytest.fixture
def tempfile():
    filename = mkstemp()[1]
    file = Path(filename)

    yield file

    if file.exists():
        file.unlink()


def test_file_is_created_properly(tempfile):
    with tempfile.open("w") as f:
        f.write("# Hello world")

    main(["argv0", str(tempfile)])

    html_file = tempfile.with_suffix(".html")
    assert html_file.exists()

    html = html_file.read_text()

    assert "<title>Hello world</title>" in html
    assert "Hello world" in html