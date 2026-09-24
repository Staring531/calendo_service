# docs/decisions/ — ADR 使用规则

> English version: [README.md](README.md)。

本目录下的 ADR 遵循 Michael Nygard 2011 年提出的格式（Title / Status / Context /
Decision / Consequences），这套格式是行业事实标准（adr-tools、AWS、Azure 等
广泛采用）。本文档是通用规则，可直接套用到其他项目；项目专属的取舍映射放在
各项目自己的 AGENTS.md 里。

## 什么改动算"架构级"，必须先开 ADR

判断标准（Nygard 定义）：一个决定如果影响系统的**结构、非功能特性、依赖关系、
接口或构建方式**，就是架构级决定。

更可操作的版本，符合下面任意一条就该开 ADR：

- 在几个都说得通的技术方案里选了一个，排除了其他方案
- 改变了系统结构（新增/移除一个组件，或改变模块边界）
- 锁定了某个数据源、协议或依赖，之后想换代价很高
- 明确接受了一个权衡取舍

**不需要开 ADR 的情况**：决定在一次迭代内可逆、只影响单个模块内部实现、是常规
实现选择（比如换一个日志库）。琐碎决定写太多 ADR 会稀释真正重要决定的可见性。

## 模糊边界怎么裁决

拿不准时用 Olaf Zimmermann 提出的**架构显著性测试**（Architectural Significance
Test）——七条判断依据（辅助判断的 checklist，不是打分工具）：

1. 对业务价值或业务风险有直接影响？
2. 是某个重要利益相关方明确关心的事？
3. 涉及的运行时质量要求比现有架构已满足的水平高出一个数量级？
4. 涉及一个行为不可控、不可预测的外部依赖？
5. 跨越多个部分、影响系统整体（比如安全、监控这类横切关注点）？
6. 对这个团队来说是第一次做？
7. 过去因类似问题吃过亏？

前 5 条相对客观，后 2 条依赖具体情境。跑完还拿不准时，默认动作是先写一个
**Y-Statement**（比完整 ADR 轻得多的单句格式："在 X 情境下，面对 Y 问题，我们
决定 Z，以达成 W，代价是接受 V"），而不是直接不记录，之后可以再升级成完整 ADR。

## 状态流转

`Proposed → Accepted`，之后可能变成 `Deprecated` 或 `Superseded by ADR-XXXX`。

- **Proposed**：决定被提出，但还没有实际验证（比如还没跑通原型）
- **Accepted**：决定生效，之后的代码改动应该遵循它
- **Deprecated**：决定不再适用，没有被另一条 ADR 直接替代
- **Superseded by ADR-XXXX**：被更新的决定取代，写清楚是哪一条

## 谁能把 Proposed 改成 Accepted

ADR 通过独立的、仅含文档的 PR 提出，初始 `Status: Proposed`。

- **审批人**：PR 负责人（仓库所有者）或指定的评审 agent。审批人必须是与
  PR 作者不同的 GitHub 账号，并通过 GitHub PR review 给出批准。
- **审批通过后**：在同一 PR 分支上追加一个提交，把 ADR 的 `Status` 改为
  `Accepted`，然后合并。`master` 上出现 `Accepted` 才允许开始实现。
- 实现（代码 + 测试 + changelog）放在之后另开的 PR，从已包含 `Accepted` ADR
  的 `master` 拉分支。
- `docs/design-docs/` 下的设计文档没有 Status 字段；同样走 PR 评审，但只有
  `Accepted` 的 ADR 才能解锁实现。

## 文件命名与目录结构

**格式**：`YYYY-MM-DD-NNNN-短小明确的英文说明.md`（英文，默认版本），配一份
`YYYY-MM-DD-NNNN-短小明确的英文说明.zh.md`（中文版）。

- 编号前缀（`NNNN-标题.md`）：Nygard/adr-tools 的标准做法
- 日期前缀：joelparkerhenderson.com 系 ADR 仓库家族的做法（`YYYY-MM-DD
  标题.md`），原意是 ISO 日期便于排序；该家族里日期和编号是二选一，不是叠加用
- `.en.md` / `.zh.md` 双语后缀：penguin-harness 自己的真实先例
  （`architecture.en.md`、`skills.{en,zh}.md` 等）
- "日期+编号"组合：没有查到外部项目现成这么用，是本文档把上面两条拼出来的
  设计，不是被广泛采用的外部惯例
- ADR 命名允许各项目自定义，不强制统一格式（jamesmh/architecture_decision_record
  的立场）——上面这套是本项目的选择，不是唯一正确答案

**固定模板**：见同目录下的 `ADR-TEMPLATE.md`（英文）和 `ADR-TEMPLATE.zh.md`（中文），
新开 ADR 时复制这两个文件，不要从零写。
