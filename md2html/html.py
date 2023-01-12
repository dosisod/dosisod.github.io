from html import escape
from subprocess import run
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


def text_to_fragment(text: str) -> str:
    mangled = re.sub("[^a-z0-9]", "-", text.lower())

    return "-".join(x for x in mangled.split("-") if x)


def convert_node(node: Node) -> str:
    match node:
        case CommentNode():
            return ""

        case HeaderNode(contents=line, level=level):
            header = f"<h{level}>{line}</h{level}>"
            fragment = text_to_fragment(line)

            return f'<a id="{fragment}" href="#{fragment}">{header}</a>'

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


def markdown_to_html(nodes: list[Node]) -> str:
    escape_nodes(nodes)
    expand_nodes(nodes)

    return "\n".join([convert_node(node) for node in nodes])
