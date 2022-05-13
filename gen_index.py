from datetime import datetime
from pathlib import Path
from typing import List, NamedTuple
import re

from git import Repo
from git.exc import GitCommandError

from md2html.core import get_title


repo = Repo()


class Entry(NamedTuple):
    date: datetime
    path: Path
    title: str


def get_changes(type, commit):
    try:
        return commit.diff(f"{commit}~1").iter_change_type(type)

    except GitCommandError:
        # Probably means we hit the initial commit
        return []


def git_created_date(filepath, rev: str = "HEAD"):
    for commit in repo.iter_commits(rev, paths=filepath):
        for change in get_changes("R", commit):
            if change.a_path == filepath:
                return git_created_date(change.b_path, f"{commit}~1")

    return commit.authored_datetime


def gen_recent_blogs() -> str:
    commits = repo.iter_commits('HEAD')

    entries: List[Entry] = []

    for commit in commits:
        # Compare current commit with last commit. This will mean that
        # the "added" files will actually show as "deleted", hence
        # the "D" argument.
        added = [("D", x) for x in get_changes("D", commit)]
        renamed = [("R", x) for x in get_changes("R", commit)]

        changes = added + renamed

        for change_type, change in changes:
            filename = change.a_path if change_type == "R" else change.b_path

            if re.match("blog.*md", filename):
                path = Path(filename)

                if not path.exists():
                    continue

                with path.open() as f:
                    # Assumes title is in the form "# header", and on the
                    # first line. This should be changed at some point.
                    title = get_title(f.readline())

                entries.append(Entry(git_created_date(filename), path, title))

    def build_entry(entry: Entry) -> str:
        return f'''
  <li>
    <span>
      <span class="gray">{entry.date.strftime('%b %e %Y')}</span>
      <a href="./{entry.path.with_suffix('.html')}">{entry.title}</a>
    </span>
  </li>'''

    entries = sorted(entries, key=lambda e: e.date, reverse=True)

    return f"<ul>{''.join([build_entry(e) for e in entries])}\n</ul>"


def gen_updated_date() -> str:
    # From: https://stackoverflow.com/a/52045942
    def day_suffix(day):
        suffixes = ["th", "st", "nd", "rd"]

        if day % 10 in [1, 2, 3] and day not in [11, 12, 13]:
            return suffixes[day % 10]

        return suffixes[0]

    now = datetime.now()
    return now.strftime('%B %dXXX %Y').replace("XXX", day_suffix(now.day))
