"""Design RFCs, as an RFC pull request and a later revision of it read them.

- Given a well-formed English/Chinese pair, the folder reads clean and the pair is counted.
- Given README, TEMPLATE and AGENTS.md beside that pair, the folder still reads clean.
- Given a name outside CRFC-NNNN-<slug>, a missing half, or two RFCs on one number, each is named.
- Given an English RFC without one of the required sections, the missing section is named.
- Given an unknown Status, or halves whose Status or section count disagree, the pair is refused.
- Given --base, a landed RFC whose text changed must add a version above its last one under
  Changes, and its two languages must change together; a newly added RFC needs neither.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from builders import EN_RFC, ZH_RFC, Git, write_rfc

from check_rfcs import check_dir, check_revisions, main


def test_a_well_formed_pair_reads_clean_and_is_counted(tmp_path: Path) -> None:
    assert check_dir(write_rfc(tmp_path / "rfcs")) == (1, [])


def test_readme_template_and_agents_md_beside_a_pair_read_clean(tmp_path: Path) -> None:
    folder = write_rfc(tmp_path / "rfcs")
    for name in ("README.md", "README.zh.md", "TEMPLATE.md", "TEMPLATE.zh.md", "AGENTS.md"):
        (folder / name).write_text("# kept\n", encoding="utf-8")
    assert check_dir(folder) == (1, [])


def test_a_name_a_missing_half_and_a_reused_number_are_each_named(tmp_path: Path) -> None:
    folder = write_rfc(tmp_path / "rfcs")
    (folder / "rfc-day-types.md").write_text(EN_RFC, encoding="utf-8")
    (folder / "CRFC-0001-other.md").write_text(EN_RFC, encoding="utf-8")
    _, errors = check_dir(folder)
    assert any("rfc-day-types.md: not an RFC name" in error for error in errors)
    assert any("CRFC-0001-other.zh.md: missing" in error for error in errors)
    assert any("number 0001 is taken" in error for error in errors)


def test_a_missing_required_section_is_named(tmp_path: Path) -> None:
    _, errors = check_dir(write_rfc(tmp_path / "rfcs", en=EN_RFC.replace("## Drawbacks\nd\n", "")))
    assert any("missing sections Drawbacks" in error for error in errors)


@pytest.mark.parametrize(
    ("en", "zh", "rule"),
    [
        (EN_RFC.replace("Status: draft", "Status: wip"), ZH_RFC, "'- Status:' must be one of"),
        (EN_RFC, ZH_RFC.replace("Status: draft", "Status: accepted"), "differs"),
        (EN_RFC, ZH_RFC.replace("## 缺点\nd\n", ""), "'## ' sections"),
        (EN_RFC.replace("### v1.0.0", "### first"), ZH_RFC, "'### vX.Y.Z'"),
    ],
)
def test_halves_that_break_the_shape_are_refused(
    tmp_path: Path, en: str, zh: str, rule: str
) -> None:
    _, errors = check_dir(write_rfc(tmp_path / "rfcs", en=en, zh=zh))
    assert any(rule in error for error in errors), errors


def land(tmp_path: Path, git: Git) -> None:
    write_rfc(tmp_path / "rfcs")
    git("add", ".")
    git("commit", "-q", "-m", "land the RFC")
    git("switch", "-q", "-c", "revise")


def commit(git: Git) -> None:
    git("add", ".")
    git("commit", "-q", "-m", "revise")


def test_a_landed_rfc_that_changes_without_a_new_version_is_refused(
    tmp_path: Path, git: Git
) -> None:
    land(tmp_path, git)
    write_rfc(tmp_path / "rfcs", en=EN_RFC.replace("r\n", "r, revised\n"), zh=ZH_RFC + "\n")
    commit(git)
    errors = check_revisions(tmp_path, "main")
    assert len(errors) == 1
    assert "above v1.0.0" in errors[0]


def test_a_landed_rfc_that_raises_its_version_in_both_languages_passes(
    tmp_path: Path, git: Git
) -> None:
    land(tmp_path, git)
    bump = "### v1.1.0\n\n- Updated: the reference section\n\n### v1.0.0"
    write_rfc(
        tmp_path / "rfcs",
        en=EN_RFC.replace("r\n", "r, revised\n").replace("### v1.0.0", bump),
        zh=ZH_RFC.replace("### v1.0.0", bump),
    )
    commit(git)
    assert check_revisions(tmp_path, "main") == []


def test_a_landed_rfc_changed_in_one_language_only_is_refused(tmp_path: Path, git: Git) -> None:
    land(tmp_path, git)
    bump = "### v1.1.0\n\n- Updated: wording\n\n### v1.0.0"
    write_rfc(tmp_path / "rfcs", en=EN_RFC.replace("### v1.0.0", bump), zh=ZH_RFC)
    commit(git)
    errors = check_revisions(tmp_path, "main")
    assert any("changed without its counterpart" in error for error in errors)


def test_a_newly_added_rfc_needs_no_version_bump(tmp_path: Path, git: Git) -> None:
    git("switch", "-q", "-c", "propose")
    write_rfc(tmp_path / "rfcs")
    commit(git)
    assert check_revisions(tmp_path, "main") == []
    assert main(["--repo", str(tmp_path), "--base", "main"]) == 0


def test_the_command_fails_when_any_rfc_problem_is_found(tmp_path: Path) -> None:
    write_rfc(tmp_path / "rfcs", en=EN_RFC.replace("## Summary\ns\n", ""))
    assert main(["--repo", str(tmp_path)]) == 1
