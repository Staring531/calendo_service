# 仓库检查、CI、发布流程与贡献约定

- **Date:** 2026-11-05
- **Type:** process
- **Scope:** `tooling`, `ci`, `release`, `docs`, `skills`

[English](2026-11-05-repository-tooling.md)

仓库建立了 Python 工程基线、只要求一项检查的 CI、由 tag 触发的发布流程、由脚本检查的中英文变更日志与 RFC 格式，以及给编码 Agent 用的开发技能。没有发布任何产品行为：`src/calendo/` 里只有包本身和它的版本号。

## 工程基线

- `pyproject.toml` 声明了 `calendo` 包（Python 3.12 及以上，用 `uv_build` 构建），并在 `uv.lock` 中锁定了开发工具：ruff 0.17.3、自带 Node 的 pyright 1.1.414、pytest 9.2.0、pytest-socket 0.8.1、pytest-cov 7.1.0 与 actionlint-py 1.7.12。
- pytest 在禁用套接字、严格 marker 与配置、警告即错误的条件下运行；pyright 以严格模式检查 `src/`、`scripts/` 与 `tests/`。
- `scripts/check.sh` 在本机按 CI 的顺序运行检查链：`uv lock --check`、ruff 格式化与 lint、actionlint、变更日志与 RFC 检查、pyright 和 pytest。
- 恢复了仓库首个提交中的 MIT `LICENSE`，`.gitattributes` 把换行符固定为 LF。

## CI 与发布

- `.github/workflows/ci.yml` 在每个 pull request 和每次推送到 `main` 时运行 `style`、`typecheck`、`test`（Python 3.12 与 3.14）、`package`、`records`，以及一个聚合的 `ci` job：其余任何 job 没有成功，它就失败。
- `package` 构建 sdist 与 wheel，检查 wheel 中带有 `calendo/py.typed` 与 `LICENSE`，并检查安装后的 wheel 报出的版本与 `pyproject.toml` 一致。
- `records` 对没有 `skip-changelog` 标签的 pull request 要求在 `changelog/unreleased/` 下新增条目对；已落地的 RFC 若有修改，要求提升版本号。
- `.github/workflows/release.yml` 在 `v*` tag 上运行：先在 tag 的源码上运行 `scripts/check_release.py`，再在 tag 上运行完整 CI，然后 `uv build`，发布一个以 `changelog/<version>/RELEASE.md` 为正文、以 sdist、wheel 与 `SHA256SUMS` 为资产的 GitHub Release。已经有 Release 的 tag 不会再发布任何东西。
- Dependabot 每周为 GitHub Actions 与 uv 提交分组更新，打上 `dependencies` 与 `skip-changelog` 标签，并忽略 `holidays`。

## 记录

- `changelog/README.zh.md` 规定了条目对、元数据块，以及 `feature`、`fix`、`refactor`、`data`、`process` 五种类型；由 `scripts/check_changelog.py` 检查。
- `rfcs/README.zh.md` 与模板规定了 CRFC 文档对及其状态；由 `scripts/check_rfcs.py` 检查。
- `scripts/check_release.py` 拒绝版本号、版本文件夹、`RELEASE.md` 或 `CHANGELOG` 中的一行尚未就绪的 tag，也拒绝 `changelog/unreleased/` 里仍留有条目的 tag。
- `tests/tooling/` 用 47 个测试覆盖了这三项检查。

## 贡献者与 Agent

- `.github/CONTRIBUTING.md`、`.github/SECURITY.md` 及其中文版取代了 `.github/README.md`。重写了 pull request 模板，以及缺陷、需求、技术调查三个表单，并新增了报告日期错误的数据表单。
- `AGENTS.md` 与 `.agents/skills/calendo-dev/` 记录了编码 Agent 要遵守的约定，`.claude` 链接到 `.agents`。
- `docs/product/calendo-mvp.zh.md` 收录了从 `.docx` 转换来的产品背景，原 `.docx` 移到它旁边。删除了为 memrepo 编写的两份流程文档。
