# 变更日志细节

[English](README.md)

发布历史分两层：

1. [`../CHANGELOG.zh.md`](../CHANGELOG.zh.md)：每个版本一行，链接到它的文件夹。
2. `<version>/YYYY-MM-DD-<slug>.md`：每个改动一份细节文件，记录这次改动做了什么。

这里有意**不设每个版本的索引文件**。索引是每个 pull request 都要改的同一个文件，会把一批普通改动变成合并冲突；文件夹列表加 `grep` 就能回答同样的问题。

尚未发布的内容都放在 `unreleased/`。它按状态命名、不按版本号命名，因为版本号到发布时才确定。不要为未发布的工作创建带版本号的文件夹。发布准备时，`unreleased/` 改名为实际发布的版本，写好 `RELEASE.md`，在根目录的两个文件里加上这一版的一行，下一个改动再重新创建 `unreleased/`。

`<version>/RELEASE.md` 会原样作为 GitHub Release 的正文发布：一段导语，然后是 `## Install`、`## Highlights`、`## Notable in this release`（可选）和 `## Requirements`。它在发布时编写，**在创建 tag 之前**提交，只有英文：它是发布产物，不是变更记录。没有它的 tag 会被 `scripts/check_release.py` 拒绝。

已发布的文件夹冻结，不再修改。

## 细节文件格式

```markdown
# <标题：写改动本身，不写 pull request>

- **Date:** YYYY-MM-DD
- **Type:** feature
- **Scope:** `core`, `mcp`
- **PR:** [#N](https://github.com/Staring531/calendo_service/pull/N)
- **Issue:** [#N](https://github.com/Staring531/calendo_service/issues/N)
- **Breaking:** yes — <一句话说明破坏了什么>

[English](<name>.md)

<导语：这次改动做了什么>

## <按内容命名的小节>

- ...
```

元数据块紧跟在 H1 之下，每个字段一行，顺序固定，读者和 `grep` 都能在同一个位置找到每个字段。

| 字段 | 是否必填 | 取值 |
| --- | --- | --- |
| `Date` | 必填 | 条目日期，与文件名前缀一致。 |
| `Type` | 必填 | 以下之一：`feature`（新增可用的能力）、`fix`（修正缺陷）、`refactor`（不改变行为的重构）、`data`（日期事实、夹具、数据来源或 `holidays` 版本发生变化）、`process`（工具、CI、文档、技能、发布流程）。 |
| `Scope` | 必填 | 1–5 个范围，加反引号，按目录树中的名字写：`core`、`http`、`mcp`、`site`、`data`、`tooling`、`ci`、`docs`、`skills`、`release`。 |
| `PR` | 有就写 | 发布这次改动的 pull request 的完整链接。Markdown 文件里光写 `#N` 不会渲染成链接，所以正文里也一律写 URL。 |
| `Issue` | 有就写 | 这次改动关闭或回应的 issue 的完整链接。issue 与 pull request 共用一套编号，写之前先确认这个编号是哪一种。 |
| `Breaking` | 仅在有破坏性变更时 | `yes — <一句话>`。没有就省略这个字段，这样 `grep -rl 'Breaking:' changelog/` 列出的恰好是全部破坏性变更。 |

不适用的字段直接省略，不写占位符。pull request 编号要等 pull request 打开后才有：先打开它，再在同一分支上追加一个提交补上 `PR` 字段。

### 正文

条目记录**做了什么**，用过去时。先写一段导语，再按内容分节；先复用已有的节名（`## 细节`、`## 兼容性`），再考虑起新名字。设置了 `Breaking` 字段的条目必须有 `## 兼容性` 一节，写明破坏了什么、怎样迁移。

`data` 条目写明涉及的国家和年份、回答发生变化的日期（从什么变为什么），以及每处变化所核对的官方来源。

**推理过程不落盘。** 不写 `## 为什么`、`## 问题`、`## 决策`、`## 备选方案`、`## 验证` 或 `## 风险`。思考仍然要做，写进 pull request 描述，它始终跟着自己所描述的 diff。

**不描述代码库的当前状态。**「`X` 没有从 `Y` 导出」读起来像事实，会随代码变动而悄悄过时，让以后每个读者都多做一次没人要求的核对。写这次改动当时做了什么。

引用其他条目用相对链接，例如 `[包含两端的区间](2026-11-05-inclusive-ranges.zh.md)`；从中文文件链接中文版。相对链接在发布时文件夹改名后仍然有效。

## 中文版

每个条目都有两种语言：英文 `<name>.md` 与中文 `<name>.zh.md`，逐节对应，在同一个 pull request 中提交。只有一半就是没写完。

以下内容在两种语言中都保持英文原样，以便一次 `grep` 覆盖两种语言：元数据的字段名和取值（`Date`、`Type`、`Scope`、链接）、代码标识符、参数名、错误码与文件路径。只有 `Breaking` 的原因是行文，所以只有它要翻译。

需要翻译的：全部行文和各节标题，顺序与数量保持一致。

| English | 中文 |
| --- | --- |
| `## Details` | `## 细节` |
| `## Compatibility` | `## 兼容性` |

每个文件在元数据块的下一行链接对应的另一半：英文文件写 `[中文版](<name>.zh.md)`，中文文件写 `[English](<name>.md)`。

上述规则中机器能检查的，`scripts/check_changelog.py` 都会检查：文件名、成对、字段顺序与取值、链接、对应语言链接、标题是否翻译、推理类标题以及裸 `#N`。

## 查找

| 问题 | 查询 |
| --- | --- |
| 某个版本发布了什么？ | `ls changelog/<version>/` |
| 哪些改动破坏过兼容性？ | `grep -rl 'Breaking:' changelog/` |
| 所有变动过的日期事实 | `grep -rl 'Type:\*\* data' changelog/` |
| 所有涉及 MCP 服务的条目 | `grep -rl 'Scope:.*mcp' changelog/` |
| 某个 pull request 出现在哪些条目里 | `grep -rl 'pull/12)' changelog/` |
