# Contributing to Calendo

[中文版](CONTRIBUTING.zh.md)

This guide covers the setup, the daily commands, the checks a change has to pass, and the rules
the repository works by. A security problem does not go in a public issue: the
[security policy](SECURITY.md) says where to send it.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) 0.11.32 or later in the 0.11 line. uv installs the Python the
  project runs on; you do not need one of your own.
- Python 3.12 or later. Development uses the version in `.python-version` (3.14); CI also runs
  3.12, the oldest supported.

## Setup and daily commands

```sh
uv sync                     # the locked environment, in .venv/
sh scripts/check.sh         # style, typecheck and test; CI also builds and checks records

uv run ruff format .        # format
uv run ruff check --fix .   # lint
uv run pyright              # typecheck, strict
uv run pytest               # every test, with sockets disabled
uv run pytest tests/tooling/test_check_changelog.py   # one file
```

Pick the narrowest check that would fail for your change while you work, and run
`scripts/check.sh` before asking for review.

## Repo layout

| Path | What it holds |
| --- | --- |
| `src/calendo/` | The Calendo package. The core, the HTTP API and the MCP server live here as they are built. |
| `tests/` | pytest suites. `tests/tooling/` tests the repository's own checks. |
| `scripts/` | Repository checks: `check_changelog.py`, `check_rfcs.py`, `check_release.py`, and `check.sh`, which runs the chain. |
| `changelog/` | One entry pair per change, grouped by release. `changelog/README.md` is the format. |
| `rfcs/` | Design RFCs, one decision per English/Chinese pair. |
| `docs/product/` | The product background: what Calendo is for, and the open questions it started with. |
| `.agents/skills/calendo-dev/` | The index a coding agent follows, pointing at the root `AGENTS.md` and the nested ones. `.claude` links to `.agents`. |

## Quality gates

Every pull request and every push to `main` runs `.github/workflows/ci.yml`:

| Job | What it checks |
| --- | --- |
| `style` | `ruff format --check`, `ruff check`, actionlint over the workflows, and the shape of every changelog entry and RFC |
| `typecheck` | pyright in strict mode over `src/`, `scripts/` and `tests/` |
| `test` | pytest on Python 3.12 and 3.14, with branch coverage, and sockets disabled so no test reaches the network |
| `package` | `uv build`, the wheel's contents, and that the installed wheel reports the version `pyproject.toml` declares |
| `records` | Pull requests only: the branch adds a changelog entry pair, and an RFC that changed after landing raised its version |
| `ci` | Fails unless every job above succeeded. This is the one check branch protection requires. |

There is no coverage threshold. A change that adds a branch adds the scenario that takes it.

The release workflow calls the same CI on the tag before it publishes anything, so a release is
validated by exactly what a pull request is.

## Working rules

- **English is the repository's working language**: code, comments, error messages, test names,
  commit messages, pull request titles and bodies. Chinese appears where it is the content:
  `*.zh.md` documents, and data such as holiday names in `zh_CN`.
- **Every change ships a changelog entry, in both languages**:
  `changelog/unreleased/YYYY-MM-DD-<slug>.md` plus its `.zh.md` counterpart, inside the pull
  request that makes the change. [`changelog/README.md`](../changelog/README.md) is the format,
  and CI checks it. A change nobody reads or runs (a typo in a comment, a tool bump) is labelled
  `skip-changelog` instead.
- **Date facts have a source.** Calendo's answers come from a pinned version of
  [holidays](https://github.com/vacanza/holidays) and from fixtures committed here, each carrying
  a link to the official notice it was checked against. A model never supplies a date, and the
  service makes no network call at run time.
- **A data change is one pull request**: the fixture, its source link, the tests that read it and
  a `Type: data` changelog entry land together. Upgrading `holidays` is a data change, which is
  why Dependabot leaves it alone.
- **Decisions the product documents leave open go through an RFC** before the code that depends
  on them. See below.
- **A pushed tag is never moved.** Release preparation is a pull request of its own; the
  [release reference](../.agents/skills/calendo-dev/reference/release.md) has the order.

## Design RFCs

Design decisions live in [`rfcs/`](../rfcs/), one per document, as a pair:
`CRFC-NNNN-<slug>.md` in English and `CRFC-NNNN-<slug>.zh.md` in Chinese.

Write one when a change decides something later work builds on: the shape of an answer, a data
source, the framework a layer runs on, where the service is deployed, how a date fact is
corrected. A bug fix or a refactor that keeps behaviour needs none.

1. Copy [`rfcs/TEMPLATE.md`](../rfcs/TEMPLATE.md) and its Chinese counterpart, take the next free
   number from [`rfcs/README.md`](../rfcs/README.md), and add the pair with `Status: draft` in a
   pull request of its own.
2. The owner accepts it by merging it with `Status: accepted`. Implementation pull requests cite
   the RFC by number; an RFC and its implementation never share a pull request.
3. A landed RFC changes rarely. When it must, raise its version and record what changed under
   `## Changes`, in both languages. CI refuses a revision that does neither.

## Pull requests

- Branch from `main` as `feat/<topic>`, `fix/<topic>`, `data/<topic>`, `docs/<topic>` or
  `chore/<topic>`. One topic per pull request.
- Title it the way the squash commit should read: `feat(core): count working days across a
  range`. The scope is the area the changelog entry names.
- Fill in the [pull request template](PULL_REQUEST_TEMPLATE.md). Under `## Verification`, write
  what you ran and what it said.
- Pull requests are squash-merged once `ci` is green.

## Repository settings

These live in GitHub's settings, not in files, and are set once by the owner:

- **Branch protection on `main`**: require a pull request, require the `ci` status check, allow
  squash merging only, block force pushes and deletion. No approving review is required while
  there is one maintainer.
- **Labels** the forms, Dependabot and CI apply: `type:feature`, `type:bug`, `type:data`,
  `type:investigation`, `type:chore`, `type:docs`, `dependencies`, `skip-changelog`. A form only
  applies a label that already exists.
- **Private vulnerability reporting**, under Security, so the security policy's form works.
- **Actions**: workflow permissions read-only by default. The release job asks for
  `contents: write` itself.

## Reporting a problem

Use the [issue forms](https://github.com/Staring531/calendo_service/issues/new/choose). A date
Calendo gets wrong has its own form, which asks for the official source: that link is what lets
the report be checked and turned into a fixture.
