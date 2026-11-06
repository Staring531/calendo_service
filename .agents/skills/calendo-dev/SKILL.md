---
name: calendo-dev
description: Use when developing Calendo itself — the core, the HTTP API, the MCP server, the site, the date data and its fixtures, the CI and release workflows; writing or auditing a changelog entry or an RFC; writing or changing a test; preparing a release; or writing anything a user or contributor reads. The flow and the directory rules live in AGENTS.md files; this skill points at them and at the long checklists.
---

# Developing Calendo

The development flow, the setup commands and the owner-only calls are in the root
[`AGENTS.md`](../../../AGENTS.md). Directory rules live in the nearest nested `AGENTS.md`. This
page only points at them. Read a checklist when the task reaches it.

| Read | When |
| --- | --- |
| [`src/calendo/AGENTS.md`](../../../src/calendo/AGENTS.md) | Changing the package, including where a date fact comes from |
| [`tests/AGENTS.md`](../../../tests/AGENTS.md) | Writing or changing a test |
| `reference/testing.md` | The test checklist: scenarios, fakes, coverage |
| `reference/verification.md` | Choosing what to run, or CI reading green when it should not |
| [`changelog/AGENTS.md`](../../../changelog/AGENTS.md) | Writing or auditing a changelog entry |
| [`rfcs/AGENTS.md`](../../../rfcs/AGENTS.md) | Drafting an RFC |
| [`docs/AGENTS.md`](../../../docs/AGENTS.md) | Editing product direction |
| `reference/writing.md` | Prose a reader sees, in English or Chinese |
| [`.github/AGENTS.md`](../../../.github/AGENTS.md) | Editing workflows, forms or contributor docs |
| `reference/release.md` | Preparing a release: the branch, `RELEASE.md`, the tag |

Search inside the repository. When a path does not resolve, ask `git ls-files`, and say the same
to any subagent you dispatch.
