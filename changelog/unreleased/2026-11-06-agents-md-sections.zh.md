# AGENTS.md 改用 agents.md 的分节

- **Date:** 2026-11-06
- **Type:** process
- **Scope:** `docs`

[English](2026-11-06-agents-md-sections.md)

`AGENTS.md` 按 [agents.md](https://agents.md/) 建议的分节重写：项目概览、环境命令、仓库结构、测试说明、代码风格、变更日志与 RFC、pull request、需要先问所有者的事、安全。

## 细节

- 方向文档改为指向 `docs/product/` 目录，不再写死某一份产品文档。
- 日期事实规则（运行时不联网、日期不手写也不由模型生成、库与夹具及期望答案不一致时停下）移出 `AGENTS.md`，保留在 `.agents/skills/calendo-dev/SKILL.md` 的「Date facts」一节，`AGENTS.md` 链接到该文件。
- 从 `.github/CONTRIBUTING.md` 补入环境、lint、类型检查与测试命令，仓库结构，以及 pull request 规则。
