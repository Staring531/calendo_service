"""A pull request closes one adopted issue that has no open sub-issues.

    python scripts/check_requirement.py --event "$GITHUB_EVENT_PATH"

The owner is Staring531. An issue the owner opened is adopted. An issue an agent opened is
adopted when the owner has commented a line whose only text is ``Adopted``. Labels
``skip-changelog`` and ``dependencies`` skip this check.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import cast

OWNER = "Staring531"
EXEMPT_LABELS = frozenset({"skip-changelog", "dependencies"})
CLOSING = re.compile(
    r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+"
    r"(?:#|(?:https://github\.com/Staring531/calendo_service/issues/))(\d+)\b"
)


def closing_issues(body: str) -> list[int]:
    seen: dict[int, None] = {}
    for match in CLOSING.finditer(body):
        seen.setdefault(int(match.group(1)), None)
    return list(seen)


def has_adopted_line(body: str) -> bool:
    return any(line.strip() == "Adopted" for line in body.splitlines())


def requirement_errors(
    *,
    labels: set[str],
    body: str,
    issue_author: str | None,
    owner_comments: list[str],
    open_sub_issues: int,
) -> list[str]:
    if labels & EXEMPT_LABELS:
        return []
    numbers = closing_issues(body)
    if len(numbers) != 1:
        return [
            "the pull request must close exactly one issue, with "
            "`Closes https://github.com/Staring531/calendo_service/issues/N`"
        ]
    if issue_author is None:
        return [f"issue #{numbers[0]} could not be read"]
    adopted = issue_author == OWNER or any(has_adopted_line(text) for text in owner_comments)
    errors: list[str] = []
    if not adopted:
        errors.append(
            f"issue #{numbers[0]} was not opened by {OWNER} and has no `{OWNER}` comment "
            "whose line is `Adopted`"
        )
    if open_sub_issues > 0:
        errors.append(
            f"issue #{numbers[0]} still has {open_sub_issues} open sub-issue(s); "
            "close a child issue instead"
        )
    return errors


def _load(raw: str) -> object:
    return cast(object, json.loads(raw))


def _mapping(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        return {}
    raw = cast(dict[object, object], value)
    return {str(key): item for key, item in raw.items()}


def _items(value: object) -> list[object]:
    if not isinstance(value, list):
        return []
    return list(cast(list[object], value))


def _text(value: object) -> str:
    return value if isinstance(value, str) else ""


def _gh_json(path: str) -> object | None:
    result = subprocess.run(
        ["gh", "api", path, "-H", "Accept: application/vnd.github+json"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip() or result.stdout.strip(), file=sys.stderr)
        return None
    return _load(result.stdout)


def errors_for_event(event: dict[str, object]) -> list[str]:
    pull = _mapping(event.get("pull_request"))
    if not pull:
        return ["this event has no pull request"]
    labels = {_text(_mapping(label).get("name")) for label in _items(pull.get("labels"))}
    body = _text(pull.get("body"))
    if labels & EXEMPT_LABELS:
        return []
    numbers = closing_issues(body)
    if len(numbers) != 1:
        return requirement_errors(
            labels=labels,
            body=body,
            issue_author=None,
            owner_comments=[],
            open_sub_issues=0,
        )
    repo = os.environ.get("GITHUB_REPOSITORY", "Staring531/calendo_service")
    number = numbers[0]
    issue = _mapping(_gh_json(f"repos/{repo}/issues/{number}"))
    comments = _gh_json(f"repos/{repo}/issues/{number}/comments?per_page=100")
    sub_issues = _gh_json(f"repos/{repo}/issues/{number}/sub_issues?per_page=100")
    if not issue or not isinstance(comments, list) or not isinstance(sub_issues, list):
        return [f"issue #{number} could not be read"]
    author = _text(_mapping(issue.get("user")).get("login"))
    owner_comments = [
        _text(_mapping(item).get("body"))
        for item in _items(cast(object, comments))
        if _text(_mapping(_mapping(item).get("user")).get("login")) == OWNER
    ]
    open_children = sum(
        1
        for item in _items(cast(object, sub_issues))
        if _text(_mapping(item).get("state")) == "open"
    )
    return requirement_errors(
        labels=labels,
        body=body,
        issue_author=author,
        owner_comments=owner_comments,
        open_sub_issues=open_children,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=Path, required=True)
    args = parser.parse_args()
    event = _mapping(_load(args.event.read_text(encoding="utf-8")))
    errors = errors_for_event(event)
    for error in errors:
        print(f"::error::{error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
