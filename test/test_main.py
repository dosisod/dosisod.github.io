from tempfile import mkstemp
from unittest.mock import call, patch
from pathlib import Path
from time import sleep
import timeit

import pytest

from md2html.core import convert_file, main


@patch("builtins.print")
def test_print_usage_if_not_enough_args(mocked_print):
    main(["argv0"])
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


@patch("md2html.core.convert_file")
def test_convert_multiple_files(mocked):
    main(["argv0", "a", "b", "c"])

    assert mocked.call_args_list == [call("a"), call("b"), call("c")]


@patch("md2html.core.convert_file")
def test_convert_multiple_files(mocked):
    """
    Threading works differently on different machines, so this test (might)
    fail on some machines. In general though, if threading is enabled, we
    should expect that all threaded calls to "convert_file" will collectively
    run faster then the same calls ran in parallel. We also check that the
    tests took more then SLEEP_FOR_MS time, just to make sure the sleep is
    working correctly.
    """

    MAX_THREADS = 10
    SLEEP_FOR_MS = 500

    ms_to_second = lambda ms: ms / 1_000

    mocked.side_effect = lambda _: sleep(ms_to_second(SLEEP_FOR_MS))

    start_time = timeit.default_timer()
    main(["argv0", *(["filename"] * MAX_THREADS)])
    elapsed_time = timeit.default_timer() - start_time

    assert mocked.call_count == MAX_THREADS

    assert elapsed_time > ms_to_second(SLEEP_FOR_MS)
    assert elapsed_time < ms_to_second(MAX_THREADS * SLEEP_FOR_MS)
