from datetime import datetime
from pathlib import Path
import re

from git import Repo
from git.exc import GitCommandError

from md2html.core import get_title

def gen_recent_blogs() -> str:
    repo = Repo()

    commits = repo.iter_commits('HEAD')

    html = "<ul>"

    for commit in commits:
        blobs = commit.tree.blobs

        try:
            def get_changes(type):
                return [
                    (type, change)
                    for change
                    in commit.diff(f"{commit}~1").iter_change_type(type)
                ]

            # Compare current commit with last commit. This will mean that
            # the "added" files will actually show as "deleted", hence
            # the "D" argument.
            added = get_changes("D")
            renamed = get_changes("R")

            changes = added + renamed

        except GitCommandError:
            # Probably means we hit the initial commit
            continue

        for change_type, change in changes:
            filename = change.a_path if change_type == "R" else change.b_path

            if re.match(f"blog.*md", filename):
                date = commit.authored_datetime

                if change_type == "R":
                    date = list(repo.iter_commits(
                        "HEAD", change.b_path
                    ))[-1].authored_datetime

                path = Path(filename)

                if not path.exists():
                    continue

                with path.open() as f:
                    # Assumes title is in the form "# header", and on the
                    # first line. This should be changed at some point.
                    title = get_title(f.readline())

                html += f'''
  <li>
    <span>
      <span class="gray">{date.strftime('%b %e %Y')}</span>
      <a href="./{path.with_suffix('.html')}">{title}</a>
    </span>
  </li>'''

    html += "\n</ul>"

    return html

def gen_updated_date() -> str:
    # From: https://stackoverflow.com/a/52045942
    def day_suffix(day):
        suffixes = ["th", "st", "nd", "rd"]

        if day % 10 in [1, 2, 3] and day not in [11, 12, 13]:
            return sufixes[day % 10]

        return suffixes[0]

    now = datetime.now()
    return now.strftime('%B %dXXX %Y').replace("XXX", day_suffix(now.day))
