"""A pull request closes one adopted leaf issue, and events move the project card.

- Given a body that closes one owner-opened issue with no open sub-issues, the check is quiet.
- Given no closing issue, two closing issues, or a parent that still has an open child, the
  check names that fact.
- Given an issue an agent opened, a line `Adopted` from the owner adopts it. Another comment
  does not.
- Given the labels skip-changelog or dependencies, the check does not ask for an issue.
- Given an RFC file in a pull request that names an issue, the card move is Designing.
- Given a line Adopted from the owner, the card move is Ready. A bot comment is not.
- Given a pull request that closes an issue and does not change an RFC, the card move is
  Verifying. A closed issue moves to Done.
"""

from __future__ import annotations

from check_requirement import closing_issues, has_adopted_line, requirement_errors
from project_status import decide


def test_one_owner_issue_with_no_open_child_is_quiet() -> None:
    assert (
        requirement_errors(
            labels=set(),
            body="Closes https://github.com/Staring531/calendo_service/issues/8",
            issue_author="Staring531",
            owner_comments=[],
            open_sub_issues=0,
        )
        == []
    )


def test_a_missing_a_pair_and_a_parent_are_each_named() -> None:
    missing = requirement_errors(
        labels=set(),
        body="no issue",
        issue_author=None,
        owner_comments=[],
        open_sub_issues=0,
    )
    pair = requirement_errors(
        labels=set(),
        body="Closes #1 and Fixes #2",
        issue_author="Staring531",
        owner_comments=[],
        open_sub_issues=0,
    )
    parent = requirement_errors(
        labels=set(),
        body="Closes #3",
        issue_author="Staring531",
        owner_comments=[],
        open_sub_issues=2,
    )
    assert any("exactly one issue" in error for error in missing)
    assert any("exactly one issue" in error for error in pair)
    assert any("open sub-issue" in error for error in parent)


def test_adopted_is_a_line_from_the_owner_and_nothing_else() -> None:
    body = "Closes #4"
    refused = requirement_errors(
        labels=set(),
        body=body,
        issue_author="cursor-cf[bot]",
        owner_comments=["please do this"],
        open_sub_issues=0,
    )
    accepted = requirement_errors(
        labels=set(),
        body=body,
        issue_author="cursor-cf[bot]",
        owner_comments=["Adopted\n"],
        open_sub_issues=0,
    )
    assert any("Adopted" in error for error in refused)
    assert accepted == []
    assert has_adopted_line("note\nAdopted\n")
    assert closing_issues("Closes #4 and closes #4") == [4]


def test_skip_changelog_and_dependencies_ask_for_no_issue() -> None:
    assert (
        requirement_errors(
            labels={"skip-changelog"},
            body="",
            issue_author=None,
            owner_comments=[],
            open_sub_issues=3,
        )
        == []
    )
    assert (
        requirement_errors(
            labels={"dependencies"},
            body="",
            issue_author=None,
            owner_comments=[],
            open_sub_issues=0,
        )
        == []
    )


def test_an_rfc_pull_request_moves_the_card_to_designing() -> None:
    status = decide(
        "pull_request",
        files=["rfcs/CRFC-0002-http.md"],
        body="Refs https://github.com/Staring531/calendo_service/issues/9",
        comment_author="",
        comment_body="",
    )
    assert status == "Designing"


def test_the_owner_adopted_line_moves_the_card_to_ready() -> None:
    assert (
        decide(
            "issue_comment",
            files=[],
            body="",
            comment_author="Staring531",
            comment_body="Adopted",
        )
        == "Ready"
    )
    assert (
        decide(
            "issue_comment",
            files=[],
            body="",
            comment_author="cursor-cf[bot]",
            comment_body="Adopted",
        )
        is None
    )


def test_an_implementation_pull_request_verifies_and_a_closed_issue_is_done() -> None:
    assert (
        decide(
            "pull_request",
            files=["src/calendo/__init__.py"],
            body="Closes #8",
            comment_author="",
            comment_body="",
        )
        == "Verifying"
    )
    assert decide("issues", files=[], body="", comment_author="", comment_body="") == "Done"
