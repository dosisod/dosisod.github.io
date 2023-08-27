from html import escape as _escape
from subprocess import run
from typing import ClassVar
import re

from .node import *
from .pipe import pipe


def expand_links(html: str) -> str:
    md_url_regex = r"\[\]\(([^()]*)\)"
    a_tag_regex = r'<a href="\1">\1</a>'

    html = re.sub(md_url_regex, a_tag_regex, html)

    md_url_regex = r"\[([^[\]]*)\]\(([^()]*)\)"
    a_tag_regex = r'<a href="\2">\1</a>'

    return re.sub(md_url_regex, a_tag_regex, html)


def expand_footnode_ref(html: str) -> str:
    md_footnote_ref_regex = r"\[\^(\d+)\]"
    a_tag_regex = r'<a id="footnote-ref-\1" href="#footnote-\1">[\1]</a>'

    return re.sub(md_footnote_ref_regex, a_tag_regex, html)


def expand_footnote(html: str) -> str:
    md_footnote_regex = r"^\[\^(\d+)\]:"
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
        expand_footnote,
        expand_footnode_ref,
        expand_links,
        expand_strikethrough,
        expand_bold,
        expand_italics,
        expand_code,
    )


def escape(s: str) -> str:
    # unescape markdown underscore escapes
    s = re.sub(r"\\_", "_", s)

    return _escape(s)


def run_python_block(code: str) -> str:
    html = ""

    _locals = locals()
    exec(code, globals(), _locals)  # noqa: S102

    return _locals["html"]  # type: ignore[no-any-return]


def hightlight_code(code: str, language: str) -> str:
    pipe = run(  # noqa: PLW1510
        ["node", "highlighter/index.js", language],  # noqa: S603, S607
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


def build_num_list(rows: list[str]) -> str:
    width = len(str(len(rows))) + 2

    items: list[str] = []

    for i, row in enumerate(rows, start=1):
        space = " " * (width - len(str(i)) - 1)

        items.append(f'<li i="{i}.{space}">{row}</li>')

    return "\n".join(
        [
            f'<ol style="margin-left: {width}ch">',
            *items,
            "</ol>",
        ]
    )


def text_to_fragment(text: str) -> str:
    mangled = re.sub("[^a-z0-9]", "-", text.lower())

    return "-".join(x for x in mangled.split("-") if x)


class HTMLGeneratorVisitor(NodeVisitor[str]):
    alignment_to_style: ClassVar[dict[HeaderAlignment, str]] = {
        HeaderAlignment.DEFAULT: "",
        HeaderAlignment.LEFT: ' style="text-align: left;"',
        HeaderAlignment.CENTER: ' style="text-align: center;"',
        HeaderAlignment.RIGHT: ' style="text-align: right;"',
    }

    def visit_comment_node(self, node: CommentNode) -> str:
        return ""

    def visit_bullet_list_node(self, node: BulletNode) -> str:
        rows = [expand_inline(escape(row)) for row in node.data]
        items = "\n".join(f"<li>{row}</li>" for row in rows)

        return f"<ul>\n{items}\n</ul>"

    def visit_num_list_node(self, node: NumListNode) -> str:
        rows = [expand_inline(escape(row)) for row in node.data]

        # TODO: move this logic to a custom html visitor
        return build_num_list(rows)

    def visit_checkbox_node(self, node: CheckboxNode) -> str:
        data = expand_inline(escape(node.contents))
        attr = " checked" if node.checked else ""

        return f'<p><input type="checkbox"{attr}>{data}</p>'

    def visit_text_node(self, node: TextNode) -> str:
        data = expand_inline(escape(node.contents))

        return f"<p>{data}</p>"

    def visit_codeblock_node(self, node: CodeblockNode) -> str:
        if node.language:
            escaped = node.contents.replace("\\", "\\\\")

            return hightlight_code(escaped, node.language)

        escaped = escape(node.contents).replace("\\", "\\\\")

        return f'<pre class="hljs">{escaped}</pre>'

    def visit_python_node(self, node: PythonNode) -> str:
        return run_python_block(node.contents)

    def visit_html_node(self, node: HtmlNode) -> str:
        return node.contents

    def visit_header_node(self, node: HeaderNode) -> str:
        data = expand_inline(escape(node.contents))

        heading = f"<h{node.level}>{data}</h{node.level}>"
        fragment = text_to_fragment(data)

        return f'<a id="{fragment}" href="#{fragment}">{heading}</a>'

    def visit_newline_node(self, node: NewlineNode) -> str:
        return "<br>"

    def visit_divider_node(self, node: DividerNode) -> str:
        return "<hr>"

    def visit_blockquote_node(self, node: BlockquoteNode) -> str:
        data = expand_inline(escape(node.contents))

        return f"<blockquote>{data}</blockquote>"

    def visit_table_node(self, node: TableNode) -> str:
        def get_header_style(i: int) -> str:
            return self.alignment_to_style[node.header[i].alignment]

        def make_row(cells: list[str], tag: str) -> str:
            cells = [expand_inline(escape(cell)) for cell in cells]

            row = [
                f"<{tag}{get_header_style(i)}>{cell}</{tag}>"
                for i, cell in enumerate(cells)
            ]

            return f"<tr>{''.join(row)}</tr>"

        header = [cell.name for cell in node.header]

        rows = [
            *make_row(header, "th"),
            *[make_row(row, "td") for row in node.rows],
        ]

        # TODO: add newline after each row
        return f"<table>{''.join(rows)}</table>"


def markdown_to_html(nodes: list[Node]) -> str:
    visitor = HTMLGeneratorVisitor()

    return "\n".join(node.accept(visitor) for node in nodes)
