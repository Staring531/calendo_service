# AGENTS.md follows the agents.md section layout

- **Date:** 2026-11-06
- **Type:** process
- **Scope:** `docs`

[中文版](2026-11-06-agents-md-sections.zh.md)

`AGENTS.md` was rewritten in the sections [agents.md](https://agents.md/) suggests: project overview, setup commands, repository layout, testing instructions, code style, changelog and RFCs, pull requests, what to ask the owner first, and security.

## Details

- It names `docs/product/` as the directory of direction documents and no longer points at one product document.
- The date-fact rules (no network call at run time, no hand-typed or model-produced date, stopping when the library, a fixture and an expected answer disagree) left `AGENTS.md`. They stayed in the "Date facts" section of `.agents/skills/calendo-dev/SKILL.md`, which `AGENTS.md` links.
- Setup, lint, typecheck and test commands, the repository layout and the pull request rules were added from `.github/CONTRIBUTING.md`.
