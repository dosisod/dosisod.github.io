from md2html.core import categorize, expand_links, line_to_type, NodeType

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
