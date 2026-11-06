# AGENTS.md

## Project overview

Calendo answers holiday and working-day questions for AI agents. It is a Python package
(`src/calendo/`) with a core that computes every answer and adapters that expose it: an HTTP API
and an MCP server. Product direction lives in `docs/product/`; design decisions live in `rfcs/`.

Domain rules (where date facts come from, test scenarios, changelog traps, releases) are in
[`.agents/skills/calendo-dev/SKILL.md`](.agents/skills/calendo-dev/SKILL.md). Read it before you
change code, tests, date data, a changelog entry, an RFC or a workflow. `.claude` links to
`.agents`.

## Setup commands

- Install: `uv sync` (uv 0.11.32 or later in the 0.11 line; it installs the Python in
  `.python-version`)
- Full check, the same chain CI runs: `sh scripts/check.sh`
- Format: `uv run ruff format .`
- Lint: `uv run ruff check --fix .`
- Typecheck: `uv run pyright`
- Test: `uv run pytest`, or one file: `uv run pytest tests/tooling/test_check_changelog.py`

## Repository layout

| Path | Holds |
| --- | --- |
| `src/calendo/` | The package |
| `tests/` | pytest suites; `tests/tooling/` tests the repository checks |
| `scripts/` | `check_changelog.py`, `check_rfcs.py`, `check_release.py`, `check.sh` |
| `changelog/` | One entry pair per change; `changelog/README.md` is the format |
| `rfcs/` | Design RFCs; `rfcs/README.md` is the process and the index |
| `docs/product/` | Product direction documents |
| `.github/` | CI and release workflows, issue forms, PR template, `CONTRIBUTING.md` |

Search inside the repository. When a path does not resolve, ask `git ls-files`.

## Testing instructions

- CI is `.github/workflows/ci.yml`. The one required check is the aggregate `ci` job.
- Tests run on Python 3.12 and 3.14 with sockets disabled (pytest-socket). A test that needs the
  network is wrong.
- While you work, run the narrowest check that would fail for your change. The table is in
  `.agents/skills/calendo-dev/reference/verification.md`.
- Run `sh scripts/check.sh` before you ask for review.
- Report what you ran and what it printed. Say which checks you did not run.

## Code style

- Python 3.12 or later, pyright strict over `src/`, `scripts/` and `tests/`.
- ruff, line length 100. The rule set is in `pyproject.toml`.
- English for code, comments, error messages, test names, commits and pull requests. Chinese only
  in `*.zh.md` files and in data such as `zh_CN` holiday names.

## Changelog and RFCs

- Every change adds an entry pair to `changelog/unreleased/`: `YYYY-MM-DD-<slug>.md` and
  `YYYY-MM-DD-<slug>.zh.md`, in the same pull request. A change nobody reads or runs gets the
  `skip-changelog` label instead.
- A decision later work builds on goes into an RFC first, in its own pull request. Only the owner
  accepts an RFC.
- `scripts/check_changelog.py` and `scripts/check_rfcs.py` check both formats.

## Pull requests

- Branch from `main` as `feat/`, `fix/`, `data/`, `docs/` or `chore/<topic>`. One topic per pull
  request.
- Title the pull request as the squash commit: `feat(core): count working days across a range`.
- Fill in `.github/PULL_REQUEST_TEMPLATE.md`, including the verification output.
- Pull requests are squash-merged once `ci` is green. Never push to `main`.

## Ask the owner first

- Changing behaviour the owner has not approved, or changing scope.
- Accepting an RFC, cutting a release or pushing a tag.
- Upgrading `holidays` or deciding between conflicting date sources.
- Force-pushing, rewriting history, deleting a branch, changing repository settings or secrets.

## Security

- Report a vulnerability through the private advisory form linked in `.github/SECURITY.md`, not a
  public issue.
- Keep credentials, tokens and private data out of the diff, logs and screenshots.
