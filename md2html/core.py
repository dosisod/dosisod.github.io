from collections.abc import Iterator
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

        code += f"\n{node.contents}"

    raise ValueError("python block end not reached")


def iter_block_quote(
    first: Node, nodes: Iterator[Node]
) -> tuple[Node, Node | None]:
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

        comment += f"\n{node.contents}"

    raise ValueError("html comment not closed")


def iter_table(first: Node, nodes: Iterator[Node]) -> tuple[Node, Node | None]:
    def split_row(row: str) -> list[str]:
        return [x.strip() for x in row.split("|")[1:-1]]

    separator_node = next(nodes, None)

    if not separator_node:
        raise ValueError("table missing required header separator")

    if not is_valid_table_row(separator_node.contents):
        raise ValueError("line must start and end with pipe")

    separator_cells = split_row(separator_node.contents)

    def is_valid_separator_cell(cell: str) -> bool:
        return bool(re.match("^:?-{3,}:?$", cell.strip()))

    if not all(is_valid_separator_cell(x) for x in separator_cells):
        raise ValueError(
            "header separator must have:\n\n"
            "* At least 3 dashes\n"
            "* (optional) starting/ending ':'\n"
            "* (optional) whitespace at start/end\n"
        )

    header = [HeaderCell(name) for name in split_row(first.contents)]

    if len(separator_cells) != len(header):
        raise ValueError(
            f"expected {len(header)} cells, got {len(separator_cells)} instead"
        )

    for i, name in enumerate(separator_cells):
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


def group_blocked_nodes(nodes: list[Node]) -> list[Node]:
    grouped_nodes = []
    nodes = iter(nodes)

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


def classify_node(node: Node) -> Node:
    if node.is_classified():
        return node

    if node.contents.startswith("# "):
        return HeaderNode(level=1, contents=node.contents[2:])

    if node.contents.startswith("## "):
        return HeaderNode(level=2, contents=node.contents[3:])

    if node.contents.startswith("### "):
        return HeaderNode(level=3, contents=node.contents[4:])

    if node.contents.startswith("#### "):
        return HeaderNode(level=4, contents=node.contents[5:])

    if not node.contents:
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
    groups: list[Node] = []

    for node in nodes:
        if isinstance(node, TextNode):
            if not groups or not isinstance(groups[-1], TextNode):
                groups.append(node)

            else:
                groups[-1].contents += f"\n{node.contents}"

        else:
            groups.append(node)

    return groups


def group_bullet_nodes(nodes: list[Node]) -> list[Node]:
    groups: list[Node] = []

    for node in nodes:
        if isinstance(node, BulletNode):
            if not groups or not isinstance(groups[-1], BulletNode):
                groups.append(BulletNode(data=[node.contents]))

            else:
                groups[-1].data.append(node.contents)

        else:
            groups.append(node)

    return groups


def group_number_list_nodes(nodes: list[Node]) -> list[Node]:
    groups: list[Node] = []

    for node in nodes:
        if isinstance(node, NumListNode):
            if not groups or not isinstance(groups[-1], NumListNode):
                groups.append(NumListNode(data=[node.contents]))

            else:
                groups[-1].data.append(node.contents)

        else:
            groups.append(node)

    return groups


def setup_nodes(markdown: str) -> list[Node]:
    return [Node(contents=line) for line in markdown.splitlines()]


def markdown_to_nodes(markdown: str) -> list[Node]:
    return pipe(
        setup_nodes(markdown),
        group_blocked_nodes,
        classify_nodes,
        group_text_nodes,
        group_bullet_nodes,
        group_number_list_nodes,
    )


def get_title(nodes: list[Node]) -> str:
    for node in nodes:
        match node:
            case HeaderNode(level=1, contents=contents):
                return contents

    raise ValueError("missing title")
