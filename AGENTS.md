# AGENTS.md — [project name]

> Chinese version: [AGENTS.zh.md](AGENTS.zh.md).

> Project-specific hard constraints go here, with links into
> `docs/decisions/` ADRs. Example shape:
> "See ADR-000X for [constraint]; check before touching [affected area]."
> [placeholder — fill in for your project]

## Project overview

calendo (domain: calendo.day) is a public MCP server exposing worldwide
public holidays to AI agent/LLM clients, with multi-language holiday
translation. Data source is vacanza/holidays (Python, offline, 250+
countries) rather than a live API, and the project supports both
online-sync and offline/air-gapped deployment modes. The first MVP tool,
`china_public_holidays`, is implemented under `src/calendo/`.

## Build & test commands

This project uses `uv` + a `Makefile`; run `make help` for the full list.
The commands below are copied verbatim from the actual `Makefile` targets:

- `make sync` — install/sync dependencies (`uv sync --all-extras`)
- `make lint` — ruff check
- `make format` — ruff check --fix + ruff format
- `make typecheck` — mypy (src/)
- `make test` — pytest
- `make cov` — pytest with HTML coverage report
- `make check` — lint + typecheck + test, run this before committing / in CI
- `make build` / `make clean`

## Code style

Per this repo's own README.md ("开发规范"):

- Lint/format: `ruff` (replaces flake8 + isort + black)
- Type checking: `mypy`, strict mode
- Dependency management: `uv add` / `uv remove` only — do not hand-edit
  the dependency arrays in `pyproject.toml`

## Development process (design before code)

Ordering below, from strongest to weakest evidence — see
`docs/decisions/README.md` for the sourcing on each:

1. **Architecture-level changes open an ADR first**, through the
   `docs/decisions/` Proposed → Accepted flow.
2. **When a design isn't settled enough for an ADR yet**, write a
   lightweight exploratory doc under `docs/design-docs/` first; promote it
   to an ADR once a concrete decision is made. Template:
   `docs/design-docs/DESIGN-DOC-TEMPLATE.md`.
3. **Data model / interfaces before business logic** (type-first /
   schema-first): define the data shape before writing the logic that
   processes it.
4. **Production code + tests + changelog land in the same PR.** The only
   recognized exception is a genuine emergency (a severe production bug,
   a security hole, an urgent legal issue — not a soft deadline).
   Mechanism: `scripts/check_pr_bundle.py`.
5. **Architecture overview document** (`ARCHITECTURE.md` /
   `ARCHITECTURE.zh.md`) reflects only "what the shape is now" — link to
   the relevant ADR for "why."

## Comment conventions

- Comments explain **why**, not **what**. If code needs a comment to be
  understood, the code itself should usually be simplified instead.
- Exception: regular expressions and complex algorithms often do benefit
  from comments explaining what they do.
- Order of operations: if a reader can't follow a piece of code, the
  first move is to make the code itself clearer; only add a comment when
  the code genuinely can't be made clearer on its own.
- Comments are not documentation — a class/module/function's
  documentation covers purpose, usage, and behavior; that's a different
  thing from an inline comment.

## Known footguns

- `git diff --name-only` escapes non-ASCII (e.g. Chinese) filenames as
  octal by default, which silently breaks prefix matching against
  `sensitive-paths.txt` / `src-paths.txt`. Both `scripts/check_adr_gate.py`
  and `scripts/check_pr_bundle.py` already pass `-c core.quotepath=false`
  to work around this — don't remove that flag or reimplement the git
  diff call without it.
- A module named the same as a Python stdlib module (e.g. `types.py`)
  under `src/calendo/` can trigger a circular-import crash — this was hit
  once while testing this project's governance tooling. Avoid stdlib
  module names when naming new files under `src/calendo/`.

## Architecture decision links

- [ADR-0001](docs/decisions/2026-09-23-0001-china-holidays-mcp.md) — 使用
  vacanza/holidays 和 Python MCP SDK 实现首个中国节假日工具。

## CI mechanical checks currently in place

- `scripts/check_adr_gate.py` — blocks a PR that touches an
  architecturally sensitive path (configured in
  `docs/decisions/sensitive-paths.txt`) without a new ADR or an explicit
  `no-adr-needed:` reason in the PR description.
- `scripts/check_pr_bundle.py` — blocks a PR that touches production code
  (configured in `docs/decisions/src-paths.txt`) without accompanying
  test and changelog changes, unless marked `emergency:`.
- `tests/test_adr_governance.py` — a pytest suite validating ADR file
  naming, sequential numbering, valid Status values, bilingual pairing,
  and that AGENTS.md's ADR links resolve.

## Further reading

- [ARCHITECTURE.md](ARCHITECTURE.md) / [ARCHITECTURE.zh.md](ARCHITECTURE.zh.md) — current architecture snapshot
- `docs/design-docs/` — exploratory design docs not yet promoted to an ADR
