from enum import Enum, auto
from pathlib import Path
from subprocess import run
from typing import List, Tuple
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
    BLOCKQUOTE = auto()
    CHECKBOX_UNCHECKED = auto()
    CHECKBOX_CHECKED = auto()
    CODE_BLOCK = auto()

    @classmethod
    def is_list_item(cls, type: "NodeType") -> bool:
        return type in (cls.BULLET_ITEM, cls.NUMBERED_ITEM)


class Node:
    type: NodeType
    data: str

    def __init__(self, type: NodeType, data: str) -> None:
        self.type = type
        self.data = data

    def __eq__(self, o) -> bool:
        return self.type == o.type and self.data == o.data


def run_python_block(code: str) -> str:
    html = ""

    _locals = locals()
    exec(code, globals(), _locals)

    return _locals["html"]


def line_to_node(line: str) -> Node:
    if line.startswith("# "):
        return Node(NodeType.HEADER_1, line[2:])

    if line.startswith("## "):
        return Node(NodeType.HEADER_2, line[3:])

    if line.startswith("### "):
        return Node(NodeType.HEADER_3, line[4:])

    if line.startswith("#### "):
        return Node(NodeType.HEADER_4, line[5:])

    if line.startswith("* "):
        return Node(NodeType.BULLET_ITEM, line[2:])

    if re.match(r"^\d+\. ", line):
        return Node(NodeType.NUMBERED_ITEM, line[line.index(" ") + 1 :])

    if line.startswith("<"):
        return Node(NodeType.RAW_HTML, line)

    if line == "":
        return Node(NodeType.NEWLINE, "")

    if line == "!!!":
        return Node(NodeType.RAW_PYTHON, "")

    if line.startswith("```"):
        return Node(NodeType.CODE_BLOCK, line[3:])

    if line.startswith("> "):
        return Node(NodeType.BLOCKQUOTE, line[2:])

    if line.startswith("- [ ] "):
        return Node(NodeType.CHECKBOX_UNCHECKED, line[6:])

    if line.startswith("- [x] "):
        return Node(NodeType.CHECKBOX_CHECKED, line[6:])

    return Node(NodeType.TEXT, line)


def categorize(lines: List[str]) -> List[Node]:
    return [line_to_node(line) for line in lines]


class ParserContext:
    html = ""

    in_bullet_list = False
    in_number_list = False

    in_python_block = False
    python_block = ""

    in_code_block = False
    code_block = ""

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


def parse_list_item(ctx: ParserContext, type: NodeType, line: str) -> None:
    start_list_if_needed(ctx, type)

    ctx.html += f"<li>{expand_inline(line)}</li>\n"


def parse_python_block(ctx: ParserContext, type: NodeType, line: str) -> None:
    if type == NodeType.RAW_PYTHON:
        ctx.html += run_python_block(ctx.python_block)

        ctx.in_python_block = False
        ctx.python_block = ""

    else:
        ctx.python_block += f"{line}\n"


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


def parse_code_block(ctx: ParserContext, type: NodeType, line: str) -> None:
    if type == NodeType.CODE_BLOCK:
        if ctx.language:
            escaped = ctx.code_block.replace("\\", "\\\\")

            ctx.html += hightlight_code(escaped, ctx.language)

        else:
            ctx.html += f'<pre class="hljs">{ctx.code_block}</pre>'

        ctx.in_code_block = False
        ctx.code_block = ""

    else:
        ctx.code_block += f"{line}\n"


def group_text_and_blockquotes(nodes: List[Node]) -> List[Node]:
    out = [nodes.pop(0)]

    for node in nodes:
        if node.type == out[-1].type and node.type in (
            NodeType.TEXT,
            NodeType.BLOCKQUOTE,
        ):
            last = out.pop()
            out.append(Node(node.type, f"{last.data}\n{node.data}"))

        else:
            out.append(node)

    return out


def convert(nodes: List[Node]) -> str:
    ctx = ParserContext()

    for node in nodes:
        type = node.type
        line = node.data

        if ctx.in_list():
            if NodeType.is_list_item(type):
                parse_list_item(ctx, type, line)

            end_list_if_needed(ctx, type)

        elif ctx.in_python_block:
            parse_python_block(ctx, type, line)

        elif ctx.in_code_block:
            parse_code_block(ctx, type, line)

        elif NodeType.is_list_item(type):
            parse_list_item(ctx, type, line)

        elif type == NodeType.RAW_PYTHON:
            ctx.in_python_block = True

        elif type == NodeType.CODE_BLOCK:
            ctx.language = line
            ctx.in_code_block = True

        elif type == NodeType.HEADER_1:
            ctx.html += f"<h1>{expand_inline(line)}</h1>\n"

        elif type == NodeType.HEADER_2:
            ctx.html += f"<h2>{expand_inline(line)}</h2>\n"

        elif type == NodeType.HEADER_3:
            ctx.html += f"<h3>{expand_inline(line)}</h3>\n"

        elif type == NodeType.HEADER_4:
            ctx.html += f"<h4>{expand_inline(line)}</h4>\n"

        elif type == NodeType.TEXT:
            ctx.html += f"<p>{expand_inline(line)}</p>\n"

        elif type == NodeType.NEWLINE:
            ctx.html += "<br>\n"

        elif type == NodeType.RAW_HTML:
            ctx.html += f"{line}\n"

        elif type == NodeType.BLOCKQUOTE:
            ctx.html += f"<blockquote>{expand_inline(line)}</blockquote>\n"

        elif type == NodeType.CHECKBOX_UNCHECKED:
            ctx.html += (
                f'<p><input type="checkbox">{expand_inline(line)}</p>\n'
            )

        elif type == NodeType.CHECKBOX_CHECKED:
            ctx.html += f'<p><input type="checkbox" checked>{expand_inline(line)}</p>\n'

    return ctx.html


def expand_links(html: str) -> str:
    md_url_regex = r"\[([^[\]]*)\]\(([^()]*)\)"
    a_tag_regex = r'<a href="\2">\1</a>'

    return re.sub(md_url_regex, a_tag_regex, html)


def expand_bold(html: str) -> str:
    md_bold_regex = r"\*\*([^[\*]+)\*\*"
    bold_regex = r"<strong>\1</strong>"

    return re.sub(md_bold_regex, bold_regex, html)


def expand_italics(html: str) -> str:
    md_italics_regex = r"\*([^[\*]+)\*"
    italics_regex = r"<em>\1</em>"

    return re.sub(md_italics_regex, italics_regex, html)


def expand_code(html: str) -> str:
    md_code_regex = r"`([^`]+)`"
    code_regex = r'<code class="hljs">\1</code>'

    return re.sub(md_code_regex, code_regex, html)


def expand_inline(line: str) -> str:
    return expand_code(expand_italics(expand_bold(expand_links(line))))


def run_pipeline(markdown: str) -> str:
    nodes = categorize(markdown.split("\n"))
    nodes = group_text_and_blockquotes(nodes)

    return convert(nodes)


def convert_file(filename: str) -> None:
    file = Path(filename)

    markdown = file.read_text()
    content = run_pipeline(markdown)

    template = Path("./index.template.html").read_text()
    template = re.sub("TITLE", file.stem, template)

    html = re.sub("MAIN_CONTENT", content, template)

    with file.with_suffix(".html").open("w+") as f:
        f.write(html)


def main(argv: List[str]):
    if len(argv) == 2:
        convert_file(argv[1])

    else:
        print(f"usage: {argv[0]} <file.md>")
