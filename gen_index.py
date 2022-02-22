from pathlib import Path
import re

from git import Repo
from git.exc import GitCommandError

def gen_recent_blogs() -> str:
    repo = Repo()

    commits = repo.iter_commits('master')

    html = "<ul>"

    for commit in commits:
        blobs = commit.tree.blobs

        try:
            # Compare current commit with last commit. This will mean that
            # the "added" files will actually show as "deleted", hence
            # the "D" argument.
            changes = commit.diff(str(commit) + "~1").iter_change_type('D')

        except GitCommandError:
            # Probably means we hit the initial commit
            continue

        for change in changes:
            if re.match(f"blog.*md", change.b_path):
                file = change.b_path
                date = commit.authored_datetime

                path = Path(file)

                with path.open() as f:
                    # Assumes title is in the form "# header", and on the
                    # first line. This should be changed at some point.
                    title = f.readline()[2:-1]

                html += f'''
  <li>
    <span>
      <span class="gray">{date.strftime('%b %e %Y')}</span>
      <a href="./{path.with_suffix('.html')}">{title}</a>
    </span>
  </li>'''

    html += "\n</ul>"

    return html
