# AGENTS.md

The root [AGENTS.md](../AGENTS.md) applies here too. On a conflict, this file wins for
`changelog/`. [`README.md`](README.md) is the format. This file is the part agents get wrong.

## The pair

- `unreleased/YYYY-MM-DD-<slug>.md` and `.zh.md`, in the pull request that makes the change,
  mirroring section for section. Never create a numbered folder for unshipped work.
- H1, then the metadata block in this order: `Date`, `Type`, `Scope`, `PR`, `Issue`, `Breaking`.
  Omit a field that does not apply. Field names and values stay English in both files; only the
  `Breaking` reason is translated. Headings in the `.zh.md` are translated.
- `Breaking` present means a `## Compatibility` / `## 兼容性` section.
- The entry records what was done, in the past tense. No `## Why`, `## Problem`, `## Decision`,
  `## Alternatives considered`, `## Verification` or `## Risks`. Reasoning goes in the pull
  request description.
- A `data` entry names the countries and years, each date whose answer moved (from what to what),
  and the official source.
- A follow-up to an unreleased change extends that entry and adds its pull request to `PR`,
  instead of opening a new file. The `PR` line is added after the pull request is open, as a full
  URL, in both files. Issues and pull requests share one numbering space.
- A released folder is frozen. A change nobody reads or runs is labelled `skip-changelog` and
  ships no entry.

`scripts/check_changelog.py` checks the shape. On a pull request, `scripts/check_changelog.py --require-entry` checks that the branch added a pair.
