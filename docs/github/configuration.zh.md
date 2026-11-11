# GitHub 上的仓库设置

[English](configuration.md)

这页记录 2026-11-06 从 GitHub 读到的仓库规则、用户项目和 workflow。规则集、看板开关和 Actions secrets 存在 GitHub 上，不在 git 历史里。改了那些开关，同时改这页。

## 两个身份

`Staring531` 是所有者。开 issue、写 `Adopted`、批准 pull request、squash 合并、持有看板，都用这个账号。

`cursor-cf` 是安装在本仓库上的 GitHub App。仓库目录里的 agent 用它的安装令牌开 pull request。本地 `.envrc` 在进入仓库时把 `GH_TOKEN` 设成这枚令牌，所以在仓库目录里执行的 `gh` 是 App。离开仓库后，`gh` 回到钥匙串里登录的 `Staring531`。

要在仓库目录里以所有者身份执行 `gh`，先卸掉这枚令牌：

```sh
env -u GH_TOKEN gh ...
```

GitHub 不允许同一个人批准自己开的 pull request。agent 和所有者共用 `Staring531` 时，提交作者、标签和文件都分不出是谁在操作。App 开请求，所有者批准，规则集才能挡住直接推上 `main` 的操作。

App 令牌访问 `GET /user` 会返回 403，正文是 `Resource not accessible by integration`。这表示令牌属于这个 App。它也写不了 Actions secrets。设置 `PROJECT_TOKEN` 时要卸掉 `GH_TOKEN`。

## 仓库与合并方式

仓库 `Staring531/calendo_service` 是 public。免费账号的私有仓库打不开这套规则集，当时的接口要求升级到 GitHub Pro。

合并只留 squash。`allow_squash_merge` 为 true，`allow_merge_commit` 和 `allow_rebase_merge` 为 false。一次改动在 `main` 上留一条提交，提交说明用 pull request 的标题。

## 规则集 project-main

编号 26674411，enforcement 为 `active`，作用在默认分支。bypass 名单是空的，读到的 `current_user_can_bypass` 是 `never`。管理员不能跳过。页面在 https://github.com/Staring531/calendo_service/rules/26674411 。

| 规则 | 读到的参数 | 作用 | 原因 |
| --- | --- | --- | --- |
| `deletion` | 无 | 不能删除 `main` | 默认分支留在仓库里 |
| `non_fast_forward` | 无 | 不能强推，不能改写 `main` 上已有的提交 | 已合并的记录留在原地 |
| `pull_request` | 1 个批准；新推送使旧批准失效；`allowed_merge_methods` 只有 `squash`；不要求 code owner；不要求最后一次推送的人再批一次；不要求解决评论线程；`require_extra_approval_for_unattributed_changes` 为 false | 进入 `main` 的改动必须是一个 pull request，并且有一次 Approve | 所有者批准 App 开的请求。提交可以由本机 git 用户写出，pull request 由 App 打开，一次批准就够 |
| `required_status_checks` | 上下文名称正好是 `ci`；`strict_required_status_checks_policy` 为 true，分支要包含最新的 `main`；`do_not_enforce_on_create` 为 false | 合并前检查 `ci` 必须成功 | 格式、类型、测试、打包和记录都汇总进名为 `ci` 的 job。规则集只认这一个名字 |

## 怎样批准并合并

1. 打开 pull request。作者应是 `app/cursor-cf`。
2. 状态是 Closed 且没有合并时，先点 Reopen pull request。
3. 打开 Files changed，点 Review changes，选 Approve，再点 Submit review。
4. 回到 Conversation。`ci` 成功之后，绿色按钮是 Squash and merge。点它，再确认。

批准之后又推了新提交，这次 Approve 作废，需要再批一次。

## issue 怎样算需求

需求只来自本仓库的 GitHub issue。聊天消息和 `docs/` 里的文件都不提出需求，也不采纳需求。

一条 issue 算已采纳，满足下面任一条件：

- 作者是 `Staring531`。
- `Staring531` 在评论里写了单独一行 `Adopted`。这一行去掉首尾空白后正好是这 7 个字符。同一条评论里的其他句子不算。

一个 pull request 做不完的请求是父 issue。Agent 为每个 story 开一条子 issue，并写上四项内容。父 issue 在任一子 issue 还开着时保持打开，pull request 关闭的是子 issue。所有者不逐条开子 issue。Agent 开出的子 issue，要所有者单独写一行 `Adopted`，实现才开始。

`records` 作业在 pull request 上运行 `scripts/check_requirement.py`。正文用 `Closes`、`Fixes` 或 `Resolves` 带上恰好一条 issue，写成完整地址：

```text
Closes https://github.com/Staring531/calendo_service/issues/N
```

这条 issue 已采纳，并且没有未关闭的子 issue。标签 `skip-changelog` 和 `dependencies` 跳过这项检查。`skip-changelog` 同时跳过「分支必须新增一对变更日志」的检查。

需求表单的「如何判断完成」是必填。表单开头写明，一个 pull request 做不完的请求成为父 issue。

一份 RFC 在 `Status: draft` 时仍然是草案，包括已经合并的草案。它不授权实现。所有者把 `Status` 改成 `accepted` 并合并，才算接受。Agent 不改这一行。[CRFC-0001](../../rfcs/CRFC-0001-requirement-flow.zh.md) 仍是这样一份草案。这页不采纳它的澄清记录。

## 把一个 topic 拆成 story

一个 pull request 做不完的 topic 是父 issue。Agent 把它切成 story，每张 story 开一条子 issue，父 issue 保持打开。切分顺序就是根目录 [`AGENTS.md`](../../AGENTS.md) 里的七步。这一节是这七步所用的标准，以及一次拆法示范。

一张 story 写明四项：

| 项 | 内容 |
| --- | --- |
| 行为 | 调用方发出的一次调用，以及他收到的答案或错误。调用方可以单独接受或拒绝这一项 |
| 范围外 | 留在父 issue 或兄弟 story 上的行为，并写明是哪几条 issue |
| 来源 | 答案里的每个日期：官方通知及其链接、读到该值的 `holidays` 固定版本，或者缺口 |
| 完成标准 | 带标准答案的问题。只看这些问题就能判断 story 做完，不需要读代码 |

一条切割只要碰上下面任一条，它自己仍是父 issue：

- 完成标准、代码和变更日志放不进一个 pull request。
- 调用方可以在另一部分还没有时使用这一部分，而且两部分的完成标准不同，或日期来源不同。
- 行为依赖一个还没定的选择。这个选择单独走一个 RFC pull request。story 等它。RFC 和实现不放在同一个 pull request。
- story 点名了多于一个日期来源。

调用方看不到的一行，不开成子 issue。没有新的答案、新的错误、新的字段、新的已写明限度，就没有可以采纳的内容。改名、移动文件、升级工具，放进需要它的那张 story。

第一张 story 带上它那一条完成标准要用到的代码。后面的 story 写明它依赖的已合并 issue。没有一张子 issue 的正文只写「把核心搭起来」或「先选框架」。这件事若有能核对的答案，答案就是这张 story。若没有，它属于第一张有答案的 story。

示范。父 issue 要求 MCP 服务提供 7 个工具，并调用核心。调用方可以单独使用每一个工具，每个工具有自己的问题和标准答案。一个 pull request 放不下 7 组完成标准。父 issue 不实现。

1. 清单是 7 行，一个工具一行。实现核心、搭建 MCP、公共端点不进入这张清单。
2. 这 7 个工具依赖的返回结构，还没有一份 `Status: accepted` 的 RFC、也没有一条已合并的 issue 定过，那么这个结构是一张 RFC issue。工具 story 等它以 `Status: accepted` 合并。
3. 答案来自另一份官方通知的日期，单独成为一张 `data` story。工具 story 写明固定的 `holidays` 版本，或写明缺口。它不同时修改另一个国家的日期。
4. 两个工具分开。调用方可以只要其中一个，它们的完成标准也不同。
5. 第一张 story 写成：给定 `CN` 和 `2025-10-11`，调用方收到当天的类型。范围外是其余 6 个工具、HTTP 和官网。来源是固定的 `holidays` 版本，并附上通知链接，或写明「尚未与国务院通知逐日核对」。完成标准就是这一个问题和它的标准答案。回答这一个问题所需的核心代码写在这张 story 里。
6. 其余 6 个工具是 6 张 story，各自依赖第一张。父 issue 按这个顺序列出 7 张。
7. Agent 开出这 7 条子 issue，正文里写好四项。所有者不逐条开。某条子 issue 上面有 `Staring531` 单独一行 `Adopted` 之后，实现才开始。

切割要改时，所有者在父 issue 上评论。Agent 按那条评论改子 issue。还没有一行 `Adopted` 的子 issue，Agent 不动工。

## 看板状态

项目挂在用户 `Staring531` 名下，编号 1，标题是 `Calendo_Service_Devolpment`。地址是 https://github.com/users/Staring531/projects/1 。项目是私有的。Status 字段在 2026-11-06 有五个选项，顺序如下。

| 状态 | 本仓库的 workflow 何时写入 | 原因 |
| --- | --- | --- |
| `Backlog` | 不写入 | 列保留着。卡片进入项目时落在哪一列，由下面的看板自带 workflow 决定。接口不返回那个目标值 |
| `Designing` | `pull_request` 的 opened、synchronize 或 reopened。改动的文件里有 `rfcs/CRFC-NNNN-slug.md` 或同名的 `.zh.md`，并且正文点名了至少一条 issue | RFC 还在起草，实现还没开始 |
| `Ready` | `issue_comment` 的 created。评论作者的登录名是 `Staring531`，评论里有单独一行 `Adopted` | 所有者已经采纳，可以开工 |
| `Verifying` | 同一次 pull request 事件里，正文点名了 issue，并且改动的文件不属于上面的 RFC 条件 | 实现的 pull request 已经挂上这条 issue，等检查和批准 |
| `Done` | `issues` 的 closed | issue 已经关闭 |

RFC 条件先于 `Verifying`。一个 pull request 既改了 RFC 文件又写了 `Closes`，卡片去 `Designing`。

正文点名 issue 有两种写法，都会让卡片移动：`Closes`、`Fixes` 或 `Resolves` 加上编号或完整地址；正文中出现的任何一条本仓库 issue 地址。`records` 只认第一种，并且必须恰好一条。

`PROJECT_TOKEN` 没有设置时，`.github/workflows/project-status.yml` 打印警告并以退出码 0 结束。它不是规则集要求的检查，pull request 不会因此变红。2026-11-06 读到的 Actions secrets 列表是空的，这个 workflow 当时不会移动卡片。

脚本按名字查找 Status 选项，不把选项 id 写进代码。选项改名之后，同名的移动失败，日志里出现 `project status <name> does not exist`。

## 看板自带的 workflow

下表是 2026-11-06 从项目接口读到的开关。接口只返回名字和是否启用，不返回每个 workflow 写入的 Status 值。那个值在项目右上角菜单的 Workflows 里。

| 名字 | 启用 | 它响应的事 |
| --- | --- | --- |
| Auto-add to project | 是 | 仓库里新建的 issue 或 pull request 符合过滤条件时，加入这个项目 |
| Auto-add sub-issues to project | 是 | 子 issue 开出来时，加入这个项目 |
| Item added to project | 是 | 卡片进入项目时，把 Status 设成菜单里选的值 |
| Item closed | 是 | issue 或 pull request 关闭时，把 Status 设成菜单里选的值 |
| Pull request linked to issue | 是 | pull request 连上一条 issue 时，把那条 issue 的 Status 设成菜单里选的值 |
| Auto-close issue | 是 | issue 的 Status 变成菜单里选的值时，关闭这条 issue。GitHub 的说明用的是这个触发方式 |
| Pull request merged | 否 | pull request 合并时设置 Status。这里关掉了，合并本身不靠这个 workflow 挪卡片 |

`Pull request merged` 关闭后，卡片变成 `Done` 走的是 issue 关闭。正文里的 `Closes` 让 GitHub 在合并时关闭 issue，接着 `issues: closed` 触发本仓库的 workflow，把 Status 写成 `Done`。`Item closed` 同时也会跑，两边都可能写 Status。

## GitHub Actions 的 workflow

三个文件都在 `.github/workflows/`。

### CI

文件 `ci.yml`，workflow 名字是 `CI`。

触发：

- 推送到 `main`
- 目标分支是 `main` 的 pull request，类型为 opened、synchronize、reopened、labeled、unlabeled
- 手动 `workflow_dispatch`
- Release workflow 用 `workflow_call` 调用它，输入是要验证的 tag 或 commit

labeled 和 unlabeled 包含在内，是为了加上或去掉 `skip-changelog` 时重新跑 `records`。

权限是 `contents: read`。同一个 ref 上新的一次运行会取消还在进行的上一次。

| Job | 做什么 |
| --- | --- |
| `style` | `ruff format --check`、`ruff check`、actionlint，以及全部变更日志条目和 RFC 的格式 |
| `typecheck` | pyright 严格模式，范围是 `src/`、`scripts/`、`tests/` |
| `test (Python 3.12)` 与 `test (Python 3.14)` | pytest，统计分支覆盖率，套接字禁用。3.14 把 `coverage.xml` 存成 artifact，保留 7 天。没有覆盖率门槛 |
| `package` | `uv build`。wheel 里要有 `calendo/py.typed` 和 `LICENSE`。装进一个空环境后报出的版本等于 `pyproject.toml` |
| `records` | 见下一张表。事件不是 pull request 时，这个 job 打印一行后成功，不检查内容 |
| `ci` | `needs` 上面全部 job。`if: always()`，取消和跳过也算进结果。有一个结果不是 `success` 就失败 |

规则集只要求名为 `ci` 的检查。别的 job 失败时，`ci` 会失败，合并仍然被挡住。

`records` 在 pull request 上的三步：

| 步骤 | 何时跳过 | 检查什么 |
| --- | --- | --- |
| A changelog entry ships with the change | 标签 `skip-changelog` | 分支相对 `main` 新增了一对变更日志 |
| Revised RFCs raise their version | 不因这两个标签跳过 | 已落地的 RFC 有改动时，版本号已升高 |
| The pull request closes one adopted leaf issue | `skip-changelog` 或 `dependencies` | 恰好一条已采纳、且没有未关闭子 issue 的 issue |

### Project status

文件 `project-status.yml`，workflow 名字是 `Project status`。

触发：

- `pull_request` 的 opened、synchronize、reopened。不包含 closed，也不包含合并
- `issue_comment` 的 created
- `issues` 的 closed

权限是 `contents: read`、`pull-requests: read`、`issues: read`。移动卡片的那一步读取 secret `PROJECT_TOKEN`。它不用 `github.token`，也不用 App 令牌。

pull request 事件先用 `github.token` 列出改动的文件路径，再交给 `scripts/project_status.py`。状态选择见上面的看板表。脚本查找用户 `Staring531` 的 1 号项目，再按名字查找 Status 选项。issue 还不在项目里时先加进去，然后写入该字段。

这个 workflow 不属于 `ci`。secret 缺失时它警告并成功退出。

### Release

文件 `release.yml`，workflow 名字是 `Release`。

触发：推送匹配 `v*` 的 tag，或者手动运行并填入一个已有的 tag。

| Job | 作用 |
| --- | --- |
| `preflight` | 在这个 tag 的树上运行 `scripts/check_release.py`。该 tag 已经有 GitHub Release 时，后面的 job 不运行 |
| `validate` | 调用 CI workflow，验证对象是这个 tag |
| `release` | 权限改为 `contents: write`。`uv build`，写出 `SHA256SUMS`，用 `changelog/<version>/RELEASE.md` 作为 Release 正文，上传 `dist/*` |

已经推送的 tag 不移动。发布由所有者决定。这个 workflow 不在规则集要求的检查里。

## PROJECT_TOKEN

这是存在仓库 Actions secrets 里的一把经典 personal access token，名字必须是 `PROJECT_TOKEN`。`Project status` 用它修改用户项目上的卡片。

仓库自带的 `GITHUB_TOKEN` 只作用于这个仓库，改不了用户项目。App 不授予 Projects 权限。细粒度令牌的 Projects 权限只出现在组织的 Organization permissions 里。Resource owner 选择个人账号时，Account permissions 里没有 Projects。GitHub 文档把「用细粒度令牌访问用户账号拥有的 Projects」列为尚未提供的能力。

因此用经典令牌，只勾选 `project`（Full control of projects）。仓库是 public，不勾选 `repo`。这把令牌可以修改该账号下的所有项目。GitHub 目前不能把它限制到这一个看板。生成页面是 https://github.com/settings/tokens/new 。

令牌只在 `Paste your secret:` 之后粘贴，不写进命令。在仓库目录里执行：

```sh
env -u GH_TOKEN gh secret set PROJECT_TOKEN --repo Staring531/calendo_service
```

`env -u GH_TOKEN` 卸掉目录里的 App 令牌。带着那枚令牌访问 `actions/secrets/public-key` 会得到 403，正文是 `Resource not accessible by integration`。卸掉之后，`gh` 使用钥匙串里的 `Staring531`，这个账号可以写入 secret。

出现在命令行或聊天里的令牌已经暴露。到 https://github.com/settings/tokens 把它作废，再生成一把新的。

## 这次读到的，以及接口没有返回的

2026-11-06 读到的事实：仓库为 public；只允许 squash；规则集 `project-main` 的参数如上；Actions secrets 列表为空；看板五个状态如上；七个看板 workflow 的开关如上。

接口没有返回两件事。一件是每个看板自带 workflow 所写入的具体 Status 值。另一件是 App `cursor-cf` 的权限清单和安装仓库范围。App 能够打开 pull request，这一点由已合并的 [#12](https://github.com/Staring531/calendo_service/pull/12) 的作者 `app/cursor-cf` 证实。权限清单在 App 的设置页核对：Contents、Pull requests、Issues 为读写，Metadata 为只读。Administration、Projects、Actions、Secrets 不授予。安装范围只保留这个仓库。
