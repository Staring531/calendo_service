"""Check changelog entry pairs against the format in changelog/README.md.

    python scripts/check_changelog.py                       # changelog/unreleased/
    python scripts/check_changelog.py --dir changelog/0.1.0
    python scripts/check_changelog.py --require-entry --base origin/main

`--require-entry` fails unless the branch adds or edits an entry under changelog/unreleased/
relative to `--base`; CI runs it on every pull request that is not labelled `skip-changelog`.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UNRELEASED = "changelog/unreleased"

FIELDS = ("Date", "Type", "Scope", "PR", "Issue", "Breaking")
REQUIRED_FIELDS = ("Date", "Type", "Scope")
TYPES = ("feature", "fix", "refactor", "data", "process")
NON_ENTRIES = frozenset({"README.md", "README.zh.md", "RELEASE.md"})

ENTRY_NAME = re.compile(r"^(?P<date>\d{4}-\d{2}-\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*(?P<zh>\.zh)?\.md$")
FIELD_LINE = re.compile(r"^- \*\*(?P<name>[A-Za-z]+):\*\* (?P<value>.+)$")
SCOPE_VALUE = re.compile(r"^`[a-z0-9-]+`(?:, `[a-z0-9-]+`){0,4}$")
GITHUB_LINK = re.compile(
    r"^\[#(?P<text>\d+)\]\(https://github\.com/[\w.-]+/[\w.-]+/(?P<kind>pull|issues)/(?P<num>\d+)\)$"
)
BREAKING_VALUE = re.compile(r"^yes — \S")
CJK = re.compile(r"[\u3400-\u9fff]")

FENCED_CODE = re.compile(r"^```.*?^```", re.MULTILINE | re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]+`")
MARKDOWN_LINK = re.compile(r"\[[^\]\n]*\]\([^)\n]*\)")
BARE_NUMBER = re.compile(r"(?<![\w&/#])#\d+\b")

REASONING_HEADINGS = frozenset(
    {
        "Why",
        "Problem",
        "Decision",
        "Alternatives considered",
        "Verification",
        "Risks",
        "为什么",
        "问题",
        "决策",
        "备选方案",
        "验证",
        "风险",
    }
)


@dataclass
class Entry:
    path: Path
    zh: bool
    fields: dict[str, str] = field(default_factory=dict[str, str])
    headings: list[str] = field(default_factory=list[str])


def _strip_for_prose(text: str) -> str:
    text = FENCED_CODE.sub("", text)
    text = INLINE_CODE.sub("", text)
    return MARKDOWN_LINK.sub("", text)


def _check_links(value: str, kind: str) -> bool:
    links = [part.strip() for part in value.split(",")]
    for link in links:
        match = GITHUB_LINK.match(link)
        if not match or match["kind"] != kind or match["text"] != match["num"]:
            return False
    return True


def parse_entry(path: Path, errors: list[str]) -> Entry:
    """Read one entry file, appending every format violation to `errors`."""
    name = ENTRY_NAME.match(path.name)
    entry = Entry(path=path, zh=bool(name and name["zh"]))
    lines = path.read_text(encoding="utf-8").splitlines()

    def fail(message: str) -> None:
        errors.append(f"{path}: {message}")

    if not lines or not lines[0].startswith("# "):
        fail("the first line must be the H1 title")
        return entry

    index = 1
    while index < len(lines) and not lines[index].strip():
        index += 1
    order: list[str] = []
    while index < len(lines) and (match := FIELD_LINE.match(lines[index])):
        field_name, value = match["name"], match["value"].strip()
        if field_name not in FIELDS:
            fail(f"unknown metadata field {field_name!r}")
        elif field_name in entry.fields:
            fail(f"metadata field {field_name!r} appears twice")
        else:
            entry.fields[field_name] = value
            order.append(field_name)
        index += 1

    expected_order = [name for name in FIELDS if name in entry.fields]
    if order != expected_order:
        fail(f"metadata fields must be in the order {', '.join(FIELDS)}")
    for required in REQUIRED_FIELDS:
        if required not in entry.fields:
            fail(f"missing metadata field {required!r}")

    entry_date = entry.fields.get("Date")
    if entry_date is not None:
        try:
            date.fromisoformat(entry_date)
        except ValueError:
            fail(f"Date {entry_date!r} is not a calendar date")
        if name and entry_date != name["date"]:
            fail(f"Date {entry_date} does not match the filename's {name['date']}")
    entry_type = entry.fields.get("Type")
    if entry_type is not None and entry_type not in TYPES:
        fail(f"Type {entry_type!r} is not one of {', '.join(TYPES)}")
    scope = entry.fields.get("Scope")
    if scope is not None and not SCOPE_VALUE.match(scope):
        fail("Scope must be 1-5 backticked lowercase identifiers, comma separated")
    pr = entry.fields.get("PR")
    if pr is not None and not _check_links(pr, "pull"):
        fail("PR must be full links to pull requests, written [#N](https://github.com/.../pull/N)")
    issue = entry.fields.get("Issue")
    if issue is not None and not _check_links(issue, "issues"):
        fail("Issue must be full links to issues, written [#N](https://github.com/.../issues/N)")
    breaking = entry.fields.get("Breaking")
    if breaking is not None and not BREAKING_VALUE.match(breaking):
        fail("Breaking must read 'yes — <what breaks>'")

    while index < len(lines) and not lines[index].strip():
        index += 1
    stem = path.name.removesuffix(".zh.md").removesuffix(".md")
    counterpart = f"[English]({stem}.md)" if entry.zh else f"[中文版]({stem}.zh.md)"
    if index >= len(lines) or lines[index].strip() != counterpart:
        fail(f"the line after the metadata must be the counterpart link {counterpart}")
    else:
        index += 1

    body = "\n".join(lines[index:])
    entry.headings = [line[3:].strip() for line in lines[index:] if line.startswith("## ")]
    for heading in entry.headings:
        if heading in REASONING_HEADINGS:
            fail(f"'## {heading}': reasoning belongs in the PR description, not on disk")
        if entry.zh and not CJK.search(heading):
            fail(f"'## {heading}': headings in a .zh.md file are translated")

    if breaking is not None:
        compatibility = "兼容性" if entry.zh else "Compatibility"
        if compatibility not in entry.headings:
            fail(f"a Breaking entry needs a '## {compatibility}' section")

    for match in BARE_NUMBER.finditer(_strip_for_prose(body)):
        fail(f"bare {match.group()} does not render as a link; write the full URL")
    return entry


def check_pair(en: Entry, zh: Entry, errors: list[str]) -> None:
    """Hold the two halves of a pair to the same metadata and section count."""
    en_fields = {k: v for k, v in en.fields.items() if k != "Breaking"}
    zh_fields = {k: v for k, v in zh.fields.items() if k != "Breaking"}
    if en_fields != zh_fields:
        errors.append(f"{zh.path}: metadata differs from {en.path.name}")
    if ("Breaking" in en.fields) != ("Breaking" in zh.fields):
        errors.append(f"{zh.path}: Breaking is set in only one file of the pair")
    if len(en.headings) != len(zh.headings):
        errors.append(
            f"{zh.path}: {len(zh.headings)} '## ' sections, "
            f"but {en.path.name} has {len(en.headings)}"
        )


def check_dir(directory: Path) -> tuple[int, list[str]]:
    """Check every entry pair in one changelog folder; return (pairs checked, errors)."""
    errors: list[str] = []
    if not directory.is_dir():
        return 0, errors
    stems: dict[str, dict[bool, Path]] = {}
    for path in sorted(directory.iterdir()):
        if path.name in NON_ENTRIES or path.name.startswith("."):
            continue
        name = ENTRY_NAME.match(path.name)
        if not path.is_file() or not name:
            errors.append(f"{path}: not an entry name (YYYY-MM-DD-<slug>.md / .zh.md)")
            continue
        stem = path.name.removesuffix(".zh.md").removesuffix(".md")
        stems.setdefault(stem, {})[bool(name["zh"])] = path

    for stem, halves in stems.items():
        if False not in halves:
            errors.append(f"{directory / (stem + '.zh.md')}: missing its English file {stem}.md")
            continue
        if True not in halves:
            errors.append(f"{directory / (stem + '.md')}: missing its Chinese file {stem}.zh.md")
            continue
        en = parse_entry(halves[False], errors)
        zh = parse_entry(halves[True], errors)
        check_pair(en, zh, errors)
    return len(stems), errors


def changed_files(base: str, repo: Path) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def has_unreleased_entry(paths: list[str]) -> bool:
    return any(
        path.startswith(f"{UNRELEASED}/") and ENTRY_NAME.match(Path(path).name) for path in paths
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--dir", default=UNRELEASED, help="folder to check, relative to --repo")
    parser.add_argument("--require-entry", action="store_true")
    parser.add_argument("--base", help="git ref the branch is compared against")
    args = parser.parse_args(argv)

    count, errors = check_dir(args.repo / args.dir)
    if args.require_entry:
        if not args.base:
            parser.error("--require-entry needs --base")
        if not has_unreleased_entry(changed_files(args.base, args.repo)):
            errors.append(
                f"no entry added or edited under {UNRELEASED}/ since {args.base}. "
                "Add the YYYY-MM-DD-<slug>.md / .zh.md pair, or label the pull request "
                "skip-changelog if it changes nothing anyone reads or runs."
            )

    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"{len(errors)} changelog problem(s).", file=sys.stderr)
        return 1
    print(f"{count} changelog entry pair(s) in {args.dir} read clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
