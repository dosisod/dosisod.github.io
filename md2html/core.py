from concurrent.futures import ThreadPoolExecutor
from html import escape
from pathlib import Path
from subprocess import run
from typing import Iterator, Optional
import re

from .node import *
from .pipe import pipe


def is_valid_table_row(row: str) -> bool:
    return bool(re.match(r"^\|.*\|$", row))


def iter_code_block(first: Node, nodes: Iterator[Node]) -> Node:
    lang = first.contents[3:]
    next_node = next(nodes, None)

    if not next_node:
        raise ValueError("codeblock end not reached")

    codeblock = next_node.contents

    for node in nodes:
        if node.contents.startswith("```"):
            return CodeblockNode(contents=codeblock, language=lang)

        else:
            codeblock += f"\n{node.contents}"

    raise ValueError("codeblock end not reached")


def iter_python_blocks(nodes: Iterator[Node]) -> Node:
    next_node = next(nodes, None)

    if not next_node:
        raise ValueError("python block end not reached")

    code = next_node.contents

    for node in nodes:
        if node.contents == "!!!":
            return PythonNode(contents=code)

        else:
            code += f"\n{node.contents}"

    raise ValueError("python block end not reached")


def iter_block_quote(
    first: Node, nodes: Iterator[Node]
) -> tuple[Node, Optional[Node]]:
    blockquote = first.contents[2:]

    for node in nodes:
        if not node.contents.startswith("> "):
            return (BlockquoteNode(contents=blockquote), node)

        blockquote += f"\n{node.contents[2:]}"

    return (BlockquoteNode(contents=blockquote), None)


def iter_html_comment(first: Node, nodes: Iterator[Node]) -> Node:
    if first.contents.endswith("-->"):
        return CommentNode(contents=first.contents[4:-3])

    comment = first.contents[4:]

    for node in nodes:
        if node.contents.endswith("-->"):
            comment += f"\n{node.contents[:-3]}"
            next(nodes)
            return CommentNode(contents=comment)

        else:
            comment += f"\n{node.contents}"

    raise ValueError("html comment not closed")


def iter_table(
    first: Node, nodes: Iterator[Node]
) -> tuple[Node, Optional[Node]]:
    def split_row(row: str) -> list[str]:
        return [x.strip() for x in row.split("|")[1:-1]]

    seperator_node = next(nodes, None)

    if not seperator_node:
        raise ValueError("table missing required header seperator")

    if not is_valid_table_row(seperator_node.contents):
        raise ValueError("line must start and end with pipe")

    seperator_cells = split_row(seperator_node.contents)

    def is_valid_seperator_cell(cell: str) -> bool:
        return bool(re.match("^:?-{3,}:?$", cell.strip()))

    if not all([is_valid_seperator_cell(x) for x in seperator_cells]):
        raise ValueError(
            "header seperator must have:\n\n"
            "* At least 3 dashes\n"
            "* (optional) starting/ending ':'\n"
            "* (optional) whitespace at start/end\n"
        )

    header = [HeaderCell(name) for name in split_row(first.contents)]

    if len(seperator_cells) != len(header):
        raise ValueError(
            f"expected {len(header)} cells, got {len(seperator_cells)} instead"
        )

    for i, name in enumerate(seperator_cells):
        match (name.startswith(":"), name.endswith(":")):
            case (True, True):
                header[i].alignment = HeaderAlignment.CENTER
            case (True, False):
                header[i].alignment = HeaderAlignment.LEFT
            case (False, True):
                header[i].alignment = HeaderAlignment.RIGHT
            case _:
                header[i].alignment = HeaderAlignment.DEFAULT

    rows: list[list[str]] = []

    while node := next(nodes, None):
        if not is_valid_table_row(node.contents):
            return (TableNode(header=header, rows=rows), node)

        rows.append(split_row(node.contents))

    return (TableNode(header=header, rows=rows), None)


def group_blocked_nodes(nodes: Iterator[Node]) -> list[Node]:
    grouped_nodes = []

    for node in nodes:
        if node.contents.startswith("```"):
            grouped_nodes.append(iter_code_block(node, nodes))

        elif node.contents == "!!!":
            grouped_nodes.append(iter_python_blocks(nodes))

        elif node.contents.startswith("> "):
            blockquote, leftover = iter_block_quote(node, nodes)
            grouped_nodes.append(blockquote)

            if leftover:
                grouped_nodes.append(leftover)

        elif node.contents.startswith("<!--"):
            grouped_nodes.append(iter_html_comment(node, nodes))

        elif is_valid_table_row(node.contents):
            table, leftover = iter_table(node, nodes)
            grouped_nodes.append(table)

            if leftover:
                grouped_nodes.append(leftover)

        else:
            grouped_nodes.append(node)

    return grouped_nodes


def is_already_classified(node: Node) -> bool:
    # since we know "node" derives from Node, we can check if the type is
    # anything other then Node, and if it is, we will know it is derived, and
    # thus is already classified.

    return type(node) != Node


def classify_node(node: Node) -> Node:
    if is_already_classified(node):
        return node

    if node.contents.startswith("# "):
        return HeaderNode(level=1, contents=node.contents[2:])

    if node.contents.startswith("## "):
        return HeaderNode(level=2, contents=node.contents[3:])

    if node.contents.startswith("### "):
        return HeaderNode(level=3, contents=node.contents[4:])

    if node.contents.startswith("#### "):
        return HeaderNode(level=4, contents=node.contents[5:])

    if node.contents == "":
        return NewlineNode()

    if node.contents.startswith("* "):
        return BulletNode(contents=node.contents[2:])

    if node.contents.startswith("<"):
        return HtmlNode(contents=node.contents)

    if re.match(r"^\d+\. ", node.contents):
        item = node.contents

        return NumListNode(contents=item[item.index(" ") + 1 :])

    if node.contents.startswith("- [ ] "):
        return CheckboxNode(checked=False, contents=node.contents[6:])

    if node.contents.startswith("- [x] "):
        return CheckboxNode(checked=True, contents=node.contents[6:])

    if node.contents == "---":
        return DividerNode()

    return TextNode(contents=node.contents)


def classify_nodes(nodes: list[Node]) -> list[Node]:
    return [classify_node(node) for node in nodes]


def group_text_nodes(nodes: list[Node]) -> list[Node]:
    done: list[Node] = []

    for node in nodes:
        if isinstance(node, TextNode):
            if len(done) == 0 or not isinstance(done[-1], TextNode):
                done.append(node)

            else:
                done[-1].contents += f"\n{node.contents}"

        else:
            done.append(node)

    return done


def group_bullet_nodes(nodes: list[Node]) -> list[Node]:
    done: list[Node] = []

    for node in nodes:
        if isinstance(node, BulletNode):
            if len(done) == 0 or not isinstance(done[-1], BulletNode):
                done.append(BulletNode(data=[node.contents]))

            else:
                done[-1].data.append(node.contents)

        else:
            done.append(node)

    return done


def group_number_list_nodes(nodes: list[Node]) -> list[Node]:
    done: list[Node] = []

    for node in nodes:
        if isinstance(node, NumListNode):
            if len(done) == 0 or not isinstance(done[-1], NumListNode):
                done.append(NumListNode(data=[node.contents]))

            else:
                done[-1].data.append(node.contents)

        else:
            done.append(node)

    return done


def expand_links(html: str) -> str:
    md_url_regex = r"\[([^[\]]*)\]\(([^()]*)\)"
    a_tag_regex = r'<a href="\2">\1</a>'

    return re.sub(md_url_regex, a_tag_regex, html)


def expand_footnode_ref(html: str) -> str:
    md_footnote_ref_regex = r"\[\^(\d+)\]([^:]|$)"
    a_tag_regex = r'<a id="footnote-ref-\1" href="#footnote-\1">[\1]</a>\2'

    return re.sub(md_footnote_ref_regex, a_tag_regex, html)


def expand_footnote(html: str) -> str:
    md_footnote_regex = r"\[\^(\d+)\]:"
    a_tag_regex = r'<a id="footnote-\1" href="#footnote-ref-\1">[\1]</a>:'

    return re.sub(md_footnote_regex, a_tag_regex, html)


def expand_bold(html: str) -> str:
    md_bold_regex = r"\*\*([^[\*]+)\*\*"
    bold_regex = r"<strong>\1</strong>"

    return re.sub(md_bold_regex, bold_regex, html)


def expand_strikethrough(html: str) -> str:
    md_strike_regex = r"~~([^~]+)~~"
    strike_regex = r"<s>\1</s>"

    return re.sub(md_strike_regex, strike_regex, html)


def expand_italics(html: str) -> str:
    md_italics_regex = r"\*([^[\*]+)\*"
    italics_regex = r"<em>\1</em>"

    return re.sub(md_italics_regex, italics_regex, html)


def expand_code(html: str) -> str:
    md_code_regex = r"`([^`]+)`"
    code_regex = r'<code class="hljs">\1</code>'

    return re.sub(md_code_regex, code_regex, html)


def expand_inline(line: str) -> str:
    return pipe(
        line,
        expand_footnode_ref,
        expand_footnote,
        expand_links,
        expand_strikethrough,
        expand_bold,
        expand_italics,
        expand_code,
    )


def escape_node(node: Node) -> None:
    match node:
        case HtmlNode() | PythonNode():
            pass

        case CodeblockNode(contents=contents, language=""):
            node.contents = escape(contents)

        case CodeblockNode(language=_):
            pass

        case ListNode(data=data):
            for i, item in enumerate(data):
                data[i] = escape(item)

        case TableNode(header=header, rows=rows):
            for i, cell in enumerate(header):
                header[i].name = escape(cell.name)

            for i, row in enumerate(rows):
                rows[i] = [escape(cell) for cell in row]

        case _:
            node.contents = escape(node.contents)


def escape_nodes(nodes: list[Node]) -> None:
    for node in nodes:
        escape_node(node)


def expand_node(node: Node) -> None:
    match node:
        case CodeblockNode():
            pass

        case TableNode(header=header, rows=rows):
            for i, cell in enumerate(header):
                header[i].name = expand_inline(cell.name)

            for i, row in enumerate(rows):
                rows[i] = [expand_inline(cell) for cell in row]

        case ListNode(data=rows):
            for i, item in enumerate(rows):
                rows[i] = expand_inline(item)

        case _:
            node.contents = expand_inline(node.contents)


def expand_nodes(nodes: list[Node]) -> None:
    for node in nodes:
        expand_node(node)


def run_python_block(code: str) -> str:
    html = ""

    _locals = locals()
    exec(code, globals(), _locals)

    return _locals["html"]  # type: ignore


def hightlight_code(code: str, language: str) -> str:
    pipe = run(
        ["node", "highlighter/index.js", language],
        capture_output=True,
        input=code.encode(),
    )

    if pipe.returncode != 0:
        raise ChildProcessError(
            f"""\
Code could not be highlighted. This could be for a number of reasons:
* The language "{language}" was not recognized
* Node is not installed
* You didn't run "npm install" in highlighter folder
* index.js was not found
"""
        )

    return pipe.stdout.decode()


def rows_to_list_items(rows: list[str]) -> str:
    return "\n".join([f"<li>{row}</li>" for row in rows])


def convert_node(node: Node) -> str:
    match node:
        case CommentNode():
            return ""

        case HeaderNode(contents=line, level=level):
            return f"<h{level}>{line}</h{level}>"

        case TextNode(contents=line):
            return f"<p>{line}</p>"

        case NewlineNode():
            return "<br>"

        case HtmlNode(contents=line):
            return line

        case BlockquoteNode(contents=line):
            return f"<blockquote>{line}</blockquote>"

        case CheckboxNode(checked=True, contents=line):
            return f'<p><input type="checkbox" checked>{line}</p>'

        case CheckboxNode(checked=False, contents=line):
            return f'<p><input type="checkbox">{line}</p>'

        case BulletNode(data=rows):
            return f"<ul>\n{rows_to_list_items(rows)}\n</ul>"

        case NumListNode(data=rows):
            return f"<ol>\n{rows_to_list_items(rows)}\n</ol>"

        case PythonNode(contents=code):
            return run_python_block(code)

        case CodeblockNode(contents=code, language=language):
            escaped = code.replace("\\", "\\\\")

            return (
                hightlight_code(escaped, language)
                if language
                else f'<pre class="hljs">{escaped}</pre>'
            )

        case TableNode(header=header, rows=rows):
            alignment_to_style = {
                HeaderAlignment.DEFAULT: "",
                HeaderAlignment.LEFT: ' style="text-align: left;"',
                HeaderAlignment.CENTER: ' style="text-align: center;"',
                HeaderAlignment.RIGHT: ' style="text-align: right;"',
            }

            def make_row(cells: list[str], type: str) -> str:
                def get_style(i: int) -> str:
                    return alignment_to_style[header[i].alignment]

                row = [
                    f"<{type}{get_style(i)}>{text}</{type}>"
                    for i, text in enumerate(cells)
                ]

                return f"<tr>{''.join(row)}</tr>"

            table_rows = [make_row([cell.name for cell in node.header], "th")]
            table_rows.extend([make_row(row, "td") for row in rows])

            return f"<table>{''.join(table_rows)}</table>"

        case DividerNode():
            return "<hr>"

    assert False  # pragma: no cover


def setup_nodes(md: str) -> list[Node]:
    lines = md.split("\n")
    return [Node(contents=line) for line in lines]


def markdown_to_html(md: str) -> str:
    nodes = setup_nodes(md)
    nodes = group_blocked_nodes(iter(nodes))
    nodes = classify_nodes(nodes)
    nodes = group_text_nodes(nodes)
    nodes = group_bullet_nodes(nodes)
    nodes = group_number_list_nodes(nodes)
    escape_nodes(nodes)
    expand_nodes(nodes)

    return "\n".join([convert_node(node) for node in nodes])


def get_title(md: str) -> str:
    return md.split("\n")[0][2:]


# TODO(dosisod): The "core" logic should not concern itself with GitHub, move
# it elsewhere
def add_github_commenting(html: str, filename: str) -> str:
    github_comment_code = """\
<hr>

<script src="https://utteranc.es/client.js"
  repo="dosisod/dosisod.github.io"
  issue-term="title"
  theme="gruvbox-dark"
  crossorigin="anonymous"
  async>
</script>

<noscript>
  <br>
  <em>
    Comment with GitHub functionality is
    disabled when JavaScript is turned off.
  </em>
</noscript>
"""

    return re.sub(
        "GITHUB_COMMENT",
        "" if "index.md" in filename else github_comment_code,
        html,
    )


def convert_file(filename: str) -> None:
    file = Path(filename)

    markdown = file.read_text()
    content = markdown_to_html(markdown)

    template = Path("./index.template.html").read_text()
    template = re.sub("TITLE", get_title(markdown), template)

    html = re.sub("MAIN_CONTENT", content, template)
    html = add_github_commenting(html, filename)

    with file.with_suffix(".html").open("w+") as f:
        f.write(html)


def main(argv: list[str]) -> None:
    if len(argv) < 2:
        print(f"usage: {argv[0]} <file.md> [...files.md]")
        return

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(convert_file, filename) for filename in argv[1:]
        ]

        for future in futures:
            if ex := future.exception():
                raise ex
