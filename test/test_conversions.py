import pytest

from md2html.core import *
from md2html.html import (
    markdown_to_html as _markdown_to_html,
    text_to_fragment,
)
from md2html.node import *


def markdown_to_html(md: str) -> str:
    return _markdown_to_html(markdown_to_nodes(md))


def make_node(s: str) -> Node:
    return Node(contents=s)


def make_nodes(strs: list[str]) -> list[Node]:
    return [make_node(s) for s in strs]


def test_setup_nodes() -> None:
    nodes = setup_nodes("a\nb\nc")

    assert all(isinstance(node, Node) for node in nodes)

    assert len(nodes) == 3
    assert nodes[0].contents == "a"
    assert nodes[1].contents == "b"
    assert nodes[2].contents == "c"


def test_group_codeblock() -> None:
    nodes = make_nodes(["```", "some", "code", "```"])

    got_nodes = group_blocked_nodes(nodes)

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CodeblockNode)
    assert got_nodes[0].contents == "some\ncode"
    assert not got_nodes[0].language


def test_group_codeblock_with_language() -> None:
    nodes = make_nodes(["```python", "code", "```"])

    got_nodes = group_blocked_nodes(nodes)

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CodeblockNode)
    assert got_nodes[0].contents == "code"
    assert got_nodes[0].language == "python"


def test_group_python_blocks() -> None:
    nodes = make_nodes(["!!!", "some", "python", "!!!"])

    got_nodes = group_blocked_nodes(nodes)

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], PythonNode)
    assert got_nodes[0].contents == "some\npython"


def test_group_blockquote_blocks() -> None:
    nodes = make_nodes(["> this", "> is a", "> blockquote"])

    got_nodes = group_blocked_nodes(nodes)

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], BlockquoteNode)
    assert got_nodes[0].contents == "this\nis a\nblockquote"


def test_table_header_with_missing_header_separator() -> None:
    nodes = make_nodes(["| A | B | C |"])

    with pytest.raises(ValueError, match="missing .* header"):
        group_blocked_nodes(nodes)


@pytest.mark.parametrize("row", ["x| y |", "| y |x"])
def test_table_header_check_separator_pipe(row: str) -> None:
    nodes = make_nodes(["| A |", row])

    msg = "line must start and end with pipe"

    with pytest.raises(ValueError, match=msg):
        group_blocked_nodes(nodes)


@pytest.mark.parametrize(
    "row",
    [
        "|--|",
        "|xxx|",
        "|-x-|",
        "|:--:|",
        "|::---|",
        "|---::|",
        "|x---|",
        "|---x|",
    ],
)
def test_table_header_check_separator_is_formatted_correctly(row: str) -> None:
    nodes = make_nodes(["| A |", row])

    msg = "header separator must have:"

    with pytest.raises(ValueError, match=msg):
        group_blocked_nodes(nodes)


def test_table_header() -> None:
    nodes = make_nodes(["| A | B | C |", "|---|---|---|"])

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        TableNode(
            header=[
                HeaderCell("A"),
                HeaderCell("B"),
                HeaderCell("C"),
            ],
            rows=[],
        )
    ]


def test_table_header_separator_needs_same_number_of_cells() -> None:
    nodes = make_nodes(["| A |", "|---|---|"])

    with pytest.raises(ValueError, match="expected 1 cells, got 2 instead"):
        group_blocked_nodes(nodes)


def test_table_with_rows() -> None:
    nodes = make_nodes(["| A |", "|---|", "| row 1 |", "| row 2 |"])

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        TableNode(header=[HeaderCell("A")], rows=[["row 1"], ["row 2"]])
    ]


def test_table_with_trailing_content() -> None:
    nodes = make_nodes(["| A |", "|---|", "| row 1 |", "some text"])

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        TableNode(header=[HeaderCell("A")], rows=[["row 1"]]),
        Node(contents="some text"),
    ]


def test_table_with_alignment() -> None:
    nodes = make_nodes(
        ["|default|left|center|right|", "|---|:---|:---:|---:|"]
    )

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        TableNode(
            header=[
                HeaderCell("default", alignment=HeaderAlignment.DEFAULT),
                HeaderCell("left", alignment=HeaderAlignment.LEFT),
                HeaderCell("center", alignment=HeaderAlignment.CENTER),
                HeaderCell("right", alignment=HeaderAlignment.RIGHT),
            ],
            rows=[],
        ),
    ]


def test_table_with_trailing_content_after_separator() -> None:
    nodes = make_nodes(["| A |", "|---|", "some text"])

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        TableNode(header=[HeaderCell("A")], rows=[]),
        Node(contents="some text"),
    ]


def test_group_html_comments() -> None:
    nodes = make_nodes(["<!--this", "is a", "comment-->", ""])

    got_nodes = group_blocked_nodes(nodes)

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CommentNode)
    assert got_nodes[0].contents == "this\nis a\ncomment"


def test_group_html_comments_one_line() -> None:
    nodes = make_nodes(["<!--this is a comment-->"])

    got_nodes = group_blocked_nodes(nodes)

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CommentNode)
    assert got_nodes[0].contents == "this is a comment"


def test_group_html_comments_two_lines() -> None:
    nodes = make_nodes(["<!--this is\na comment-->"])

    got_nodes = group_blocked_nodes(nodes)

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CommentNode)
    assert got_nodes[0].contents == "this is\na comment"


def test_preserve_nodes_next_to_codeblock() -> None:
    nodes = make_nodes(["pre", "```", "code", "```", "post"])

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        Node(contents="pre"),
        CodeblockNode(contents="code"),
        Node(contents="post"),
    ]


def test_preserve_nodes_next_to_raw_python() -> None:
    nodes = make_nodes(["pre", "!!!", "code", "!!!", "post"])

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        Node(contents="pre"),
        PythonNode(contents="code"),
        Node(contents="post"),
    ]


def test_preserve_nodes_next_to_blockquote() -> None:
    nodes = make_nodes(["pre", "> line", "post"])

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        Node(contents="pre"),
        BlockquoteNode(contents="line"),
        Node(contents="post"),
    ]


def test_exception_throw_if_codeblock_end_isnt_hit() -> None:
    nodes = make_nodes(["```", "code"])

    with pytest.raises(ValueError):
        group_blocked_nodes(nodes)


def test_exception_throw_if_codeblock_without_body_is_missing_end() -> None:
    nodes = make_nodes(["```"])

    with pytest.raises(ValueError):
        group_blocked_nodes(nodes)


def test_exception_throw_if_raw_python_end_isnt_hit() -> None:
    nodes = make_nodes(["!!!", "code"])

    with pytest.raises(ValueError):
        group_blocked_nodes(nodes)


def test_exception_throw_if_raw_python_without_body_is_missing_end() -> None:
    nodes = make_nodes(["!!!"])

    with pytest.raises(ValueError):
        group_blocked_nodes(nodes)


def test_exception_throw_if_html_comment_not_closed() -> None:
    nodes = make_nodes(["<!--"])

    with pytest.raises(ValueError):
        group_blocked_nodes(nodes)


def test_classify_nodes() -> None:
    def run(x: str, expected: Node) -> None:
        assert classify_node(make_node(x)) == expected

    run("# hello", HeaderNode(level=1, contents="hello"))
    run("## hello", HeaderNode(level=2, contents="hello"))
    run("### hello", HeaderNode(level=3, contents="hello"))
    run("#### hello", HeaderNode(level=4, contents="hello"))

    run("", NewlineNode())

    run("* hello", BulletNode(contents="hello"))

    run("1. hello", NumListNode(contents="hello"))
    run("9. hello", NumListNode(contents="hello"))
    run("99. hello", NumListNode(contents="hello"))

    run("<html>", HtmlNode(contents="<html>"))

    run("- [ ] hello", CheckboxNode(checked=False, contents="hello"))
    run("- [x] hello", CheckboxNode(checked=True, contents="hello"))

    run("hello", TextNode(contents="hello"))


def test_group_text_nodes() -> None:
    nodes: list[Node] = [
        TextNode(contents="hello"),
        TextNode(contents="world"),
    ]

    got_nodes = group_text_nodes(nodes)

    assert got_nodes == [TextNode(contents="hello\nworld")]


def test_only_group_adjacent_nodes() -> None:
    nodes = [
        TextNode(contents="hello"),
        NewlineNode(),
        TextNode(contents="world"),
    ]

    got_nodes = group_blocked_nodes(nodes)

    assert got_nodes == [
        TextNode(contents="hello"),
        NewlineNode(),
        TextNode(contents="world"),
    ]


def test_group_bullet_nodes() -> None:
    nodes: list[Node] = [
        BulletNode(contents="item"),
        BulletNode(contents="another item"),
        BulletNode(contents="last item"),
    ]

    got_nodes = group_bullet_nodes(nodes)

    assert got_nodes == [
        BulletNode(data=["item", "another item", "last item"])
    ]


def test_group_only_adjacent_bullet_nodes() -> None:
    nodes = [
        BulletNode(contents="item"),
        TextNode(contents="text"),
        BulletNode(contents="item"),
    ]

    got_nodes = group_bullet_nodes(nodes)

    assert got_nodes == [
        BulletNode(data=["item"]),
        TextNode(contents="text"),
        BulletNode(data=["item"]),
    ]


def test_group_numbered_list_nodes() -> None:
    nodes: list[Node] = [
        NumListNode(contents="item 1"),
        NumListNode(contents="item 2"),
        NumListNode(contents="item 3"),
    ]

    got_nodes = group_number_list_nodes(nodes)

    assert got_nodes == [NumListNode(data=["item 1", "item 2", "item 3"])]


def test_group_only_adjacent_num_list_nodes() -> None:
    nodes = [
        NumListNode(contents="item"),
        TextNode(contents="text"),
        NumListNode(contents="item"),
    ]

    got_nodes = group_number_list_nodes(nodes)

    assert got_nodes == [
        NumListNode(data=["item"]),
        TextNode(contents="text"),
        NumListNode(data=["item"]),
    ]


def test_convert_node() -> None:
    def run(s: str, html: str) -> None:
        assert markdown_to_html(s) == html

    run("# hello", '<a id="hello" href="#hello"><h1>hello</h1></a>')
    run("## hello", '<a id="hello" href="#hello"><h2>hello</h2></a>')
    run("### hello", '<a id="hello" href="#hello"><h3>hello</h3></a>')
    run("#### hello", '<a id="hello" href="#hello"><h4>hello</h4></a>')

    run("hello", "<p>hello</p>")

    run("", "")
    run("\n", "<br>")

    run("<html>", "<html>")

    run("- [ ] hello", '<p><input type="checkbox">hello</p>')
    run("- [x] hello", '<p><input type="checkbox" checked>hello</p>')

    run("> hello\n> world", "<blockquote>hello\nworld</blockquote>")

    run("!!!\nhtml += 'hello'\n!!!", "hello")

    run("* hello\n* world", "<ul>\n<li>hello</li>\n<li>world</li>\n</ul>")

    run(
        "1. hello\n2. world",
        "\n".join(  # noqa: FLY002
            [
                '<ol style="margin-left: 3ch">',
                '<li i="1. ">hello</li>',
                '<li i="2. ">world</li>',
                "</ol>",
            ]
        ),
    )

    run("```\nhello world\n```", '<pre class="hljs">hello world</pre>')
    run("```\nhello\\nworld\n```", '<pre class="hljs">hello\\\\nworld</pre>')


def test_convert_table_node() -> None:
    markdown = "| A | B | C |\n|---|---|---|\n| 1 | 2 | 3 |"

    html = (
        "<table>"
        "<tr><th>A</th><th>B</th><th>C</th></tr>"
        "<tr><td>1</td><td>2</td><td>3</td></tr>"
        "</table>"
    )

    assert markdown_to_html(markdown) == html


def test_expand_inline_code_in_lists() -> None:
    assert (
        markdown_to_html("* *hello*") == "<ul>\n<li><em>hello</em></li>\n</ul>"
    )

    assert (
        markdown_to_html("1. *hello*")
        == '<ol style="margin-left: 3ch">\n<li i="1. "><em>hello</em></li>\n</ol>'
    )


def test_inline_markdown_expanded() -> None:
    html = markdown_to_html("*hello* **there** `world` ~~strikethrough~~")
    expected = (
        "<p><em>hello</em> "
        "<strong>there</strong> "
        '<code class="hljs">world</code> '
        "<s>strikethrough</s></p>"
    )

    assert html == expected


def test_expand_inline_markdown_in_blockquote() -> None:
    assert (
        markdown_to_html("> **hello**")
        == "<blockquote><strong>hello</strong></blockquote>"
    )


def test_expand_inline_markdown_in_table() -> None:
    markdown = "|*hello*|\n|---|\n|*world*|"
    html = (
        "<table>"
        "<tr><th><em>hello</em></th></tr>"
        "<tr><td><em>world</em></td></tr>"
        "</table>"
    )

    assert markdown_to_html(markdown) == html


def test_convert_table_with_alignment() -> None:
    markdown = """\
|default|left|center|right|
|-------|:---|:----:|----:|
|1|2|3|4|"""

    html = (
        "<table>"
        "<tr>"
        "<th>default</th>"
        '<th style="text-align: left;">left</th>'
        '<th style="text-align: center;">center</th>'
        '<th style="text-align: right;">right</th>'
        "</tr>"
        "<tr>"
        "<td>1</td>"
        '<td style="text-align: left;">2</td>'
        '<td style="text-align: center;">3</td>'
        '<td style="text-align: right;">4</td>'
        "</tr>"
        "</table>"
    )

    assert markdown_to_html(markdown) == html


def test_escape_html() -> None:
    markdown = """
# <x>

## <x>

### <x>

#### <x>

* <x>

1. <x>

```
<x>
```

> <x>

some text <x>

- [ ] <x>

- [x] <x>

| <x> |
| --- |
| <x> |

"""

    html = markdown_to_html(markdown)

    assert "<x>" not in html


def test_convert_html_comment_doesnt_throw_assertion() -> None:
    markdown_to_html("<!-- comment -->")


def test_convert_divider() -> None:
    assert markdown_to_html("---") == "<hr>"


def test_get_title_fails_when_no_header_is_found() -> None:
    nodes = markdown_to_nodes("no header here")

    with pytest.raises(ValueError, match="missing title"):
        get_title(nodes)


def test_text_to_fragment() -> None:
    tests = {
        "abc": "abc",
        "123": "123",
        "hello world": "hello-world",
        "Hello World!": "hello-world",
        "(this)(is)(a)(test)": "this-is-a-test",
    }

    for test, expected in tests.items():
        assert text_to_fragment(test) == expected
