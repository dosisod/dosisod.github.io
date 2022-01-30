from sys import argv
from typing import List, Tuple
from pathlib import Path
from enum import Enum, auto
import re

class NodeType(Enum):
    TEXT = auto()
    HEADER_1 = auto()
    HEADER_2 = auto()
    HEADER_3 = auto()
    HEADER_4 = auto()
    BULLET_ITEM = auto()
    NUMBERED_ITEM = auto()
    RAW_HTML = auto()
    RAW_PYTHON = auto()
    NEWLINE = auto()

    @classmethod
    def is_list_item(cls, type: "NodeType") -> bool:
        return type == cls.BULLET_ITEM or type == cls.NUMBERED_ITEM


def run_python_block(code: str) -> str:
    html = ""

    _locals = locals()
    exec(code, globals(), _locals)

    return _locals["html"]


def line_to_type(line: str) -> NodeType:
    if line.startswith("# "):
        return NodeType.HEADER_1

    if line.startswith("## "):
        return NodeType.HEADER_2

    if line.startswith("### "):
        return NodeType.HEADER_3

    if line.startswith("#### "):
        return NodeType.HEADER_4

    if line.startswith("*"):
        return NodeType.BULLET_ITEM

    if re.match(r"^\d+\.", line):
        return NodeType.NUMBERED_ITEM

    if line.startswith("<"):
        return NodeType.RAW_HTML

    if line == "":
        return NodeType.NEWLINE

    if line == "!!!":
        return NodeType.RAW_PYTHON

    return NodeType.TEXT


def categorize(lines: List[str]) -> List[Tuple[NodeType, str]]:
    return [((line_to_type(line), line)) for line in lines]


class ParserContext:
    html = ""

    in_bullet_list = False
    in_number_list = False

    in_python_block = False
    python_block = ""

    def in_list(self) -> bool:
        return self.in_bullet_list or self.in_number_list


def start_list_if_needed(ctx: ParserContext, type: NodeType) -> None:
    if ctx.in_list():
        return

    if type == NodeType.BULLET_ITEM:
        ctx.html += "<ul>\n"
        ctx.in_bullet_list = True

    else:
        ctx.html += "<ol>\n"
        ctx.in_number_list = True


def end_list_if_needed(ctx: ParserContext, type: NodeType) -> None:
    if not NodeType.is_list_item(type):
        if ctx.in_bullet_list:
            ctx.html += "</ul>\n"

        else:
            ctx.html += "</ol>\n"

        ctx.in_bullet_list = False
        ctx.in_number_list = False


def end_python_block_if_needed(ctx: ParserContext) -> None:
    if not ctx.in_python_block:
        ctx.in_python_block = True


def parse_list_item(ctx: ParserContext, type: NodeType, line: str) -> None:
    start_list_if_needed(ctx, type)

    ctx.html += f"<li>{line[line.index(' ') + 1:]}</li>\n"


def parse_python_block(ctx: ParserContext, type: NodeType, line: str) -> None:
    if type == NodeType.RAW_PYTHON:
        ctx.html += run_python_block(ctx.python_block)

        ctx.in_python_block = False
        ctx.python_block = ""

    else:
        ctx.python_block += f"{line}\n"


def convert(lines: List[Tuple[NodeType, str]]) -> str:
    ctx = ParserContext()

    for type, line in lines:
        if ctx.in_list():
            if NodeType.is_list_item(type):
                parse_list_item(ctx, type, line)

            end_list_if_needed(ctx, type)

        elif ctx.in_python_block:
            parse_python_block(ctx, type, line)

        elif NodeType.is_list_item(type):
            parse_list_item(ctx, type, line)

        elif type == NodeType.RAW_PYTHON:
            end_python_block_if_needed(ctx)

        elif type == NodeType.HEADER_1:
            ctx.html += f"<h1>{line[2:]}</h1><br>\n"

        elif type == NodeType.HEADER_2:
            ctx.html += f"<h2>{line[3:]}</h2><br>\n"

        elif type == NodeType.HEADER_3:
            ctx.html += f"<h3>{line[4:]}</h3><br>\n"

        elif type == NodeType.HEADER_4:
            ctx.html += f"<h4>{line[5:]}</h4><br>\n"

        elif type == NodeType.TEXT:
            ctx.html += f"<p>{line}</p>\n"

        elif type == NodeType.NEWLINE:
            ctx.html += "<br>\n"

        elif type == NodeType.RAW_HTML:
            ctx.html += f"{line}\n"

    return ctx.html


def expand_links(html: str) -> str:
    md_url_regex = r"\[([^[\]]*)\]\(([^()]*)\)"
    a_tag_regex = r'<a href="\2">\1</a>'

    return re.sub(md_url_regex, a_tag_regex, html)


def main():
    if len(argv) != 2:
        print(f"usage: {argv[0]} <file.md>")
        return

    file = Path(argv[1])

    markdown = file.read_text()
    lines = markdown.split("\n")
    content = expand_links(convert(categorize(lines)))

    # to have style sheet referenced correctly, we need to add an
    # appropriate amount of folder back-tracking
    nested_dir_count = len(file.parts) - 1
    path_prefix = "/".join([".." * nested_dir_count]) or "."

    template = Path("./index.template.html").read_text()
    template = re.sub("PATH_PREFIX", path_prefix, template)
    template = re.sub("TITLE", file.stem, template)

    html = re.sub("MAIN_CONTENT", content, template)

    with file.with_suffix(".html").open("w+") as f:
        f.write(html)


if __name__ == "__main__":
    main()
