from md2html.core import (
    NodeType,
    categorize,
    convert,
    expand_bold,
    expand_italics,
    expand_links,
    expand_code,
    group_text,
    line_to_type,
    run_pipeline,
)


def test_expand_bold():
    content = "hello **there** world"
    expected = "hello <strong>there</strong> world"

    assert expand_bold(content) == expected


def test_expand_bold_multiple():
    content = "hello **there** world **goodbye** world"
    expected = "hello <strong>there</strong> world <strong>goodbye</strong> world"

    assert expand_bold(content) == expected


def test_expand_italics():
    content = "hello *there* world"
    expected = "hello <em>there</em> world"

    assert expand_italics(content) == expected


def test_expand_italics_multiple():
    content = "hello *there* world *goodbye* world"
    expected = "hello <em>there</em> world <em>goodbye</em> world"

    assert expand_italics(content) == expected


def test_expand_code():
    content = "hello `there` world"
    expected = "hello <code>there</code> world"

    assert expand_code(content) == expected


def test_expand_code_multiple():
    content = "hello `there` world `goodbye` world"
    expected = "hello <code>there</code> world <code>goodbye</code> world"

    assert expand_code(content) == expected


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
    assert line_to_type("*not a bullet point") != NodeType.BULLET_ITEM

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


def test_convert_headings():
    assert run_pipeline("# Heading 1") == "<h1>Heading 1</h1><br>\n"
    assert run_pipeline("## Heading 2") == "<h2>Heading 2</h2><br>\n"
    assert run_pipeline("### Heading 3") == "<h3>Heading 3</h3><br>\n"
    assert run_pipeline("#### Heading 4") == "<h4>Heading 4</h4><br>\n"


def test_convert_text():
    assert run_pipeline("hello") == "<p>hello</p>\n"


def test_convert_bullet_list():
    assert run_pipeline("* hello\n") == "<ul>\n<li>hello</li>\n</ul>\n"

    assert run_pipeline("* hello\n* world\n") == (
        "<ul>\n"
        "<li>hello</li>\n"
        "<li>world</li>\n"
        "</ul>\n"
    )


def test_convert_numbered_list():
    assert run_pipeline("1. hello\n") == "<ol>\n<li>hello</li>\n</ol>\n"

    assert run_pipeline("1. hello\n2. world\n") == (
        "<ol>\n"
        "<li>hello</li>\n"
        "<li>world</li>\n"
        "</ol>\n"
    )


def test_convert_raw_html():
    assert run_pipeline("<something/>") == "<something/>\n"


def make_python_block(code: str) -> str:
    return f"!!!\n{code}\n!!!\n"


def test_convert_raw_python_single_line():
    block = make_python_block("html += 'hi'")

    assert run_pipeline(block) == "hi<br>\n"


def test_convert_raw_python_multi_line():
    block = make_python_block('html += "hello "\nhtml += "world"\n')

    assert run_pipeline(block) == "hello world<br>\n"


def test_convert_newline():
    block = run_pipeline("\n\n") == "<br>\n"


def test_group_text_lines():
    assert run_pipeline("hello\nthere\nworld") == "<p>hello\nthere\nworld</p>\n"


def test_pipeline_runs_bold():
    assert run_pipeline("**hello**") == "<p><strong>hello</strong></p>\n"


def test_pipeline_runs_italics():
    assert run_pipeline("*hello*") == "<p><em>hello</em></p>\n"


def test_pipeline_converts_code():
    assert run_pipeline("`hello`") == "<p><code>hello</code></p>\n"


def test_multiline_bold_ignored():
    assert "<strong>" not in run_pipeline("**hello\n\n**world")


def test_multiline_italics_ignored():
    assert "<em>" not in run_pipeline("*hello\n\n*world")


def test_multiline_code_ignored():
    assert "<code>" not in run_pipeline("`hello\n\n`world")
