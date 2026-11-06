# AGENTS.md carries the development flow, with directory rules beside the files

- **Date:** 2026-11-06
- **Type:** process
- **Scope:** `docs`, `skills`, `tooling`

[中文版](2026-11-06-agents-md-sections.zh.md)

`AGENTS.md` now follows the sections [agents.md](https://agents.md/) suggests, and it holds one development flow. The detailed rules sit in nested `AGENTS.md` files next to the directories they govern.

## Details

- The root file names `docs/product/` as the directory of direction documents. It states that the package is pre-alpha and that `src/calendo/` exposes `__version__` only.
- A development-flow diagram covers a request, the owner's yes, an RFC when later work depends on a choice, the branch, the changelog pair, `scripts/check.sh`, the push, the `ci` job, the squash merge, and a release when the owner asks for one.
- Nested `AGENTS.md` files were added for `src/calendo/` (date facts), `tests/`, `changelog/`, `rfcs/`, `docs/` and `.github/`. Each one says the root file still applies, and that the nearer file wins on a conflict.
- `scripts/check_rfcs.py` treats `rfcs/AGENTS.md` as a non-RFC file, with the README and the template.
- `.agents/skills/calendo-dev/SKILL.md` no longer restates the flow, the date-fact rules or the repository layout. It points at the `AGENTS.md` files and at the checklists under `reference/`.
- `sh scripts/check.sh` is described as the style, typecheck and test chain. CI also builds the package and, on a pull request, checks the changelog and RFC records.
