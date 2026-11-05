"""Check that a tag can be released from this tree.

    python scripts/check_release.py --tag v0.1.0

The release workflow runs this on the tag's own checkout before it builds anything, because a
pushed tag is never moved: a mismatch found after publishing costs a version number.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

from check_changelog import check_dir

ROOT = Path(__file__).resolve().parent.parent
TAG = re.compile(r"^v(?P<version>\d+\.\d+\.\d+)$")
RELEASE_SECTIONS = ("Install", "Highlights", "Requirements")


def check_release(repo: Path, tag: str) -> list[str]:
    match = TAG.match(tag)
    if not match:
        return [f"tag {tag!r} is not vMAJOR.MINOR.PATCH"]
    version = match["version"]
    errors: list[str] = []

    project = tomllib.loads((repo / "pyproject.toml").read_text(encoding="utf-8"))
    declared = project.get("project", {}).get("version")
    if declared != version:
        errors.append(
            f"pyproject.toml declares version {declared!r}, not {version!r}: bump it in the "
            "release PR, then tag the merge commit"
        )

    folder = repo / "changelog" / version
    count, entry_errors = check_dir(folder)
    errors.extend(entry_errors)
    if count == 0:
        errors.append(f"{folder}: no entries; release prep renames changelog/unreleased/ to it")

    notes = folder / "RELEASE.md"
    if not notes.is_file() or not notes.read_text(encoding="utf-8").strip():
        errors.append(f"{notes}: missing or empty; it is published as the Release body")
    else:
        lines = notes.read_text(encoding="utf-8").splitlines()
        first = next(line for line in lines if line.strip())
        if first.startswith("#"):
            errors.append(f"{notes}: opens with a lead paragraph, not a heading")
        found = [line[3:].strip() for line in lines if line.startswith("## ")]
        present = [name for name in found if name in RELEASE_SECTIONS]
        if present != list(RELEASE_SECTIONS):
            errors.append(f"{notes}: needs the sections {', '.join(RELEASE_SECTIONS)}, in order")

    for name in ("CHANGELOG.md", "CHANGELOG.zh.md"):
        path = repo / name
        text = path.read_text(encoding="utf-8") if path.is_file() else ""
        if not re.search(rf"^- \*\*{re.escape(version)}\*\* — ", text, re.MULTILINE):
            errors.append(f"{name}: no '- **{version}** — ' line for this release")

    unreleased = repo / "changelog" / "unreleased"
    if unreleased.is_dir() and any(p.suffix == ".md" for p in unreleased.iterdir()):
        errors.append(f"{unreleased}: still holds entries; move them into changelog/{version}/")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--repo", type=Path, default=ROOT)
    parser.add_argument("--tag", required=True)
    args = parser.parse_args(argv)

    errors = check_release(args.repo, args.tag)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"{args.tag} cannot be released from this tree.", file=sys.stderr)
        return 1
    print(f"{args.tag} is ready to release.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
