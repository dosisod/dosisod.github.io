from concurrent.futures import ThreadPoolExecutor
from html import escape
from pathlib import Path
from subprocess import run
from typing import List, Tuple, Iterator, Optional
import re

from .node import *


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
            return CodeblockNode(data=[lang, codeblock])

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
) -> Tuple[Node, Optional[Node]]:
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
) -> Tuple[Node, Optional[Node]]:
    def split_row(row: str) -> List[str]:
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

    rows: List[List[str]] = []

    while node := next(nodes, None):
        if not is_valid_table_row(node.contents):
            return (TableNode(header=header, rows=rows), node)

        rows.append(split_row(node.contents))

    return (TableNode(header=header, rows=rows), None)


def group_blocked_nodes(nodes: Iterator[Node]) -> List[Node]:
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

    return TextNode(contents=node.contents)


def classify_nodes(nodes: List[Node]) -> List[Node]:
    return [classify_node(node) for node in nodes]


def group_text_nodes(nodes: List[Node]) -> List[Node]:
    done: List[Node] = []

    for node in nodes:
        if isinstance(node, TextNode):
            if len(done) == 0 or not isinstance(done[-1], TextNode):
                done.append(node)

            else:
                done[-1].contents += f"\n{node.contents}"

        else:
            done.append(node)

    return done


def group_bullet_nodes(nodes: List[Node]) -> List[Node]:
    done: List[Node] = []

    for node in nodes:
        if isinstance(node, BulletNode):
            if len(done) == 0 or not isinstance(done[-1], BulletNode):
                done.append(BulletNode(data=[node.contents]))

            else:
                done[-1].data.append(node.contents)

        else:
            done.append(node)

    return done


def group_number_list_nodes(nodes: List[Node]) -> List[Node]:
    done: List[Node] = []

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
    md_url_regex = r"\[(\S*)\]\((\S*)\)"
    a_tag_regex = r'<a href="\2">\1</a>'

    return re.sub(md_url_regex, a_tag_regex, html)


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
    return expand_code(
        expand_italics(expand_bold(expand_strikethrough(expand_links(line))))
    )


def escape_nodes(nodes: List[Node]) -> None:
    for node in nodes:
        if isinstance(node, (HtmlNode, PythonNode)):
            pass

        elif isinstance(node, DataNode):
            if isinstance(node, CodeblockNode) and not node.data[0]:
                node.data[1] = escape(node.data[1])

            elif isinstance(node, ListNode):
                for i, item in enumerate(node.data):
                    node.data[i] = escape(item)

        elif isinstance(node, TableNode):
            for i, cell in enumerate(node.header):
                node.header[i].name = escape(cell.name)

            for i, row in enumerate(node.rows):
                node.rows[i] = [escape(cell) for cell in row]

        else:
            node.contents = escape(node.contents)


def expand_nodes(nodes: List[Node]) -> None:
    for node in nodes:
        if isinstance(node, ListNode) and isinstance(node, DataNode):
            for i, item in enumerate(node.data):
                node.data[i] = expand_inline(item)

        elif isinstance(node, TableNode):
            for i, cell in enumerate(node.header):
                node.header[i].name = expand_inline(cell.name)

            for i, row in enumerate(node.rows):
                node.rows[i] = [expand_inline(cell) for cell in row]

        elif not isinstance(node, CodeblockNode):
            node.contents = expand_inline(node.contents)


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


def convert_node(node: Node) -> str:
    line = node.contents

    if isinstance(node, CommentNode):
        return ""

    if isinstance(node, HeaderNode):
        return f"<h{node.level}>{line}</h{node.level}>"

    elif isinstance(node, TextNode):
        return f"<p>{line}</p>"

    elif isinstance(node, NewlineNode):
        return "<br>"

    elif isinstance(node, HtmlNode):
        return line

    elif isinstance(node, BlockquoteNode):
        return f"<blockquote>{line}</blockquote>"

    elif isinstance(node, CheckboxNode):
        checked = " checked" if node.checked else ""

        return f'<p><input type="checkbox"{checked}>{line}</p>'

    elif isinstance(node, BulletNode):
        items = "\n".join([f"<li>{x}</li>" for x in node.data])

        return f"<ul>\n{items}\n</ul>"

    elif isinstance(node, NumListNode):
        items = "\n".join([f"<li>{x}</li>" for x in node.data])

        return f"<ol>\n{items}\n</ol>"

    elif isinstance(node, PythonNode):
        return run_python_block(line)

    elif isinstance(node, CodeblockNode):
        lang = node.data[0]
        code = node.data[1]

        if lang:
            escaped = code.replace("\\", "\\\\")

            return hightlight_code(escaped, lang)

        else:
            return f'<pre class="hljs">{code}</pre>'

    elif isinstance(node, TableNode):
        alignment_to_style = {
            HeaderAlignment.DEFAULT: "",
            HeaderAlignment.LEFT: ' style="text-align: left;"',
            HeaderAlignment.CENTER: ' style="text-align: center;"',
            HeaderAlignment.RIGHT: ' style="text-align: right;"',
        }

        table_node = node

        def make_row(cells: List[str], type: str, style: str = "") -> str:
            def get_style(i: int) -> str:
                return alignment_to_style[table_node.header[i].alignment]

            row = [
                f"<{type}{get_style(i)}>{text}</{type}>"
                for i, text in enumerate(cells)
            ]

            return f"<tr>{''.join(row)}</tr>"

        rows = [make_row([cell.name for cell in node.header], "th")]
        rows.extend([make_row(row, "td") for row in node.rows])

        return f"<table>{''.join(rows)}</table>"

    assert False  # pragma: no cover


def setup_nodes(md: str) -> List[Node]:
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


def convert_file(filename: str) -> None:
    file = Path(filename)

    markdown = file.read_text()
    content = markdown_to_html(markdown)

    template = Path("./index.template.html").read_text()
    template = re.sub("TITLE", get_title(markdown), template)

    html = re.sub("MAIN_CONTENT", content, template)

    with file.with_suffix(".html").open("w+") as f:
        f.write(html)


def main(argv: List[str]) -> None:
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
