## What this changes

<!--
One or two sentences: what the change does and why it was needed. Add
`Closes https://github.com/Staring531/calendo_service/issues/N`.
The issue was opened by the owner, or the owner commented a line `Adopted`.
It has no open sub-issues. `skip-changelog` and `dependencies` skip this.
-->

## Verification

<!--
What you ran and what it said. Pick the narrowest evidence that would have failed without this
change. The full local chain is `sh scripts/check.sh`. For a date fact, name the dates you checked
and the official source you checked them against.
-->

## Checklist

- [ ] Changelog entry pair under `changelog/unreleased/`: `YYYY-MM-DD-<slug>.md` and its `.zh.md` counterpart, in the format [changelog/README.md](https://github.com/Staring531/calendo_service/blob/main/changelog/README.md) describes. A change nobody reads or runs is labelled `skip-changelog` instead.
- [ ] A changed date fact ships its fixture, its source link, its tests and a `Type: data` entry in this PR.
- [ ] Docs updated where this changes documented behaviour (README, `docs/`, the dev skill).
- [ ] No credential, token or private data in the diff, the logs or the screenshots.
