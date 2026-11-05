# Changelog details

[中文版](README.zh.md)

Release history lives in two levels:

1. [`../CHANGELOG.md`](../CHANGELOG.md): one line per release, linking its folder.
2. `<version>/YYYY-MM-DD-<slug>.md`: one detail file per change, recording what the change did.

There is deliberately **no per-release index file**. An index is one file every pull request has
to touch, which turns an ordinary batch of changes into merge conflicts; a folder listing and
`grep` answer the same questions.

Everything that has not shipped goes into `unreleased/`, named for its state rather than a number,
because the version is decided at release. Never create a numbered folder for unshipped work. At
release preparation, `unreleased/` is renamed to the version actually shipped, `RELEASE.md` is
written, the release line is added to the root files, and the next change recreates `unreleased/`.

`<version>/RELEASE.md` is published verbatim as the GitHub Release body: a lead paragraph, then
`## Install`, `## Highlights`, `## Notable in this release` (optional) and `## Requirements`. It is
written at release, committed **before** the tag, and English-only: it is a publishing artifact,
not a changelog record. `scripts/check_release.py` refuses a tag without it.

Released folders are frozen.

## Detail file format

```markdown
# <Title: name the change, not the pull request>

- **Date:** YYYY-MM-DD
- **Type:** feature
- **Scope:** `core`, `mcp`
- **PR:** [#N](https://github.com/Staring531/calendo_service/pull/N)
- **Issue:** [#N](https://github.com/Staring531/calendo_service/issues/N)
- **Breaking:** yes — <what breaks, in one line>

[中文版](<name>.zh.md)

<lead paragraph: what the change did>

## <section named for its content>

- ...
```

The metadata block sits directly under the H1, one field per bullet, always in this order, so a
reader and a `grep` find each field in the same place.

| Field | Required | Value |
| --- | --- | --- |
| `Date` | always | The entry date, matching the filename prefix. |
| `Type` | always | One of `feature` (a new capability someone can use), `fix` (a defect corrected), `refactor` (restructuring with no change in behaviour), `data` (a date fact, a fixture, a data source or the `holidays` version changed), `process` (tooling, CI, docs, skills, release plumbing). |
| `Scope` | always | 1–5 areas, backticked, named as the tree names them: `core`, `http`, `mcp`, `site`, `data`, `tooling`, `ci`, `docs`, `skills`, `release`. |
| `PR` | when one exists | Full links to the pull requests that shipped the change. A bare `#N` does not render as a link in a Markdown file, so always write the URL, in the body too. |
| `Issue` | when one exists | Full links to the issues the change closes or answers. Issues and pull requests share one numbering space: check which one a number is before you write it. |
| `Breaking` | only when breaking | `yes — <one line>`. Omit the field otherwise, so `grep -rl 'Breaking:' changelog/` lists exactly the breaking changes. |

Omit a field that does not apply rather than writing a placeholder. The pull request number exists
only once the pull request is open: open it, then add the `PR` field in a follow-up commit on the
same branch.

### Body

An entry records **what was done**, in the past tense. It opens with a lead paragraph and
continues in sections named for their content; reuse an existing name (`## Details`,
`## Compatibility`) before inventing one. An entry whose `Breaking` field is set carries a
`## Compatibility` section stating what breaks and the migration step.

A `data` entry names the countries and years it touched, the dates whose answer changed (from what
to what), and the official source each change was checked against.

**Reasoning does not go on disk.** No `## Why`, `## Problem`, `## Decision`,
`## Alternatives considered`, `## Verification` or `## Risks`. The thinking still has to happen; it
goes in the pull request description, which stays attached to the diff it describes.

**Do not describe the current state of the codebase.** "`X` is not exported from `Y`" reads as
fact, drifts as the code moves, and costs every later reader a check they did not ask for. Write
what the change did at the time.

Link other entries relatively, e.g. `[inclusive ranges](2026-11-05-inclusive-ranges.md)`; from a
Chinese file, link the Chinese counterpart. Relative links survive the folder rename at release.

## Chinese counterpart

Every entry ships in both languages: `<name>.md` in English and `<name>.zh.md` in Chinese,
mirroring it section for section, in the same pull request. One without the other is unfinished.

What stays in English, verbatim, so one `grep` works across both languages: the metadata field
names and values (`Date`, `Type`, `Scope`, the links), code identifiers, parameter names, error
codes and file paths. Only the `Breaking` reason is prose, so only it is translated.

What is translated: all prose, and the section headings, in the same order and count.

| English | 中文 |
| --- | --- |
| `## Details` | `## 细节` |
| `## Compatibility` | `## 兼容性` |

Each file links its counterpart on the line directly below the metadata block: `[中文版](<name>.zh.md)`
in the English file, `[English](<name>.md)` in the Chinese one.

`scripts/check_changelog.py` checks all of the above that a machine can: names, pairs, field order
and values, links, the counterpart line, translated headings, reasoning headings and bare `#N`.

## Finding things

| Question | Query |
| --- | --- |
| What shipped in a release? | `ls changelog/<version>/` |
| What has ever broken compatibility? | `grep -rl 'Breaking:' changelog/` |
| Every date fact that changed | `grep -rl 'Type:\*\* data' changelog/` |
| Every entry touching the MCP server | `grep -rl 'Scope:.*mcp' changelog/` |
| Which entries a pull request appears in | `grep -rl 'pull/12)' changelog/` |
