# CRFC-0001 从方向到可开工的 issue

- Status: draft
- Start Date: 2026-11-05
- RFC PR: [#9](https://github.com/Staring531/calendo_service/pull/9)
- Implementation PR: [#N](https://github.com/Staring531/calendo_service/pull/N)

[English](CRFC-0001-requirement-flow.md)

## 摘要

工作要经过四级才能落到代码：方向、需求、决定、实现。只有澄清记录经所有者确认的 issue 能授权开发。产品文档给出方向，不能单独授权任何工作。超出一个可开工单元的请求转为父 issue，先拆分，拆完才确认其中任何一项。只有在已确认的澄清记录点名某个决定时，才写 RFC。GitHub Project 看板上每个状态都有进入条件，对应上面某一项产物，并写明谁能移动卡片。`AGENTS.md` 改为项目入口，写明每一级放在哪里。

## 动机

issue [#8](https://github.com/Staring531/calendo_service/issues/8) 要的是整个 MCP 服务：7 个工具、一个公共端点、一轮 10 题验收。它要调用的核心只是一个空的 `src/calendo/__init__.py`。一则评论之内，这张 issue 就被当成已确认，理由是每一句都抄自 `docs/product/calendo-mvp.zh.md`；卡片随后被直接移到 Designing，理由是产品文档写了 MCP SDK 选型「走 RFC」。范围没有商定，需求没有拆分，悬而未决的边界问题一个也没送到所有者面前。

仓库规则允许了其中每一步：

- `AGENTS.md` 第 1 条和开发 skill 把产品背景、issue、所有者的话并列为需求来源。粗粒度文档里的一句话因此算作已确认。
- 没有规定一项工作要小到什么程度才能确认。
- 「写成问答，等所有者同意」没有固定格式，也没有标记同意的信号，一则评论就能顶替。
- 开发 skill 把产品文档的待决问题称为 RFC 的「队列」，Agent 会自行逐条处理。
- Project 的状态（Clarifying、Investigating、Designing、Ready、Accepted）在仓库里没有出现，`gh project item-edit` 改卡片时不检查任何东西。
- `AGENTS.md` 把一份文档写成「产品背景」，概览只有三行。Agent 读不到这份文档成熟到什么程度，也读不到仓库里已经有什么。

只修 #8，这六处都还在，下一个大请求会重演。

## 指南级说明

以「做 HTTP API」这样大的请求为例。

1. 有人开了 issue，看板把它放进 Backlog。
2. Agent 用可开工单元的标准衡量它，结果不满足：7 个接口、框架未选、核心还不存在。Agent 写一份澄清记录说明这些，把 issue 标为父 issue，并提出子卡片：先是首批接口需要的核心函数，然后是 `GET /v1/days/{date}`，再是其余接口。卡片移到 Clarifying。
3. 所有者阅读记录，调整拆分并确认。父 issue 永远不进 Ready，只用来跟踪子卡片。
4. 每张子卡片各有一份澄清记录：调用方发什么、返回什么、每个日期事实的来源、什么不在范围内。其中一张要先取证，例如 `holidays` 0.108 对 CN 2027 年返回什么。这张卡片移到 Investigating，证据写进 issue 后再移出。
5. 某份记录在「需要的决定」里列出「HTTP 框架」，所有者同意现在就定。这时才开 RFC pull request，引用那张 issue，卡片移到 Designing。
6. 所有者以 `Status: accepted` 合并 RFC，并确认那张子卡片。子卡片移到 Ready，开始实现。

产品文档在第 2 步用来提出拆分建议，不能让第 3 到第 6 步被跳过。

## 参考级说明

### 四级

| 级别 | 存放位置 | 能做什么 | 不能做什么 |
| --- | --- | --- | --- |
| 方向 | `docs/product/` 下的文档 | 说明要做什么、为什么做 | 授权任何工作 |
| 需求 | 澄清记录已确认的 issue | 授权一张卡片的行为和范围 | 做设计选择 |
| 决定 | `rfcs/` 下 `Status: accepted` 的 RFC | 定下一个以后要依赖的选择 | 扩大需求范围 |
| 实现 | 引用已确认 issue 的 pull request | 交付那张 issue | 超出澄清记录 |

所有者后来的话与文档冲突时，以所有者的话为准，记录里写明它推翻了哪一行。这条不变。

### 可开工单元

一张 issue 同时满足下面四条，才是可开工单元：

1. 只交付一组调用方能看到的行为，例如两个 MCP 工具，而不是一个产品。
2. 一个实现 pull request 能交付完。
3. 答案里每个日期事实都有来源，或者列为缺口。
4. 依赖的东西已经存在，或者是另一张 issue。

不满足的是父 issue。它记录范围和拆分，用 GitHub 的 sub-issue 挂子卡片，永远不进 Ready，子卡片全部完成后关闭。

### 澄清记录

issue 上的一则评论，按顺序包含这些小标题：

1. 范围内：本 issue 交付的行为。
2. 范围外：不做的事，以及每一项归哪张 issue。
3. 问答：请求、返回，以及每个日期事实的来源（带链接的官方通知、在固定版本下对 `holidays` 的观察，或者缺口）。
4. 假设：Agent 推断的内容，一行一条，等所有者确认或否定。
5. 拆分：issue 不满足可开工单元时，提出的子卡片。
6. 需要的决定：每个需要 RFC 的选择，以及为什么现在就要定。

所有者要求修改时由 Agent 改记录。Agent 不能确认自己写的记录。

### RFC 的进入条件

已确认的澄清记录在「需要的决定」里点名某个选择，而且所有者同意现在就定，才写 RFC。RFC 的动机一节引用那张 issue。产品文档里的待决问题只是候选，每一条转为一张 issue，文档改为链接到这些 issue，不再保留列表。本文这样的流程决定也从同一入口进来，来自所有者的要求。

### 看板状态

删除 `Accepted` 状态。交付 issue 的 pull request 写 `Closes <issue 链接>`，合并即关闭 issue，Project 的 Item closed workflow 把卡片移到 Done。

| 状态 | 进入条件 | 谁移动 |
| --- | --- | --- |
| Backlog | issue 加入看板 | Project workflow |
| Clarifying | 澄清记录已发表 | Agent |
| Investigating | 记录里列出缺口，issue 写明什么证据能补上 | Agent |
| Designing | 已确认的记录点名的 RFC，其 draft pull request 已开 | Agent |
| Ready | 记录已确认，issue 是可开工单元，依赖已就绪 | 所有者 |
| In Progress | 该 issue 的分支已建立 | Agent |
| Verifying | pull request 已开，正文附 `sh scripts/check.sh` 的输出 | Agent |
| Blocked | 一则评论写明在等什么：所有者的决定、上游发版、官方通知 | Agent 或所有者 |
| Done | issue 已关闭 | Project workflow |
| Rejected | 所有者否决 | 所有者 |

Agent 每次移动卡片，都在 issue 上评论：满足了哪条进入条件，附上那项产物的链接。Agent 从不把卡片移进 Ready 或 Rejected。

### 机械检查

CI 的 `records` job 检查 pull request 引用的 issue 带有确认信号。标为不交付行为（文档、工具、RFC）的 pull request 除外。读取哪种信号，见下面的未决问题。

### 实现要改的地方

- `AGENTS.md`：项目概览、仓库当前状态、每一级放在哪里、工作怎样流转（一段话加状态表链接），以及现有规则，其中第 1 条和第 5 条按本文改写。它把 `docs/product/` 写成方向文档的目录，不再写死某一份文件。
- 开发 skill：四级、可开工单元、澄清记录和 RFC 进入条件，替换「Before any code」一节，以及把待决问题称为队列的那句话。
- `.github/CONTRIBUTING.md` 及中文版：状态表。
- issue 表单：范围内、范围外两个字段，并说明大请求转为父 issue。
- pull request 模板：保留 `Closes <issue 链接>`。
- `scripts/check_changelog.py` 或新脚本，以及 `ci.yml`：机械检查。
- `docs/product/calendo-mvp.zh.md`：标题下加一行，说明它是方向文档；待决问题列表换成 issue 链接。
- 仓库标签：确认信号若是标签则新建；`type:bug`、`type:data`、`type:feature`、`type:investigation`（issue 表单已经在用）；`skip-changelog`（CI 已经在读）。
- Project 1：删除 `Accepted`，打开 Item closed，把 Pull request linked to issue 设为移到 Verifying。

## 缺点

一个明显的小改动现在也要经过澄清记录和确认。记录可以只有三行，但等所有者回复的时间省不掉。

看板和仓库仍然不是一个系统。状态表和每次移动时的评论，靠 Agent 自觉遵守；只有确认信号由机器检查。

## 理由与备选方案

只修 #8，手工拆分它，会留下所有让它发生的规则，下一个大请求会重演。

把产品文档当规格书，不断细化到足够细，等于把范围决定放进一份没有确认步骤、也不连着工作的文件。issue 两样都有。

让看板强制执行流程做不到：Project workflow 只在事件发生时设置状态，不做任何检查。检查应放在 CI，它已经卡住每一个 pull request。

考虑过保留 `Accepted` 作为人工验收。所有者选择合并即交付，所以 pull request 模板保留 `Closes`，删掉多出的那个状态。

什么都不做，Agent 仍可以把方向文档里的任何一行当成已确认的工作。

## 未决问题

- 确认信号。选项：所有者给 issue 打 `approved` 标签，CI 能读到；所有者回复固定字样，CI 只能靠解析评论读到；所有者把卡片移到 Ready，CI 没有 Project 令牌就读不到。机械检查要等这个答案。
- RFC 的实现合并之后，由谁把它改为 `implemented`。本文不决定。
- 父 issue 除了 GitHub 的 sub-issue 关联，是否另加标签。

---

## Changes

### v1.0.0

- 初始版本
