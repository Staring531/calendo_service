# 参与 Calendo 开发

[English](CONTRIBUTING.md)

本文说明环境准备、日常命令、改动必须通过的检查，以及仓库的工作规则。安全问题不要发公开 issue，[安全策略](SECURITY.zh.md)写明了报告渠道。

## 前置条件

- [uv](https://docs.astral.sh/uv/) 0.11.32 及以上的 0.11 版本。项目所用的 Python 由 uv 安装，本机不需要另装。
- Python 3.12 及以上。开发使用 `.python-version` 中的版本（3.14），CI 同时在最低支持版本 3.12 上运行。

## 环境与日常命令

```sh
uv sync                     # 按锁文件安装环境到 .venv/
sh scripts/check.sh         # 在本机跑一遍 CI 的完整检查链

uv run ruff format .        # 格式化
uv run ruff check --fix .   # lint
uv run pyright              # 严格模式类型检查
uv run pytest               # 全部测试，网络套接字禁用
uv run pytest tests/tooling/test_check_changelog.py   # 单个文件
```

开发过程中选最窄的、能让这次改动失败的检查；请求审查前跑一遍 `scripts/check.sh`。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| `src/calendo/` | Calendo 包。核心、HTTP API 与 MCP 服务建成后都放在这里。 |
| `tests/` | pytest 测试。`tests/tooling/` 测试仓库自身的检查脚本。 |
| `scripts/` | 仓库检查：`check_changelog.py`、`check_rfcs.py`、`check_release.py`，以及串起整条检查链的 `check.sh`。 |
| `changelog/` | 每个改动一对条目，按版本分组。格式见 `changelog/README.zh.md`。 |
| `rfcs/` | 设计 RFC，每个决定一对中英文文档。 |
| `docs/product/` | 产品背景：Calendo 做什么，以及起步时留下的待决问题。 |
| `.agents/skills/calendo-dev/` | 编码 Agent 需要知道、从外部又容易弄错的约定。`.claude` 链接到 `.agents`。 |

## 质量关卡

每个 pull request 和每次推送到 `main` 都运行 `.github/workflows/ci.yml`：

| Job | 检查内容 |
| --- | --- |
| `style` | `ruff format --check`、`ruff check`、对 workflow 的 actionlint，以及每个变更日志条目和 RFC 的格式 |
| `typecheck` | 对 `src/`、`scripts/`、`tests/` 的 pyright 严格模式检查 |
| `test` | 在 Python 3.12 与 3.14 上运行 pytest，统计分支覆盖率；套接字禁用，任何测试都碰不到网络 |
| `package` | `uv build`、wheel 的内容，以及安装后的 wheel 报出的版本与 `pyproject.toml` 一致 |
| `records` | 仅 pull request：分支新增了变更日志条目对；已落地的 RFC 若有修改，版本号已提升 |
| `ci` | 上面任何一个 job 没有成功就失败。分支保护只要求这一项检查。 |

没有覆盖率门槛。改动新增一个分支，就要新增走到这个分支的场景。

发布 workflow 在发布任何东西之前，先在 tag 上调用同一份 CI，所以发布所经过的验证与 pull request 完全相同。

## 工作规则

- **仓库的工作语言是英文**：代码、注释、错误信息、测试名、commit 信息、pull request 的标题与正文。中文只出现在它本身就是内容的地方：`*.zh.md` 文档，以及 `zh_CN` 节日名称这类数据。
- **每个改动都附一对中英文变更日志条目**：在做出改动的同一个 pull request 中新增 `changelog/unreleased/YYYY-MM-DD-<slug>.md` 及其 `.zh.md`。格式见 [`changelog/README.zh.md`](../changelog/README.zh.md)，CI 会检查。没有人会读到或运行到的改动（注释里的错别字、工具升级）改为打上 `skip-changelog` 标签。
- **日期事实都有来源。** Calendo 的回答来自固定版本的 [holidays](https://github.com/vacanza/holidays)，以及提交在仓库中的夹具；每份夹具都附有核对所依据的官方通知链接。日期从不由模型提供，服务运行时不发起任何网络调用。
- **一次数据变更就是一个 pull request**：夹具、来源链接、读取它的测试，以及一条 `Type: data` 的变更日志条目一起合入。升级 `holidays` 属于数据变更，所以 Dependabot 不碰它。
- **产品文档中留作待决的决定，先走 RFC**，再写依赖它的代码。见下文。
- **已推送的 tag 永不移动。** 发布准备单独走一个 pull request，顺序见[发布参考](../.agents/skills/calendo-dev/reference/release.md)。

## 设计 RFC

设计决定放在 [`rfcs/`](../rfcs/)，一份文档一个决定，成对出现：英文 `CRFC-NNNN-<slug>.md` 与中文 `CRFC-NNNN-<slug>.zh.md`。

当改动所做的决定会成为后续工作的基础时就写一份：回答的形状、数据来源、某一层所用的框架、服务部署在哪里、日期事实怎样更正。缺陷修复和不改变行为的重构不需要。

1. 复制 [`rfcs/TEMPLATE.md`](../rfcs/TEMPLATE.md) 及其中文版，从 [`rfcs/README.zh.md`](../rfcs/README.zh.md) 取下一个空闲编号，以 `Status: draft` 单独提一个 pull request。
2. 由所有者以 `Status: accepted` 合并，即为接受。实现的 pull request 按编号引用 RFC；RFC 与其实现从不放在同一个 pull request。
3. 已落地的 RFC 很少修改。必须修改时，提升版本号，并在 `## Changes` 下记录改了什么，中英文都要改。两样都没做的修订会被 CI 拒绝。

## Pull request

- 从 `main` 拉分支，命名为 `feat/<topic>`、`fix/<topic>`、`data/<topic>`、`docs/<topic>` 或 `chore/<topic>`。一个 pull request 只做一件事。
- 标题写成 squash 提交应有的样子：`feat(core): count working days across a range`。scope 与变更日志条目中的范围一致。
- 按 [pull request 模板](PULL_REQUEST_TEMPLATE.md)填写。在 `## Verification` 下写明实际运行了什么、结果如何。
- `ci` 通过后以 squash 方式合并。

## 仓库设置

这些设置在 GitHub 的设置页里，不在文件中，由所有者设置一次：

- **`main` 的分支保护**：必须经 pull request，必须通过 `ci` 状态检查，只允许 squash 合并，禁止强制推送和删除。只有一位维护者期间，不要求审批。
- **标签**，供表单、Dependabot 和 CI 使用：`type:feature`、`type:bug`、`type:data`、`type:investigation`、`type:chore`、`type:docs`、`dependencies`、`skip-changelog`。表单只会打上已经存在的标签。
- **私密漏洞报告**（Security 设置下），安全策略里的报告表单依赖它。
- **Actions**：workflow 权限默认只读。发布 job 自行申请 `contents: write`。

## 报告问题

使用 [issue 表单](https://github.com/Staring531/calendo_service/issues/new/choose)。Calendo 判定错的日期有专门的表单，它要求填写官方来源：有了这个链接，报告才能被核对，并转成夹具。
