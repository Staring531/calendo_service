# AGENTS.md 写入开发流程，细则放到各目录旁

- **Date:** 2026-11-06
- **Type:** process
- **Scope:** `docs`, `skills`, `tooling`

[English](2026-11-06-agents-md-sections.md)

`AGENTS.md` 改为 [agents.md](https://agents.md/) 建议的分节，并写入唯一的一条开发流程。更细的规则放在各目录旁的嵌套 `AGENTS.md` 里。

## 细节

- 根文件把方向文档写成 `docs/product/` 目录。它写明包还处在 pre-alpha，`src/calendo/` 目前只暴露 `__version__`。
- 开发流程图覆盖：请求、所有者的确认、后续工作依赖某个选择时的 RFC、分支、changelog 一对文件、`scripts/check.sh`、推送、`ci` 检查、squash merge，以及所有者要求发版时的发布。
- 为 `src/calendo/`（日期事实）、`tests/`、`changelog/`、`rfcs/`、`docs/`、`.github/` 各加了一份 `AGENTS.md`。每份都写明根文件仍然适用，冲突时以更近的那份为准。
- `scripts/check_rfcs.py` 把 `rfcs/AGENTS.md` 与 README、模板一样，视为非 RFC 文件。
- `.agents/skills/calendo-dev/SKILL.md` 不再复述流程、日期事实规则和仓库结构。它改为指向这些 `AGENTS.md` 和 `reference/` 下的检查清单。
- `sh scripts/check.sh` 被写成格式、类型检查和测试这条链。CI 另外还会构建包，并在 pull request 上检查 changelog 和 RFC 记录。
