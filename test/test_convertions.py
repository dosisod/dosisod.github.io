from md2html.core import (
    NodeType,
    categorize,
    convert,
    expand_links,
    group_text,
    line_to_type
)

def test_expand_single_link():
    content = "[example.com](https://example.com)"
    expected = '<a href="https://example.com">example.com</a>'

    assert expand_links(content) == expected


def test_expand_multile_links():
    content = "[1](2) [3](4)"
    expected = '<a href="2">1</a> <a href="4">3</a>'

    assert expand_links(content) == expected


def test_line_type_detection():
    assert line_to_type("hello world") == NodeType.TEXT

    assert line_to_type("# hello world") == NodeType.HEADER_1
    assert line_to_type("## hello world") == NodeType.HEADER_2
    assert line_to_type("### hello world") == NodeType.HEADER_3
    assert line_to_type("#### hello world") == NodeType.HEADER_4

    assert line_to_type("* something") == NodeType.BULLET_ITEM

    assert line_to_type("1. something") == NodeType.NUMBERED_ITEM
    assert line_to_type("99. something") == NodeType.NUMBERED_ITEM

    assert line_to_type("<p>raw html</p>") == NodeType.RAW_HTML

    assert line_to_type("") == NodeType.NEWLINE

    assert line_to_type("!!!") == NodeType.RAW_PYTHON


def test_categorize():
    content = "# hello\nworld".split("\n")

    categorized = categorize(content)

    assert len(categorized) == 2

    assert categorized[0][0] == NodeType.HEADER_1
    assert categorized[0][1] == "# hello"

    assert categorized[1][0] == NodeType.TEXT
    assert categorized[1][1] == "world"


def convert_fixture(s: str) -> str:
    return convert(group_text(categorize(s.split("\n"))))


def test_convert_headings():
    assert convert_fixture("# Heading 1") == "<h1>Heading 1</h1><br>\n"
    assert convert_fixture("## Heading 2") == "<h2>Heading 2</h2><br>\n"
    assert convert_fixture("### Heading 3") == "<h3>Heading 3</h3><br>\n"
    assert convert_fixture("#### Heading 4") == "<h4>Heading 4</h4><br>\n"


def test_convert_text():
    assert convert_fixture("hello") == "<p>hello</p>\n"


def test_convert_bullet_list():
    assert convert_fixture("* hello\n") == "<ul>\n<li>hello</li>\n</ul>\n"

    assert convert_fixture("* hello\n* world\n") == (
        "<ul>\n"
        "<li>hello</li>\n"
        "<li>world</li>\n"
        "</ul>\n"
    )


def test_convert_numbered_list():
    assert convert_fixture("1. hello\n") == "<ol>\n<li>hello</li>\n</ol>\n"

    assert convert_fixture("1. hello\n2. world\n") == (
        "<ol>\n"
        "<li>hello</li>\n"
        "<li>world</li>\n"
        "</ol>\n"
    )


def test_convert_raw_html():
    assert convert_fixture("<something/>") == "<something/>\n"


def make_python_block(code: str) -> str:
    return f"!!!\n{code}\n!!!\n"


def test_convert_raw_python_single_line():
    block = make_python_block("html += 'hi'")

    assert convert_fixture(block) == "hi<br>\n"


def test_convert_raw_python_multi_line():
    block = make_python_block('html += "hello "\nhtml += "world"\n')

    assert convert_fixture(block) == "hello world<br>\n"


def test_convert_newline():
    block = convert_fixture("\n\n") == "<br>\n"


def test_group_text_lines():
    assert convert_fixture("hello\nthere\nworld") == "<p>hello\nthere\nworld</p>\n"
