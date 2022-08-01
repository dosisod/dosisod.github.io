from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, Literal
import re

from git import Diff, Repo
from git.exc import GitCommandError
from git.objects.commit import Commit

from md2html.core import get_title, markdown_to_nodes


repo = Repo()


@dataclass
class Entry:
    date: datetime
    path: Path
    title: str


def get_changes(type: Literal["R", "D"], commit: Commit) -> Iterator[Diff]:
    try:
        return commit.diff(f"{commit}~1").iter_change_type(type)

    except GitCommandError:
        # Probably means we hit the initial commit
        return iter([])


def git_created_date(
    filepath: str | None, rev: str | None = "HEAD"
) -> datetime:
    for commit in repo.iter_commits(rev, paths=filepath or ""):
        for change in get_changes("R", commit):
            if change.a_path == filepath:
                return git_created_date(change.b_path, f"{commit}~1")

    return commit.authored_datetime


def gen_recent_blogs() -> str:
    commits = repo.iter_commits("HEAD")

    entries: list[Entry] = []

    for commit in commits:
        # Compare current commit with last commit. This will mean that
        # the "added" files will actually show as "deleted", hence
        # the "D" argument.
        added = [("D", x) for x in get_changes("D", commit)]
        renamed = [("R", x) for x in get_changes("R", commit)]

        changes = added + renamed

        for change_type, change in changes:
            filename = (
                change.a_path if change_type == "R" else change.b_path
            ) or ""

            if re.match("blog.*md", filename):
                path = Path(filename)

                if not path.exists():
                    continue

                title = get_title(markdown_to_nodes(path.read_text()))

                entries.append(Entry(git_created_date(filename), path, title))

    def build_entry(entry: Entry) -> str:
        return f"""
  <li>
    <span>
      <span class="gray">{entry.date.strftime('%b %e %Y')}</span>
      <a href="./{entry.path.with_suffix('.html')}">{entry.title}</a>
    </span>
  </li>"""

    entries = sorted(entries, key=lambda e: e.date, reverse=True)

    return f"<ul>{''.join([build_entry(e) for e in entries])}\n</ul>"


def gen_updated_date() -> str:
    # From: https://stackoverflow.com/a/52045942
    def day_suffix(day: int) -> str:
        suffixes = ["th", "st", "nd", "rd"]

        if day % 10 in [1, 2, 3] and day not in [11, 12, 13]:
            return suffixes[day % 10]

        return suffixes[0]

    now = datetime.now()
    return (
        now.strftime("%B %_dXXX %Y")
        .replace("XXX", day_suffix(now.day))
        .replace("  ", " ")
    )
