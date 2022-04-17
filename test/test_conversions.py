import pytest

from md2html.core import *
from md2html.node import *


def make_node(s):
    return Node(contents=s)


def make_nodes(strs):
    return [make_node(s) for s in strs]


def test_setup_nodes():
    nodes = setup_nodes("a\nb\nc")

    assert all([isinstance(node, Node) for node in nodes])

    assert len(nodes) == 3
    assert nodes[0].contents == "a"
    assert nodes[1].contents == "b"
    assert nodes[2].contents == "c"


def test_group_codeblock():
    nodes = make_nodes(["```", "some", "code", "```"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CodeblockNode)
    assert got_nodes[0].data == ["", "some\ncode"]


def test_group_codeblock_with_language():
    nodes = make_nodes(["```python", "code", "```"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CodeblockNode)
    assert got_nodes[0].data == ["python", "code"]


def test_group_python_blocks():
    nodes = make_nodes(["!!!", "some", "python", "!!!"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], PythonNode)
    assert got_nodes[0].contents == "some\npython"


def test_group_blockquote_blocks():
    nodes = make_nodes(["> this", "> is a", "> blockquote"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], BlockquoteNode)
    assert got_nodes[0].contents == "this\nis a\nblockquote"


def test_table_header_with_missing_header_seperator():
    nodes = make_nodes(["| A | B | C |"])

    with pytest.raises(ValueError, match="missing .* header") as exc:
        group_blocked_nodes(iter(nodes))


@pytest.mark.parametrize("row", ["x| y |", "| y |x"])
def test_table_header_check_seperator_pipe(row):
    nodes = make_nodes(["| A |", row])

    msg = "line must start and end with pipe"

    with pytest.raises(ValueError, match=msg) as exc:
        group_blocked_nodes(iter(nodes))


def test_table_header():
    nodes = make_nodes(["| A | B | C |", "|---|---|---|"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [TableNode(header=["A", "B", "C"], rows=[])]


def test_table_header_seperator_needs_same_number_of_cells():
    nodes = make_nodes(["| A |", "|---|---|"])

    with pytest.raises(ValueError, match="expected 1 cells, got 2 instead"):
        group_blocked_nodes(iter(nodes))


def test_table_with_rows():
    nodes = make_nodes(["| A |", "|---|", "| row 1 |", "| row 2 |"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [TableNode(header=["A"], rows=[["row 1"], ["row 2"]])]


def test_table_with_trailing_content():
    nodes = make_nodes(["| A |", "|---|", "| row 1 |", "some text"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [
        TableNode(header=["A"], rows=[["row 1"]]),
        Node(contents="some text"),
    ]


def test_table_with_trailing_content_after_seperator():
    nodes = make_nodes(["| A |", "|---|", "some text"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [
        TableNode(header=["A"], rows=[]),
        Node(contents="some text"),
    ]


def test_group_html_comments():
    nodes = make_nodes(["<!--this", "is a", "comment-->", ""])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CommentNode)
    assert got_nodes[0].contents == "this\nis a\ncomment"


def test_group_html_comments_one_line():
    nodes = make_nodes(["<!--this is a comment-->"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CommentNode)
    assert got_nodes[0].contents == "this is a comment"


def test_group_html_comments_two_lines():
    nodes = make_nodes(["<!--this is\na comment-->"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert len(got_nodes) == 1
    assert isinstance(got_nodes[0], CommentNode)
    assert got_nodes[0].contents == "this is\na comment"


def test_preserve_nodes_next_to_codeblock():
    nodes = make_nodes(["pre", "```", "code", "```", "post"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [
        Node(contents="pre"),
        CodeblockNode(data=["", "code"]),
        Node(contents="post"),
    ]


def test_preserve_nodes_next_to_raw_python():
    nodes = make_nodes(["pre", "!!!", "code", "!!!", "post"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [
        Node(contents="pre"),
        PythonNode(contents="code"),
        Node(contents="post"),
    ]


def test_preserve_nodes_next_to_blockquote():
    nodes = make_nodes(["pre", "> line", "post"])

    got_nodes = group_blocked_nodes(iter(nodes))

    assert got_nodes == [
        Node(contents="pre"),
        BlockquoteNode(contents="line"),
        Node(contents="post"),
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


def test_exception_throw_if_html_comment_not_closed():
    nodes = make_nodes(["<!--"])

    with pytest.raises(ValueError):
        group_blocked_nodes(iter(nodes))


def test_classify_nodes():
    def run(x, expected):
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


def test_group_text_nodes():
    nodes = [
        TextNode(contents="hello"),
        TextNode(contents="world"),
    ]

    got_nodes = group_text_nodes(nodes)

    assert got_nodes == [TextNode(contents="hello\nworld")]


def test_only_group_adjacent_nodes():
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


def test_group_bullet_nodes():
    nodes = [
        BulletNode(contents="item"),
        BulletNode(contents="another item"),
        BulletNode(contents="last item"),
    ]

    got_nodes = group_bullet_nodes(nodes)

    assert got_nodes == [
        BulletNode(data=["item", "another item", "last item"])
    ]


def test_group_only_adjacent_bullet_nodes():
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


def test_group_numbered_list_nodes():
    nodes = [
        NumListNode(contents="item 1"),
        NumListNode(contents="item 2"),
        NumListNode(contents="item 3"),
    ]

    got_nodes = group_number_list_nodes(nodes)

    assert got_nodes == [NumListNode(data=["item 1", "item 2", "item 3"])]


def test_group_only_adjacent_num_list_nodes():
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

    run("!!!\nhtml += 'hello'\n!!!", "hello")

    run("* hello\n* world", "<ul>\n<li>hello</li>\n<li>world</li>\n</ul>")

    run("1. hello\n2. world", "<ol>\n<li>hello</li>\n<li>world</li>\n</ol>")

    run("```\nhello world\n```", '<pre class="hljs">hello world</pre>')


def test_convert_table_node():
    markdown = "| A | B | C |\n|---|---|---|\n| 1 | 2 | 3 |"

    html = "<table><tr><th>A</th><th>B</th><th>C</th></tr><tr><td>1</td><td>2</td><td>3</td></tr></table>"

    assert markdown_to_html(markdown) == html


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


def test_expand_inline_markdown_in_blockquote():
    assert (
        markdown_to_html("> **hello**")
        == "<blockquote><strong>hello</strong></blockquote>"
    )


def test_expand_inline_markdown_in_table():
    markdown = "|*hello*|\n|---|\n|*world*|"
    html = "<table><tr><th><em>hello</em></th></tr><tr><td><em>world</em></td></tr></table>"

    assert markdown_to_html(markdown) == html


def test_escape_html():
    markdown = f"""
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


def test_convert_html_comment_doesnt_throw_assertion():
    markdown_to_html("<!-- comment -->")
