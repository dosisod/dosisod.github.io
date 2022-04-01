from dataclasses import dataclass, field
from html import escape
from pathlib import Path
from subprocess import run
from sys import argv
from typing import List, Tuple, Iterator, Optional
import re


@dataclass
class Node:
    type: str
    contents: str = ""
    data: List[str] = field(default_factory=list)


def group_blocked_nodes(nodes: Iterator[Node]) -> List[Node]:
    def iter_code_block(first: Node, nodes: Iterator[Node]) -> Node:
        lang = first.contents[3:]
        next_node = next(nodes, None)

        if not next_node:
            raise ValueError("codeblock end not reached")

        codeblock = next_node.contents

        for node in nodes:
            if node.contents.startswith("```"):
                return Node("CODEBLOCK", data=[lang, codeblock])

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
                return Node("PYTHON_BLOCK", code)

            else:
                code += f"\n{node.contents}"

        raise ValueError("python block end not reached")

    def iter_block_quote(
        first: Node, nodes: Iterator[Node]
    ) -> Tuple[Node, Node]:
        blockquote = first.contents[2:]

        for node in nodes:
            if not node.contents.startswith("> "):
                return (Node("BLOCKQUOTE", blockquote), node)

            blockquote += f"\n{node.contents[2:]}"

        return (Node("BLOCKQUOTE", blockquote), None)

    def iter_html_comment(first: Node, nodes: Iterator[Node]) -> Node:
        if first.contents.endswith("-->"):
            return Node("COMMENT", first.contents[4:-3])

        comment = first.contents[4:]

        for node in nodes:
            if node.contents.endswith("-->"):
                comment += f"\n{node.contents[:-3]}"
                next(nodes)
                return Node("COMMENT", comment)

            else:
                comment += f"\n{node.contents}"

        raise ValueError("html comment not closed")

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

        else:
            grouped_nodes.append(node)

    return grouped_nodes


def classify_node(node: Node) -> None:
    if node.type in ("PYTHON_BLOCK", "CODEBLOCK", "BLOCKQUOTE"):
        pass

    elif node.contents.startswith("# "):
        node.type = "HEADER1"
        node.contents = node.contents[2:]

    elif node.contents.startswith("## "):
        node.type = "HEADER2"
        node.contents = node.contents[3:]

    elif node.contents.startswith("### "):
        node.type = "HEADER3"
        node.contents = node.contents[4:]

    elif node.contents.startswith("#### "):
        node.type = "HEADER4"
        node.contents = node.contents[5:]

    elif node.contents == "":
        node.type = "NEWLINE"

    elif node.contents.startswith("* "):
        node.type = "BULLET"
        node.contents = node.contents[2:]

    elif node.contents.startswith("<"):
        node.type = "HTML"

    elif re.match(r"^\d+\. ", node.contents):
        node.type = "NUM_LIST"
        node.contents = node.contents[node.contents.index(" ") + 1 :]

    elif node.contents.startswith("- [ ] "):
        node.type = "CHECKBOX_UNCHECKED"
        node.contents = node.contents[6:]

    elif node.contents.startswith("- [x] "):
        node.type = "CHECKBOX_CHECKED"
        node.contents = node.contents[6:]

    else:
        node.type = "TEXT"


def classify_nodes(nodes: List[Node]) -> None:
    for node in nodes:
        classify_node(node)


def group_text_nodes(nodes: List[Node]) -> List[Node]:
    done: List[Node] = []

    for node in nodes:
        if node.type == "TEXT":
            if len(done) == 0 or done[-1].type != "TEXT":
                done.append(node)

            else:
                done[-1].contents += f"\n{node.contents}"

        else:
            done.append(node)

    return done


def group_bullet_nodes(nodes: List[Node]) -> List[Node]:
    done: List[Node] = []

    for node in nodes:
        if node.type == "BULLET":
            if len(done) == 0 or done[-1].type != "BULLET":
                done.append(Node(node.type, data=[node.contents]))

            else:
                done[-1].data.append(node.contents)

        else:
            done.append(node)

    return done


def group_number_list_nodes(nodes: List[Node]) -> List[Node]:
    done: List[Node] = []

    for node in nodes:
        if node.type == "NUM_LIST":
            if len(done) == 0 or done[-1].type != "NUM_LIST":
                done.append(Node(node.type, data=[node.contents]))

            else:
                done[-1].data.append(node.contents)

        else:
            done.append(node)

    return done


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


def escape_nodes(nodes: List[Node]) -> None:
    for node in nodes:
        if node.type in ("PYTHON_BLOCK", "HTML"):
            pass

        elif node.type == "CODEBLOCK" and not node.data[0]:
            node.data[1] = escape(node.data[1])

        elif node.type in ("BULLET", "NUM_LIST"):
            for i, item in enumerate(node.data):
                node.data[i] = escape(item)

        else:
            node.contents = escape(node.contents)


def expand_nodes(nodes: List[Node]) -> None:
    for node in nodes:
        if node.type in ("BULLET", "NUM_LIST"):
            for i, item in enumerate(node.data):
                node.data[i] = expand_inline(item)

        elif node.type != "CODEBLOCK":
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
    type = node.type
    line = node.contents

    if type == "HEADER1":
        return f"<h1>{line}</h1>"

    elif type == "HEADER2":
        return f"<h2>{line}</h2>"

    elif type == "HEADER3":
        return f"<h3>{line}</h3>"

    elif type == "HEADER4":
        return f"<h4>{line}</h4>"

    elif type == "TEXT":
        return f"<p>{line}</p>"

    elif type == "NEWLINE":
        return "<br>"

    elif type == "HTML":
        return line

    elif type == "BLOCKQUOTE":
        return f"<blockquote>{line}</blockquote>"

    elif type == "CHECKBOX_UNCHECKED":
        return f'<p><input type="checkbox">{line}</p>'

    elif type == "CHECKBOX_CHECKED":
        return f'<p><input type="checkbox" checked>{line}</p>'

    elif type == "BULLET":
        items = "\n".join([f"<li>{l}</li>" for l in node.data])

        return f"<ul>\n{items}\n</ul>"

    elif type == "NUM_LIST":
        items = "\n".join([f"<li>{l}</li>" for l in node.data])

        return f"<ol>\n{items}\n</ol>"

    elif type == "PYTHON_BLOCK":
        return escape(run_python_block(line))

    elif type == "CODEBLOCK":
        lang = node.data[0]
        code = node.data[1]

        if lang:
            escaped = code.replace("\\", "\\\\")

            return hightlight_code(escaped, lang)

        else:
            return f'<pre class="hljs">{code}</pre>'

    assert False  # pragma: no cover


def setup_nodes(md: str) -> List[Node]:
    lines = md.split("\n")
    return [Node("UNKNOWN", line) for line in lines]


def markdown_to_html(md: str) -> str:
    nodes = setup_nodes(md)
    nodes = group_blocked_nodes(iter(nodes))
    classify_nodes(nodes)
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


def main(argv: List[str]):
    if len(argv) < 2:
        print(f"usage: {argv[0]} <file.md> [...files.md]")

    else:
        for filename in argv[1:]:
            convert_file(filename)
