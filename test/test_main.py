from collections.abc import Iterator
from tempfile import mkstemp
from unittest.mock import call, patch
from pathlib import Path
from time import sleep
import timeit

import pytest

from md2html.main import convert_file, main


def test_print_usage_if_not_enough_args() -> None:
    with patch("builtins.print") as p:
        main(["argv0"])

        assert p.call_args[0][0].startswith("usage:")


@pytest.fixture()
def tempfile() -> Iterator[Path]:
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


def test_convert_multiple_files():
    with patch("md2html.main.convert_file") as mock:
        main(["argv0", "a", "b", "c"])

        assert mock.call_args_list == [call("a"), call("b"), call("c")]


def test_file_multi_threaded():
    """
    Threading works differently on different machines, so this test (might)
    fail on some machines. In general though, if threading is enabled, we
    should expect that all threaded calls to "convert_file" will collectively
    run faster then the same calls ran in parallel. We also check that the
    tests took more then sleep_for_ms time, just to make sure the sleep is
    working correctly.
    """

    max_threads = 10
    sleep_for_ms = 500

    ms_to_second = lambda ms: ms / 1_000

    with patch("md2html.main.convert_file") as convert_file:
        convert_file.side_effect = lambda _: sleep(ms_to_second(sleep_for_ms))

        start_time = timeit.default_timer()
        main(["argv0", *(["filename"] * max_threads)])
        elapsed_time = timeit.default_timer() - start_time

        assert convert_file.call_count == max_threads

        assert elapsed_time > ms_to_second(sleep_for_ms)
        assert elapsed_time < ms_to_second(max_threads * sleep_for_ms)


def test_exception_is_thrown_when_file_doesnt_exist():
    with pytest.raises(FileNotFoundError):
        main(["argv0", "file_doesnt_exist"])


def test_github_comment_feature_is_disabled_on_some_files():
    md_file = Path("./test/index.md")
    html_file = md_file.with_suffix(".html")

    md_file.write_text("# Some title")

    convert_file(str(md_file))

    ok = "github" not in html_file.read_text()

    md_file.unlink()
    html_file.unlink()

    assert ok
