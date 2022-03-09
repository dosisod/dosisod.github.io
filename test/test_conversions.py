import pytest

from md2html.core import *


def make_node(s):
    return Node("UNKNOWN", s)


def make_nodes(strs):
    return [make_node(s) for s in strs]


def test_setup_nodes():
    nodes = setup_nodes("a\nb\nc")

    assert all([node.type == "UNKNOWN" for node in nodes])

    assert len(nodes) == 3
    assert nodes[0].contents == "a"
    assert nodes[1].contents == "b"
    assert nodes[2].contents == "c"


def test_group_codeblock():
    # TODO: fix needing "" by adding default value to next() iterator
    nodes = make_nodes(["```", "some", "code", "```", ""])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert got_nodes[0].type == "CODEBLOCK"
    assert got_nodes[0].data == ["", "some\ncode"]


def test_group_codeblock_with_language():
    nodes = make_nodes(["```python", "code", "```", ""])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert got_nodes[0].type == "CODEBLOCK"
    assert got_nodes[0].data == ["python", "code"]


def test_group_python_blocks():
    nodes = make_nodes(["!!!", "some", "python", "!!!", ""])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert got_nodes[0].type == "PYTHON_BLOCK"
    assert got_nodes[0].contents == "some\npython"


def test_group_blockquote_blocks():
    nodes = make_nodes(["> this", "> is a", "> blockquote", ""])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert got_nodes[0].type == "BLOCKQUOTE"
    assert got_nodes[0].contents == "this\nis a\nblockquote"


def test_group_html_comments():
    nodes = make_nodes(["<!--this", "is a", "comment-->", ""])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert got_nodes[0].type == "COMMENT"
    assert got_nodes[0].contents == "this\nis a\ncomment"


def test_group_html_comments_one_line():
    nodes = make_nodes(["<!--this is a comment-->"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert got_nodes[0].type == "COMMENT"
    assert got_nodes[0].contents == "this is a comment"


def test_group_html_comments_two_lines():
    nodes = make_nodes(["<!--this is\na comment-->"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert got_nodes[0].type == "COMMENT"
    assert got_nodes[0].contents == "this is\na comment"


def test_preserve_nodes_next_to_codeblock():
    # TODO: fix line directly after closing ``` getting eaten
    nodes = make_nodes(["pre", "```", "code", "```", "", "post"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [
        Node("UNKNOWN", "pre"),
        Node("CODEBLOCK", data=["", "code"]),
        Node("UNKNOWN", "post"),
    ]


def test_preserve_nodes_next_to_raw_python():
    # TODO: fix line directly after closing !!! getting eaten
    nodes = make_nodes(["pre", "!!!", "code", "!!!", "", "post"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [
        Node("UNKNOWN", "pre"),
        Node("PYTHON_BLOCK", "code"),
        Node("UNKNOWN", "post"),
    ]


def test_preserve_nodes_next_to_blockquote():
    # TODO: fix line directly after blockquote getting eaten
    nodes = make_nodes(["pre", "> line", "", "post"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [
        Node("UNKNOWN", "pre"),
        Node("BLOCKQUOTE", "line"),
        Node("UNKNOWN", "post"),
    ]


def test_exception_throw_if_codeblock_end_isnt_hit():
    nodes = make_nodes(["```", "code"])

    with pytest.raises(ValueError):
        group_blocked_nodes(iter(nodes))


def test_exception_throw_if_codeblock_without_body_is_missing_end():
    nodes = make_nodes(["```"])

    with pytest.raises(ValueError):
        group_blocked_nodes(iter(nodes))


def test_exception_throw_if_raw_python_end_isnt_hit():
    nodes = make_nodes(["!!!", "code"])

    with pytest.raises(ValueError):
        group_blocked_nodes(iter(nodes))


def test_exception_throw_if_raw_python_without_body_is_missing_end():
    nodes = make_nodes(["!!!"])

    with pytest.raises(ValueError):
        group_blocked_nodes(iter(nodes))


def test_classify_nodes():
    def run(x, expected):
        node = make_node(x)
        classify_node(node)

        assert node == expected

    run("## hello", Node("HEADER2", "hello"))
    run("### hello", Node("HEADER3", "hello"))
    run("#### hello", Node("HEADER4", "hello"))

    run("", Node("NEWLINE", ""))

    run("* hello", Node("BULLET", "hello"))

    run("1. hello", Node("NUM_LIST", "hello"))
    run("9. hello", Node("NUM_LIST", "hello"))
    run("99. hello", Node("NUM_LIST", "hello"))

    run("<html>", Node("HTML", "<html>"))

    run("- [ ] hello", Node("CHECKBOX_UNCHECKED", "hello"))
    run("- [x] hello", Node("CHECKBOX_CHECKED", "hello"))

    run("hello", Node("TEXT", "hello"))


def test_group_text_nodes():
    nodes = [
        Node("TEXT", "hello"),
        Node("TEXT", "world"),
    ]

    got_nodes = group_text_nodes(nodes)

    assert got_nodes == [Node("TEXT", "hello\nworld")]


def test_only_group_adjacent_nodes():
    nodes = [
        Node("TEXT", "hello"),
        Node("NEWLINE", ""),
        Node("TEXT", "world"),
    ]

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        Node("TEXT", "hello"),
        Node("NEWLINE", ""),
        Node("TEXT", "world"),
    ]


def test_group_bullet_nodes():
    nodes = [
        Node("BULLET", "item"),
        Node("BULLET", "another item"),
        Node("BULLET", "last item"),
    ]

    got_nodes = group_bullet_nodes(nodes)

    assert got_nodes == [
        Node("BULLET", data=["item", "another item", "last item"])
    ]


def test_group_only_adjacent_bullet_nodes():
    nodes = [
        Node("BULLET", "item"),
        Node("TEXT", "text"),
        Node("BULLET", "item"),
    ]

    got_nodes = group_bullet_nodes(nodes)

    assert got_nodes == [
        Node("BULLET", data=["item"]),
        Node("TEXT", "text"),
        Node("BULLET", data=["item"]),
    ]


def test_group_numbered_list_nodes():
    nodes = [
        Node("NUM_LIST", "item 1"),
        Node("NUM_LIST", "item 2"),
        Node("NUM_LIST", "item 3"),
    ]

    got_nodes = group_number_list_nodes(nodes)

    assert got_nodes == [Node("NUM_LIST", data=["item 1", "item 2", "item 3"])]


def test_group_only_adjacent_num_list_nodes():
    nodes = [
        Node("NUM_LIST", "item"),
        Node("TEXT", "text"),
        Node("NUM_LIST", "item"),
    ]

    got_nodes = group_number_list_nodes(nodes)

    assert got_nodes == [
        Node("NUM_LIST", data=["item"]),
        Node("TEXT", "text"),
        Node("NUM_LIST", data=["item"]),
    ]


def test_convert_node():
    def run(s, html):
        assert markdown_to_html(s) == html

    run("# hello", "<h1>hello</h1>")
    run("## hello", "<h2>hello</h2>")
    run("### hello", "<h3>hello</h3>")
    run("#### hello", "<h4>hello</h4>")

    run("hello", "<p>hello</p>")

    run("", "<br>")

    run("<html>", "<html>")

    run("- [ ] hello", '<p><input type="checkbox">hello</p>')
    run("- [x] hello", '<p><input type="checkbox" checked>hello</p>')

    run("> hello\n> world", "<blockquote>hello\nworld</blockquote>")

    run("!!!\nhtml += 'hello'\n!!!\n", "hello")

    run("* hello\n* world", "<ul>\n<li>hello</li>\n<li>world</li>\n</ul>")

    run("1. hello\n2. world", "<ol>\n<li>hello</li>\n<li>world</li>\n</ol>")

    run("```\nhello world\n```\n", '<pre class="hljs">hello world</pre>')


def test_expand_inline_code_in_lists():
    assert (
        markdown_to_html("* *hello*") == "<ul>\n<li><em>hello</em></li>\n</ul>"
    )

    assert (
        markdown_to_html("1. *hello*")
        == "<ol>\n<li><em>hello</em></li>\n</ol>"
    )


def test_inline_markdown_expanded():
    html = markdown_to_html("*hello* **there** `world`")
    expected = '<p><em>hello</em> <strong>there</strong> <code class="hljs">world</code></p>'

    assert html == expected
