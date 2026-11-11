# The changelog contract

The rules an agent follows are in [`changelog/AGENTS.md`](../../../../changelog/AGENTS.md), and
the format is `changelog/README.md`. This page is the longer checklist.

## The pair

- `YYYY-MM-DD-<slug>.md` and `YYYY-MM-DD-<slug>.zh.md`, mirroring section for section.
- H1, then the metadata block in fixed order — `Date` / `Type` / `Scope` / `PR` / `Issue` /
  `Breaking` — then the counterpart link, then a lead paragraph and sections named for their
  content. Field names and values stay English in both files; only the `Breaking` reason is
  translated.
- `Breaking` present means a `## Compatibility` / `## 兼容性` section stating what breaks and the
  migration step.
- Headings in the `.zh.md` are translated. An English heading left in the Chinese file is the most
  common way a pair stops mirroring, and the check refuses it.

## Traps

**The `PR` field is the one that gets forgotten.** The number exists only once the pull request is
open: open it, then add `- **PR:** [#N](https://github.com/Staring531/calendo_service/pull/N)` in
a follow-up commit on the same branch, in both files.

**Numbers are links, and some are issues.** A bare `#N` does not render as a link. Issues and pull
requests share one numbering space; route an issue to `Issue`, not `PR`.

**A `data` entry names its dates.** The countries and years touched, each date whose answer moved
(from what to what), and the official source each was checked against. "Updated CN data" is not
an entry.

**Reasoning does not go on disk.** No `## Why`, `## Decision`, `## Verification` and the like; the
check refuses them. The reasoning goes in the PR description.

**Related changes may share one entry.** A follow-up to an unreleased change extends that entry's
sections and adds its PR to the `PR` field, instead of opening a new file.

**A released folder is frozen.** Fix an entry's metadata during release preparation, before the
rename, or not at all.

Check before asking for review:

```sh
uv run python scripts/check_changelog.py
grep -L 'PR:' changelog/unreleased/*.md
```
