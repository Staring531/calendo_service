# AGENTS.md — [项目名称]

> 英文版：[AGENTS.md](AGENTS.md)。

> 项目专属的硬约束写在这里，链接到`docs/decisions/`下对应的ADR。示例格式：
> "见ADR-000X关于[某约束]；改动[相关区域]前先看这条。"
> [占位符——需要按你的项目填写]

## 项目概述

calendo（域名 calendo.day）是一个面向 AI agent/LLM 客户端的公共假日 MCP 服务，
支持多语言假日翻译。数据源用 vacanza/holidays（Python，离线，覆盖 250+ 国家/
地区），不实时调用外部 API；同时支持在线同步和离线/物理隔离两种部署模式。
当前阶段：下面这套 ADR/CI 治理骨架已经搭好，但 `src/calendo/` 目前只有一个
占位用的 `add()` 函数，MVP 的真实实现还没开始。

## 构建与测试命令

本项目用 `uv` + `Makefile`，完整列表见 `make help`。下面这些命令原样照抄自
真实的 `Makefile` target：

- `make sync` —— 安装/同步依赖（`uv sync --all-extras`）
- `make lint` —— ruff 检查
- `make format` —— ruff check --fix + ruff format
- `make typecheck` —— mypy（检查 src/）
- `make test` —— pytest
- `make cov` —— pytest 并生成 HTML 覆盖率报告
- `make check` —— lint + typecheck + test 一次跑完，提交前/CI 用这个
- `make build` / `make clean`

## 代码风格

照抄本仓库自己 README.md「开发规范」一节：

- 检查/格式化：统一用 `ruff`（替代 flake8 + isort + black）
- 类型检查：`mypy`，strict 模式
- 依赖管理：只用 `uv add` / `uv remove`——不要手改 `pyproject.toml`
  里的依赖数组

## 研发流程（设计先于代码）

按依据强度从强到弱排列——每条的来源见`docs/decisions/README.md`：

1. **架构级改动先开ADR**，走`docs/decisions/`下Proposed → Accepted流程。
2. **设计还没到能开ADR的阶段**，先在`docs/design-docs/`下写一份轻量的
   探索性文档，定型后再升级成ADR。模板：`docs/design-docs/DESIGN-DOC-TEMPLATE.zh.md`。
3. **数据模型/接口先于业务逻辑实现**（type-first / schema-first）：
   能定义清楚的数据结构，先写出来，再写处理逻辑。
4. **生产代码 + 测试 + changelog 同一个PR产出**。唯一认可的例外是真正的
   emergency（严重生产bug、安全漏洞、紧急法律问题——不包括赶软性deadline）。
   机制见`scripts/check_pr_bundle.py`。
5. **架构总览文档**（`ARCHITECTURE.md` / `ARCHITECTURE.zh.md`）只反映
   "现在是什么样"，不解释"为什么"——为什么去看对应的ADR。

## 注释规范

- 注释解释**为什么**，不解释**是什么**。如果代码需要靠注释才能看懂，
  通常说明代码本身该写得更简单。
- 例外：正则表达式、复杂算法这类，注释解释"在做什么"是有价值的。
- 顺序：如果读者看不懂一段代码，第一反应应该是把代码本身改清楚；
  只有代码确实没法变得更清楚时，才加注释。
- 注释不等于文档——类/模块/函数的文档说明的是用途、用法、行为，
  跟行内注释是两回事。

## PR 流程（架构级改动走两个 PR）

1. **设计 PR（仅文档）**：ADR（`.md` + `.zh.md`，`Status: Proposed`）和/或
   设计文档。不改 `src/`。使用 `.github/PULL_REQUEST_TEMPLATE/adr.md`。
2. **审批**：由 PR 负责人或指定评审 agent 审批，审批人必须是与 PR 作者不同的
   GitHub 账号（见 `docs/decisions/README.zh.md`）。审批通过后把 `Status`
   改为 `Accepted` 并合并。
3. **实现 PR**：只有 ADR 在 `master` 上已是 `Accepted` 才能开始。从 `master`
   拉分支；代码 + 测试 + `CHANGELOG/unreleased/` 条目在同一 PR。使用
   `.github/PULL_REQUEST_TEMPLATE/code.md`。
4. agent 不得审批自己提的 PR；除非是指定审批人且不是该 PR 作者，否则不得把
   ADR 改成 `Accepted`。

## 已知坑（footguns）

- `git diff --name-only` 默认会把非 ASCII（比如中文）文件名转成八进制转义，
  会让对 `sensitive-paths.txt` / `src-paths.txt` 的前缀匹配悄悄失效。
  `scripts/check_adr_gate.py` 和 `scripts/check_pr_bundle.py` 已经加了
  `-c core.quotepath=false` 来绕过这个问题——不要去掉这个参数，也不要重新实现
  一遍不带这个参数的 git diff 调用。
- 在 `src/calendo/` 下新建文件时，如果模块名跟 Python 标准库同名（比如
  `types.py`），可能触发循环导入崩溃——测试这套治理工具时真实遇到过一次。
  给 `src/calendo/` 下的新文件起名时避开标准库模块名。

## 架构决策链接

[占位符——随着ADR积累，在这里逐条链接。格式：markdown链接，链接文字用ADR编号，
指向`docs/decisions/`下对应文件路径，后面跟一句话说明决定了什么。（这里刻意不写
真实示例链接，因为`tests/test_adr_governance.py`里的ADR链接检查会把它当成失效
链接报错——见该文件的`test_agents_md_adr_links_resolve`。）]

## 当前存在的CI机械核验

- `scripts/check_adr_gate.py`——改动碰了架构敏感路径（配置见
  `docs/decisions/sensitive-paths.txt`），没有新增ADR也没写
  `no-adr-needed:`理由就挡merge。
- `scripts/check_pr_bundle.py`——改动了生产代码（配置见
  `docs/decisions/src-paths.txt`）但没带测试和changelog就挡，
  `emergency:`标记可以豁免。
- `tests/test_adr_governance.py`——pytest套件，核验ADR文件名、编号
  连续性、Status合法取值、双语配对、AGENTS.md链接有效性。
- `.github/workflows/ci.yml` — 对每个到 `master` 的 PR 运行 `make sync` 和 `make check`（lint + typecheck + test）。

## 深入文档

- [ARCHITECTURE.md](ARCHITECTURE.md) / [ARCHITECTURE.zh.md](ARCHITECTURE.zh.md) —— 当前架构快照
- `docs/design-docs/` —— 还没升级成ADR的探索性设计文档
