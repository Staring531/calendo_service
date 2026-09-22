# AGENTS.md — [project name]

> Chinese version: [AGENTS.zh.md](AGENTS.zh.md).

> Project-specific hard constraints go here, with links into
> `docs/decisions/` ADRs. Example shape:
> "See ADR-000X for [constraint]; check before touching [affected area]."
> [placeholder — fill in for your project]

## Project overview

[placeholder — one paragraph: what this project is, its differentiation,
its current stage]

## Build & test commands

[placeholder — do not assume commands. An agent working in this repo
should confirm from pyproject.toml / package.json / Makefile etc.
before running anything, rather than guessing.]

## Code style

[placeholder — project-specific conventions, if any]

## Development process (design before code)

Ordering below, from strongest to weakest evidence — see
`docs/decisions/README.md` for the sourcing on each:

1. **Architecture-level changes open an ADR first**, through the
   `docs/decisions/` Proposed → Accepted flow.
2. **When a design isn't settled enough for an ADR yet**, write a
   lightweight exploratory doc under `docs/design-docs/` first; promote it
   to an ADR once a concrete decision is made. Template:
   `docs/design-docs/DESIGN-DOC-TEMPLATE.en.md`.
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

[placeholder — record project-specific gotchas here as they're
discovered, so the next agent session doesn't rediscover them the hard
way]

## Architecture decision links

[placeholder — as ADRs accumulate under docs/decisions/, link them here.
Format: a markdown link with the ADR number as link text, pointing at
its file path under docs/decisions/, followed by one line on what it
decided. (This section intentionally avoids writing a literal example
link here, since the ADR-link checker in tests/test_adr_governance.py
would flag it as a broken link — see that file's `test_agents_md_adr_links_resolve`.)]

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
