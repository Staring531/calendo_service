"""Check design RFCs against the conventions in rfcs/README.md.

    python scripts/check_rfcs.py
    python scripts/check_rfcs.py --base origin/main     # also checks revisions of landed RFCs

Every RFC is a pair, CRFC-NNNN-<slug>.md and CRFC-NNNN-<slug>.zh.md. With `--base`, an RFC
that already existed at the base and changed must raise its version under `## Changes`, and its
two languages must change together.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RFC_DIR = "rfcs"
NON_RFCS = frozenset({"README.md", "README.zh.md", "TEMPLATE.md", "TEMPLATE.zh.md"})

RFC_NAME = re.compile(r"^CRFC-(?P<num>\d{4})-[a-z0-9]+(?:-[a-z0-9]+)*(?P<zh>\.zh)?\.md$")
STATUS_LINE = re.compile(r"^- Status: (?P<status>\S+)\s*$", re.MULTILINE)
VERSION_HEADING = re.compile(r"^### v(\d+)\.(\d+)\.(\d+)\s*$", re.MULTILINE)

STATUSES = ("draft", "accepted", "implemented", "superseded", "rejected")
REQUIRED_SECTIONS = (
    "Summary",
    "Motivation",
    "Guide-level explanation",
    "Reference-level explanation",
    "Drawbacks",
    "Rationale and alternatives",
    "Unresolved questions",
    "Changes",
)


def sections(text: str) -> list[str]:
    return [line[3:].strip() for line in text.splitlines() if line.startswith("## ")]


def latest_version(text: str) -> tuple[int, int, int] | None:
    _, _, changes = text.partition("\n## Changes")
    versions = [(int(m[1]), int(m[2]), int(m[3])) for m in VERSION_HEADING.finditer(changes)]
    return max(versions) if versions else None


def check_document(path: Path, number: str, errors: list[str]) -> tuple[str | None, int]:
    """Check one file; return its Status and its count of '## ' sections."""
    text = path.read_text(encoding="utf-8")
    first = text.splitlines()[0] if text else ""
    if not first.startswith(f"# CRFC-{number} "):
        errors.append(f"{path}: the first line must be '# CRFC-{number} <title>'")
    status_match = STATUS_LINE.search(text)
    status = status_match["status"] if status_match else None
    if status not in STATUSES:
        errors.append(f"{path}: '- Status:' must be one of {', '.join(STATUSES)}")

    found = sections(text)
    if not path.name.endswith(".zh.md"):
        missing = [name for name in REQUIRED_SECTIONS if name not in found]
        if missing:
            errors.append(f"{path}: missing sections {', '.join(missing)}")
    if latest_version(text) is None:
        errors.append(f"{path}: '## Changes' needs at least one '### vX.Y.Z' heading")
    return status, len(found)


def check_dir(directory: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    if not directory.is_dir():
        return 0, errors
    pairs: dict[str, dict[bool, Path]] = {}
    numbers: dict[str, str] = {}
    for path in sorted(directory.iterdir()):
        if path.name in NON_RFCS or path.name.startswith(".") or path.is_dir():
            continue
        match = RFC_NAME.match(path.name)
        if not match:
            errors.append(f"{path}: not an RFC name (CRFC-NNNN-<slug>.md / .zh.md)")
            continue
        stem = path.name.removesuffix(".zh.md").removesuffix(".md")
        pairs.setdefault(stem, {})[bool(match["zh"])] = path
        if not match["zh"]:
            if match["num"] in numbers:
                errors.append(f"{path}: number {match['num']} is taken by {numbers[match['num']]}")
            numbers[match["num"]] = path.name

    for stem, halves in pairs.items():
        number = stem[5:9]
        if False not in halves or True not in halves:
            missing = f"{stem}.md" if False not in halves else f"{stem}.zh.md"
            errors.append(f"{directory / missing}: missing; every RFC is an English/Chinese pair")
            continue
        en_status, en_sections = check_document(halves[False], number, errors)
        zh_status, zh_sections = check_document(halves[True], number, errors)
        if en_status != zh_status:
            errors.append(f"{halves[True]}: Status {zh_status} differs from the English file's")
        if en_sections != zh_sections:
            errors.append(
                f"{halves[True]}: {zh_sections} '## ' sections, but the English file has "
                f"{en_sections}"
            )
    return len(pairs), errors


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, check=False)


def check_revisions(repo: Path, base: str) -> list[str]:
    """A landed RFC that changed since `base` raises its version, in both languages."""
    errors: list[str] = []
    diff = _git(repo, "diff", "--name-status", f"{base}...HEAD", "--", RFC_DIR)
    if diff.returncode != 0:
        return [f"git diff against {base} failed: {diff.stderr.strip()}"]
    modified = {
        line.split("\t")[-1]
        for line in diff.stdout.splitlines()
        if line.startswith("M\t") and RFC_NAME.match(Path(line.split("\t")[-1]).name)
    }
    for path in sorted(modified):
        counterpart = (
            path.removesuffix(".zh.md") + ".md"
            if path.endswith(".zh.md")
            else path.removesuffix(".md") + ".zh.md"
        )
        if counterpart not in modified:
            errors.append(f"{path}: changed without its counterpart {Path(counterpart).name}")
        if path.endswith(".zh.md"):
            continue
        before = _git(repo, "show", f"{base}:{path}").stdout
        after = (repo / path).read_text(encoding="utf-8")
        old, new = latest_version(before), latest_version(after)
        if old is not None and (new is None or new <= old):
            shown = ".".join(map(str, old))
            errors.append(
                f"{path}: a landed RFC that changes adds a '### v' heading above v{shown} "
                "under '## Changes'"
            )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--base", help="git ref the branch is compared against")
    args = parser.parse_args(argv)

    count, errors = check_dir(args.repo / RFC_DIR)
    if args.base:
        errors.extend(check_revisions(args.repo, args.base))
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"{len(errors)} RFC problem(s).", file=sys.stderr)
        return 1
    print(f"{count} RFC pair(s) read clean.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
