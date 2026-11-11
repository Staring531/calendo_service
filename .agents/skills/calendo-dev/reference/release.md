# Preparing a release

Who may cut a release, and that a pushed tag is never moved, is in
[`.github/AGENTS.md`](../../../../.github/AGENTS.md). A release is the owner's call: prepare it
when asked, and do not push the tag unless the owner says to.

## The one rule

**A pushed tag is never moved.** If a release run fails after the tag exists, fix the cause and
release the next patch version. Everything that can fail is therefore checked before the tag:
`scripts/check_release.py` runs on the release branch, and the release workflow runs it again on
the tag's own tree, then the full CI, before anything is published.

## Order

1. Branch `release/<version>` off `main`.
2. Make the changes in the table below, in one commit, and run
   `uv run python scripts/check_release.py --tag v<version>` until it passes.
3. Open the pull request `release: <version> — <one line>` and merge it when `ci` is green.
4. Tag `v<version>` on the merge commit and push the tag. `release.yml` reads
   `changelog/<version>/RELEASE.md` from the tag's checkout, so a file added after the tag never
   reaches the Release page.

## What changes

| Path | Change |
| --- | --- |
| `changelog/unreleased/` | `git mv` to `changelog/<version>/`. Nothing else moves; released folders are frozen. |
| `changelog/<version>/RELEASE.md` | New. The Release body, published verbatim. Shape below. |
| `CHANGELOG.md`, `CHANGELOG.zh.md` | One line at the top of the list: `- **<version>** — YYYY-MM-DD. <what it is>. ([details](changelog/<version>/))`. Replace the "Nothing has been released yet" line on the first release. |
| `pyproject.toml` | `version`. `calendo.__version__` reads the installed metadata, so there is nothing else to bump. |

Before the rename, sweep the batch: every entry has its `PR` field, every `Type` is one of the five,
no bare `#N` survives, and an entry amended by later pull requests cites all of them. Grep for
`changelog/unreleased/` across the tree; a citation into that folder breaks when it moves.

The version follows semver while below 1.0: a minor bump when an answer's shape or meaning
changes, a patch bump otherwise. A `data` change that moves a released answer is at least a minor
bump, and its entry says which dates moved.

## RELEASE.md

A lead paragraph saying what this release is, then `## Install`, `## Highlights`,
`## Notable in this release` (optional) and `## Requirements`, in that order; the check refuses
anything else. English only. Write it for a developer deciding whether to upgrade, in the register
of VS Code's release notes: each section leads with what changed in one sentence, and names,
numbers, defaults, error codes and file names carry the weight. `writing.md` has the rest.

For a release that changes date data, `## Highlights` lists the countries and years whose status
moved (for example `CN 2027: provisional → official`) and links the notices.
