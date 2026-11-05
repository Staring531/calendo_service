---
name: calendo-dev
description: Use when developing Calendo itself — the core, the HTTP API, the MCP server, the site, the date data and its fixtures, the CI and release workflows; writing or auditing a changelog entry or an RFC; writing or changing a test; preparing a release; or writing anything a user or contributor reads. Covers where requirements come from, what the owner decides, the date-fact rules, the verification table, and the record-and-ship contract.
---

# Developing Calendo

Calendo answers holiday and working-day questions for AI agents: is this day a workday, what is the
N-th working day after a date, how many working days fall in a range, which long breaks a year has.
One Python core is the only source of answers. An MCP server and a read-only HTTP API adapt it;
the site at calendo.day calls the HTTP API and nothing else. Date facts come from a pinned version
of [holidays](https://github.com/vacanza/holidays) and from fixtures committed here, checked
against official notices. `docs/product/calendo-mvp.zh.md` is the product background.

This page is what applies to every change. Read a reference when the task reaches it:

| Read | When |
| --- | --- |
| `reference/testing.md` | **Writing or changing any test**: scenarios first, behaviour only, where the fakes go, how date expectations carry their source |
| `reference/verification.md` | Choosing what to run for a change, a test failing oddly, or CI reading green when it should not |
| `reference/changelog.md` | Writing or auditing a changelog entry |
| `reference/release.md` | Preparing a release: the branch, what changes, `RELEASE.md`, the tag |
| `reference/writing.md` | **Anything a reader sees**: docs, README, changelog prose, PR bodies, tool descriptions, error messages, in English or Chinese |

## Before any code: where the work comes from

A requirement comes from the product background, an issue, or the owner's own words. Something
neither says is not a requirement: propose it, and wait. When a request conflicts with the
background, the owner's later word wins; say which line it overrides.

Before you change behaviour, write down what you will build as questions with their answers: the
request a caller makes, what comes back, and **where each date fact in the answer comes from** (an
official notice and its link, or an observation of `holidays` at its pinned version, or nothing
yet). An answer with no source is a gap to report, not a value to invent. Show it to the owner and
wait for a yes before you implement anything whose behaviour they have not already approved.

A decision later work builds on — the shape of an answer, a data source, a framework, the
deployment, how a wrong date gets corrected — goes into an RFC under `rfcs/` first, in its own pull
request. The product background's 待决问题 list is the queue of such decisions.

## The owner's calls, never yours

Accepting an RFC. Changing scope. Which source wins when `holidays` and an official notice
disagree. What happens to answers already released (a changed date, a renamed field). Upgrading
`holidays`. Cutting a release or a tag. Force-pushing, rewriting history, deleting a branch someone
else made. Repository settings and secrets.

For each, state plainly what happens if nothing is done, give the options, and let the owner
decide. Do not pick one and mention it afterwards.

## Date facts

- **The service makes no network call at run time.** Tests run with sockets disabled
  (pytest-socket); a test that needs the network is wrong, not flaky.
- **No date is typed into code by hand, and none comes from a model.** A fact lives in the pinned
  library or in a fixture file that names its official source.
- **Every answer says how sure it is**: its status (`official`, `cross_checked`, `unverified`,
  `provisional`) and the `data_version` of the block it came from. Unverified and provisional
  answers say so in words a model can repeat to a user.
- **A disagreement is a finding.** When the library, a fixture and the expected answer differ,
  stop. List each date with all three values and hand it to the owner. Do not pick one and carry on.
- **A data change is one pull request**: fixture, source link, tests and a `Type: data` entry.
- The library's documented behaviours that are easy to get backwards (closed ranges, `days=0` and
  `days=1` from a non-working day, the next holiday inside an ongoing break, half days, silent
  language fallback) are listed with the product background's table of the library's limits. A
  test pins each one before code depends on it.

## Repo shape and branches

| Path | Holds |
| --- | --- |
| `src/calendo/` | The package: the core first, then the HTTP and MCP adapters |
| `tests/` | pytest; `tests/tooling/` tests the repository checks |
| `scripts/` | `check_changelog.py`, `check_rfcs.py`, `check_release.py`, `check.sh` |
| `changelog/`, `rfcs/` | The records; their READMEs are the formats |
| `.github/` | CI, release, Dependabot, forms, CONTRIBUTING, SECURITY |

Changes go through a branch and a pull request against `main`, squash-merged. Never push to
`main`. Branches are `feat/<topic>`, `fix/<topic>`, `data/<topic>`, `docs/<topic>`,
`chore/<topic>`; the PR title reads as the squash commit, `feat(core): …`.

Keep searches inside the repository. When a path does not resolve, ask `git ls-files` rather than
scanning the disk. Say the same to any subagent you dispatch.

## Tests prove behaviour

Write the scenarios in the module docstring before the tests; one test per scenario, named as the
behaviour. Assert what a caller observes, and look first for what must not happen. Never test a
constant or restate the source. `reference/testing.md` has the rules and the checklist.

## Verify what you changed

`uv sync` first. The full chain is `sh scripts/check.sh`; CI runs the same commands. Pick the
narrowest evidence that would fail for this change while you work, from the table in
`reference/verification.md`, and run the full chain before you ask for review.

Report what you ran and what it printed. A command you did not run did not pass. Mark what you did
not verify as unverified, in the reply and in the PR body.

Once the evidence passes, commit and push to the current branch without asking. A force push still
needs the owner's yes.

## Record and ship

Every change ships a changelog entry pair in `changelog/unreleased/`, inside the pull request that
makes it: `YYYY-MM-DD-<slug>.md` and `.zh.md`, mirroring section for section. Reasoning goes in the
PR description, not on disk. A conclusion is not a deliverable file: findings go in the PR
description, in review comments on the lines they concern, and in the reply.
`changelog/README.md` is the format; `reference/changelog.md` has the traps.
