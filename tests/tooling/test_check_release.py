"""The pre-tag release check, as the release workflow runs it on the tag's checkout.

- Given a tree prepared for v0.1.0, the check passes.
- Given a tag that is not vMAJOR.MINOR.PATCH, nothing else is read and the tag is refused.
- Given a pyproject.toml still on the previous version, the mismatch is named.
- Given a release folder with no entries, no RELEASE.md, a RELEASE.md that opens with a heading or
  lacks a required section, or a CHANGELOG without the release's line, each is named.
- Given entries left behind in changelog/unreleased/, the release is refused.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from builders import write_pair

from check_release import check_release, main

RELEASE_NOTES = """\
Calendo 0.1.0 answers whether a day in China is a working day.

## Install

uv add calendo

## Highlights

- get_day_info

## Requirements

Python 3.12 or later.
"""


def prepare(repo: Path, version: str = "0.1.0", notes: str | None = RELEASE_NOTES) -> Path:
    (repo / "pyproject.toml").write_text(
        f'[project]\nname = "calendo"\nversion = "{version}"\n', encoding="utf-8"
    )
    folder = write_pair(repo / "changelog" / "0.1.0")
    if notes is not None:
        (folder / "RELEASE.md").write_text(notes, encoding="utf-8")
    line = "- **0.1.0** — 2026-11-20. First release. ([details](changelog/0.1.0/))\n"
    (repo / "CHANGELOG.md").write_text(f"# Changelog\n\n{line}", encoding="utf-8")
    (repo / "CHANGELOG.zh.md").write_text(f"# 更新日志\n\n{line}", encoding="utf-8")
    return repo


def test_a_prepared_tree_is_ready_to_release(tmp_path: Path) -> None:
    prepare(tmp_path)
    assert main(["--repo", str(tmp_path), "--tag", "v0.1.0"]) == 0


@pytest.mark.parametrize("tag", ["0.1.0", "v0.1", "v0.1.0-rc1", "release-0.1.0"])
def test_a_tag_outside_the_version_pattern_is_refused(tmp_path: Path, tag: str) -> None:
    assert check_release(tmp_path, tag) == [f"tag {tag!r} is not vMAJOR.MINOR.PATCH"]


def test_a_pyproject_on_the_previous_version_is_named(tmp_path: Path) -> None:
    prepare(tmp_path, version="0.0.0")
    errors = check_release(tmp_path, "v0.1.0")
    assert len(errors) == 1
    assert "declares version '0.0.0'" in errors[0]


@pytest.mark.parametrize(
    ("notes", "rule"),
    [
        (None, "missing or empty"),
        ("\n", "missing or empty"),
        ("## Install\n\n## Highlights\n\n## Requirements\n", "lead paragraph"),
        (RELEASE_NOTES.replace("## Highlights", "## Changes"), "needs the sections"),
    ],
)
def test_release_notes_that_cannot_be_published_are_named(
    tmp_path: Path, notes: str | None, rule: str
) -> None:
    prepare(tmp_path, notes=notes)
    errors = check_release(tmp_path, "v0.1.0")
    assert any(rule in error for error in errors), errors


def test_a_release_folder_without_entries_is_named(tmp_path: Path) -> None:
    prepare(tmp_path)
    for path in (tmp_path / "changelog" / "0.1.0").glob("2026-*"):
        path.unlink()
    errors = check_release(tmp_path, "v0.1.0")
    assert any("no entries" in error for error in errors)


def test_a_changelog_without_the_release_line_is_named(tmp_path: Path) -> None:
    prepare(tmp_path)
    (tmp_path / "CHANGELOG.zh.md").write_text("# 更新日志\n", encoding="utf-8")
    errors = check_release(tmp_path, "v0.1.0")
    assert errors == ["CHANGELOG.zh.md: no '- **0.1.0** — ' line for this release"]


def test_entries_left_in_unreleased_refuse_the_release(tmp_path: Path) -> None:
    prepare(tmp_path)
    write_pair(tmp_path / "changelog" / "unreleased")
    errors = check_release(tmp_path, "v0.1.0")
    assert any("still holds entries" in error for error in errors)
