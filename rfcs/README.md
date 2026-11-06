# Design RFCs (CRFC)

[中文版](README.zh.md)

One design decision per document, as an English/Chinese pair: `CRFC-NNNN-<slug>.md` and
`CRFC-NNNN-<slug>.zh.md`. The open questions in the
[product background](../docs/product/calendo-mvp.zh.md) (待决问题) are background. An issue raises
the work of drafting an RFC; the issue may cite one of those questions.

## Conventions

1. **An RFC and the implementation it decides are never in the same pull request.** They merge
   independently; the implementation cites the RFC by number.
2. **The owner accepts an RFC by merging it with `Status: accepted`.** Until then it is `draft`.
   An agent may draft one; it never accepts one.
3. **A landed RFC changes rarely.** When it must, its version is raised and the change items are
   listed under `## Changes` (`### v1.1.0`, then `- Added…` / `- Removed…` / `- Updated…`), in both
   languages.
4. `Status` is one of `draft`, `accepted`, `implemented`, `superseded`, `rejected`. A superseded
   RFC names its successor in its first paragraph.

`scripts/check_rfcs.py` checks names, pairs, unique numbers, the required sections, `Status`, and,
on a pull request, that a revised RFC raised its version in both files.

## Shape

Copy [`TEMPLATE.md`](TEMPLATE.md) and [`TEMPLATE.zh.md`](TEMPLATE.zh.md). The English file carries
`## Summary`, `## Motivation`, `## Guide-level explanation`, `## Reference-level explanation`,
`## Drawbacks`, `## Rationale and alternatives`, `## Unresolved questions` and `## Changes`; the
Chinese file carries the same sections, translated, in the same order, except `## Changes`, which
keeps its English heading on both sides.

## Index

Take the next number after the last row.

| Document | Title | Status |
| --- | --- | --- |
| [CRFC-0001](CRFC-0001-requirement-flow.md) | From direction to workable issue | draft |
