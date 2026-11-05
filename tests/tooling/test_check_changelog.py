"""Changelog entries, as a contributor's pull request and the release check read them.

- Given a well-formed English/Chinese pair, the folder reads clean and the pair is counted.
- Given a folder that does not exist (right after a release renames it), nothing is reported.
- Given one half of a pair, the missing half is named.
- Given a metadata block that breaks the format (order, a missing field, a Type outside the set,
  a Date that is not the filename's, a bare #N for PR or Issue, a PR field pointing at an issue),
  the file is reported with the rule it broke.
- Given a Breaking entry, it must carry a Compatibility section in each language.
- Given a reasoning heading, an untranslated Chinese heading or a bare #N in the prose, the entry
  is refused; a #N inside a link or code span is not prose and passes.
- Given two halves whose metadata or section count disagree, the pair is refused; the Breaking
  reason alone may differ, because it is translated.
- Given --require-entry, a branch that adds no entry under changelog/unreleased/ fails and one
  that adds an entry passes.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from builders import EN_ENTRY, STEM, ZH_ENTRY, Git, write_pair

from check_changelog import check_dir, main


def errors_for(tmp_path: Path, en: str = EN_ENTRY, zh: str = ZH_ENTRY) -> list[str]:
    _, errors = check_dir(write_pair(tmp_path / "unreleased", en, zh))
    return errors


def test_a_well_formed_pair_reads_clean_and_is_counted(tmp_path: Path) -> None:
    count, errors = check_dir(write_pair(tmp_path / "unreleased"))
    assert (count, errors) == (1, [])


def test_a_folder_that_does_not_exist_reports_nothing(tmp_path: Path) -> None:
    assert check_dir(tmp_path / "unreleased") == (0, [])


@pytest.mark.parametrize(("missing", "named"), [(".zh.md", "Chinese"), (".md", "English")])
def test_one_half_of_a_pair_names_the_missing_half(
    tmp_path: Path, missing: str, named: str
) -> None:
    folder = write_pair(tmp_path / "unreleased")
    (folder / f"{STEM}{missing}").unlink()
    _, errors = check_dir(folder)
    assert len(errors) == 1
    assert f"missing its {named} file" in errors[0]


@pytest.mark.parametrize(
    ("old", "new", "rule"),
    [
        (
            "- **Type:** feature\n- **Scope:** `core`, `http`",
            "- **Scope:** `core`, `http`\n- **Type:** feature",
            "in the order",
        ),
        ("- **Scope:** `core`, `http`\n", "", "missing metadata field 'Scope'"),
        ("- **Type:** feature", "- **Type:** feat", "Type 'feat'"),
        ("- **Date:** 2026-11-05", "- **Date:** 2026-11-04", "does not match the filename"),
        ("- **Scope:** `core`, `http`", "- **Scope:** core", "Scope must be"),
        (
            "- **PR:** [#12](https://github.com/Staring531/calendo_service/pull/12)",
            "- **PR:** #12",
            "PR must be full links",
        ),
        (
            "- **PR:** [#12](https://github.com/Staring531/calendo_service/pull/12)",
            "- **PR:** [#12](https://github.com/Staring531/calendo_service/issues/12)",
            "PR must be full links",
        ),
        (
            "- **PR:** [#12](https://github.com/Staring531/calendo_service/pull/12)",
            "- **PR:** [#12](https://github.com/Staring531/calendo_service/pull/12)\n"
            "- **Issue:** #3",
            "Issue must be full links",
        ),
        ("[中文版](2026-11-05-inclusive-ranges.zh.md)", "", "counterpart link"),
        ("## Details", "## Why", "reasoning belongs in the PR description"),
        ("counted both ends of the range.", "counted both ends, see #7.", "bare #7"),
    ],
)
def test_a_format_violation_in_the_english_file_names_its_rule(
    tmp_path: Path, old: str, new: str, rule: str
) -> None:
    assert old in EN_ENTRY
    errors = errors_for(tmp_path, en=EN_ENTRY.replace(old, new))
    assert any(rule in error and f"{STEM}.md" in error for error in errors), errors


def test_a_number_inside_a_link_or_a_code_span_is_not_a_bare_reference(tmp_path: Path) -> None:
    en = EN_ENTRY.replace(
        "counted both ends of the range.",
        "counted both ends ([#7](https://github.com/Staring531/calendo_service/issues/7), `#8`).",
    )
    assert errors_for(tmp_path, en=en) == []


def test_an_untranslated_heading_in_the_chinese_file_is_refused(tmp_path: Path) -> None:
    errors = errors_for(tmp_path, zh=ZH_ENTRY.replace("## 细节", "## Details"))
    assert any("headings in a .zh.md file are translated" in error for error in errors)


def test_a_breaking_entry_needs_a_compatibility_section_in_each_language(tmp_path: Path) -> None:
    pr = "- **PR:** [#12](https://github.com/Staring531/calendo_service/pull/12)"
    en = EN_ENTRY.replace(pr, pr + "\n- **Breaking:** yes — ranges now include both ends")
    zh = ZH_ENTRY.replace(pr, pr + "\n- **Breaking:** yes — 区间改为包含两端")
    errors = errors_for(tmp_path, en=en, zh=zh)
    assert any("'## Compatibility'" in error for error in errors)
    assert any("'## 兼容性'" in error for error in errors)

    en = en.replace("## Details", "## Compatibility")
    zh = zh.replace("## 细节", "## 兼容性")
    assert errors_for(tmp_path, en=en, zh=zh) == []


def test_halves_whose_metadata_or_sections_disagree_are_refused(tmp_path: Path) -> None:
    zh = ZH_ENTRY.replace("`core`, `http`", "`core`").replace("## 细节", "## 细节\n\n## 其他")
    errors = errors_for(tmp_path, zh=zh)
    assert any("metadata differs" in error for error in errors)
    assert any("2 '## ' sections" in error for error in errors)


def test_a_stray_file_in_the_folder_is_reported_and_readme_is_not(tmp_path: Path) -> None:
    folder = write_pair(tmp_path / "unreleased")
    (folder / "README.md").write_text("# notes\n", encoding="utf-8")
    (folder / "notes.md").write_text("# notes\n", encoding="utf-8")
    _, errors = check_dir(folder)
    assert len(errors) == 1
    assert "notes.md: not an entry name" in errors[0]


def test_require_entry_fails_a_branch_that_adds_no_entry(tmp_path: Path, git: Git) -> None:
    git("switch", "-q", "-c", "topic")
    (tmp_path / "README.md").write_text("changed\n", encoding="utf-8")
    git("add", ".")
    git("commit", "-q", "-m", "topic")

    code = main(["--repo", str(tmp_path), "--require-entry", "--base", "main"])
    assert code == 1


def test_require_entry_passes_a_branch_that_adds_an_entry(tmp_path: Path, git: Git) -> None:
    git("switch", "-q", "-c", "topic")
    write_pair(tmp_path / "changelog" / "unreleased")
    git("add", ".")
    git("commit", "-q", "-m", "topic")

    code = main(["--repo", str(tmp_path), "--require-entry", "--base", "main"])
    assert code == 0
