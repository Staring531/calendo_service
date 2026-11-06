"""Move a project card from a GitHub event. The agent does not move cards.

GH_TOKEN is a token that can edit the owner's project. When it is unset the script warns and
exits 0, so a missing secret does not turn the pull request's required check red.

Designing: a pull request changes an RFC file and names an issue.
Ready: Staring531 comments a line whose only text is Adopted.
Verifying: any other pull request closes an issue.
Done: the issue is closed.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import cast

OWNER = "Staring531"
PROJECT_NUMBER = 1
RFC_FILE = re.compile(r"^rfcs/CRFC-\d{4}-[a-z0-9-]+(?:\.zh)?\.md$")
CLOSING = re.compile(
    r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+"
    r"(?:#|(?:https://github\.com/Staring531/calendo_service/issues/))(\d+)\b"
)
ISSUE_URL = re.compile(r"https://github\.com/Staring531/calendo_service/issues/(\d+)\b")


def has_adopted_line(body: str) -> bool:
    return any(line.strip() == "Adopted" for line in body.splitlines())


def issue_numbers(body: str) -> list[int]:
    seen: dict[int, None] = {}
    for pattern in (CLOSING, ISSUE_URL):
        for match in pattern.finditer(body):
            seen.setdefault(int(match.group(1)), None)
    return list(seen)


def decide(
    event_name: str,
    *,
    files: list[str],
    body: str,
    comment_author: str,
    comment_body: str,
) -> str | None:
    if event_name == "issues":
        return "Done"
    if event_name == "issue_comment":
        if comment_author == OWNER and has_adopted_line(comment_body):
            return "Ready"
        return None
    if event_name == "pull_request" and any(RFC_FILE.fullmatch(path) for path in files):
        return "Designing" if issue_numbers(body) else None
    if event_name == "pull_request" and issue_numbers(body):
        return "Verifying"
    return None


def targets(event_name: str, event: dict[str, object], body: str) -> list[int]:
    if event_name in {"issues", "issue_comment"}:
        number = _whole(_mapping(event.get("issue")).get("number"))
        return [number] if number is not None else []
    return issue_numbers(body)


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


def _whole(value: object) -> int | None:
    return value if isinstance(value, int) else None


def _graphql(query: str, variables: dict[str, object]) -> dict[str, object]:
    result = subprocess.run(
        ["gh", "api", "graphql", "--input", "-"],
        input=json.dumps({"query": query, "variables": variables}),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip() or result.stdout.strip(), file=sys.stderr)
        return {}
    payload = _mapping(_load(result.stdout))
    if _items(payload.get("errors")):
        print(json.dumps(payload.get("errors")), file=sys.stderr)
        return {}
    return _mapping(payload.get("data"))


def move(repo: str, number: int, status: str) -> bool:
    project = _graphql(
        "query($login: String!, $number: Int!) {"
        " user(login: $login) { projectV2(number: $number) { id } } }",
        {"login": OWNER, "number": PROJECT_NUMBER},
    )
    project_id = _text(_mapping(_mapping(project.get("user")).get("projectV2")).get("id"))
    if not project_id:
        return False
    field_data = _graphql(
        'query($id: ID!) { node(id: $id) { ... on ProjectV2 { field(name: "Status") {'
        " ... on ProjectV2SingleSelectField { id options { id name } } } } } }",
        {"id": project_id},
    )
    field = _mapping(_mapping(field_data.get("node")).get("field"))
    option_id = ""
    for item in _items(field.get("options")):
        row = _mapping(item)
        if _text(row.get("name")) == status:
            option_id = _text(row.get("id"))
    field_id = _text(field.get("id"))
    if not field_id or not option_id:
        print(f"::error::project status {status} does not exist", file=sys.stderr)
        return False
    owner, name = repo.split("/", 1)
    found = _graphql(
        "query($owner: String!, $name: String!, $number: Int!) {"
        " repository(owner: $owner, name: $name) { issue(number: $number) {"
        " id projectItems(first: 20) { nodes { id project { id } } } } } }",
        {"owner": owner, "name": name, "number": number},
    )
    issue = _mapping(_mapping(found.get("repository")).get("issue"))
    item_id = ""
    for node in _items(_mapping(issue.get("projectItems")).get("nodes")):
        row = _mapping(node)
        if _text(_mapping(row.get("project")).get("id")) == project_id:
            item_id = _text(row.get("id"))
    content_id = _text(issue.get("id"))
    if not item_id and content_id:
        added = _graphql(
            "mutation($project: ID!, $content: ID!) {"
            " addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {"
            " item { id } } }",
            {"project": project_id, "content": content_id},
        )
        item_id = _text(_mapping(_mapping(added.get("addProjectV2ItemById")).get("item")).get("id"))
    if not item_id:
        return False
    updated = _graphql(
        "mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {"
        " updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item,"
        " fieldId: $field, value: {singleSelectOptionId: $value}}) {"
        " projectV2Item { id } } }",
        {"project": project_id, "item": item_id, "field": field_id, "value": option_id},
    )
    return bool(updated)


def main() -> int:
    token = os.environ.get("PROJECT_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("::warning::PROJECT_TOKEN is unset; the card was not moved.")
        return 0
    os.environ["GH_TOKEN"] = token
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")
    event_name = os.environ.get("GITHUB_EVENT_NAME", "")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if not event_path or not repo:
        print("::error::GITHUB_EVENT_PATH and GITHUB_REPOSITORY are required", file=sys.stderr)
        return 1
    event = _mapping(_load(Path(event_path).read_text(encoding="utf-8")))
    files = [line for line in os.environ.get("CHANGED_FILES", "").splitlines() if line]
    pull = _mapping(event.get("pull_request"))
    comment = _mapping(event.get("comment"))
    comment_user = _mapping(comment.get("user"))
    body = _text(pull.get("body"))
    status = decide(
        event_name,
        files=files,
        body=body,
        comment_author=_text(comment_user.get("login")),
        comment_body=_text(comment.get("body")),
    )
    if status is None:
        print("no card move for this event")
        return 0
    failed = False
    for number in targets(event_name, event, body):
        if move(repo, number, status):
            print(f"issue #{number} -> {status}")
        else:
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
