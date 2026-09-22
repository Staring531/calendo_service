# AGENTS.md — [项目名称]

> 英文版：[AGENTS.md](AGENTS.md)。

> 项目专属的硬约束写在这里，链接到`docs/decisions/`下对应的ADR。示例格式：
> "见ADR-000X关于[某约束]；改动[相关区域]前先看这条。"
> [占位符——需要按你的项目填写]

## 项目概述

[占位符——一段话说清楚：这是什么项目、差异化在哪、目前处于什么阶段]

## 构建与测试命令

[占位符——不要假设具体命令。agent在这个仓库里工作前，应该先去
pyproject.toml / package.json / Makefile 等文件里确认实际命令，
而不是凭空编。]

## 代码风格

[占位符——项目专属的代码规范，如果有的话]

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

## 已知坑（footguns）

[占位符——项目专属的坑，发现一个记一个，避免下次agent会话重新踩一遍]

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

## 深入文档

- [ARCHITECTURE.md](ARCHITECTURE.md) / [ARCHITECTURE.zh.md](ARCHITECTURE.zh.md) —— 当前架构快照
- `docs/design-docs/` —— 还没升级成ADR的探索性设计文档
