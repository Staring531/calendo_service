# AGENTS.md

The root [AGENTS.md](../../AGENTS.md) applies here too. On a conflict, this file wins for
`src/calendo/`.

## Date facts

- The service makes no network call at run time.
- No date is typed into code by hand, and none comes from a model. A fact lives in the pinned
  `holidays` library or in a fixture file that names its official source.
- Every answer says how sure it is: its status (`official`, `cross_checked`, `unverified`,
  `provisional`) and the `data_version` of the block it came from. Unverified and provisional
  answers say so in words a model can repeat to a user.
- When the library, a fixture and the expected answer differ, stop. List each date with all three
  values and hand it to the owner. Which source wins is the owner's call.
- A data change is one pull request: the fixture, its source link, the tests and a `Type: data`
  changelog entry.
- The library's documented behaviours that are easy to get backwards (closed ranges, `days=0` and
  `days=1` from a non-working day, the next holiday inside an ongoing break, half days, silent
  language fallback) are listed with the product documents' table of the library's limits. A test
  pins each one before code depends on it. The test rules are in [`tests/AGENTS.md`](../../tests/AGENTS.md).
