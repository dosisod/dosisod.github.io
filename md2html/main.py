from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re

from .node import *
from .core import markdown_to_nodes, get_title
from .html import markdown_to_html


def add_github_commenting(nodes: list[Node], filename: str) -> None:
    if filename in ("index.md", "404.md"):
        return

    github_comment_code = """\
<hr>

<script src="https://utteranc.es/client.js"
  repo="dosisod/dosisod.github.io"
  issue-term="title"
  theme="github-light"
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

    nodes.append(HtmlNode(contents=github_comment_code))


def convert_file(filename: str) -> None:
    file = Path(filename)

    markdown = file.read_text()
    nodes = markdown_to_nodes(markdown)
    add_github_commenting(nodes, file.name)

    html = markdown_to_html(nodes)

    template = Path("./index.template.html").read_text()
    template = re.sub("TITLE", get_title(nodes), template)

    html = re.sub("MAIN_CONTENT", html, template)

    file.with_suffix(".html").write_text(html)


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
