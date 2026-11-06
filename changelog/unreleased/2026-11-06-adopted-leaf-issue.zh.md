# pull request 必须关闭一条已采纳的叶子 issue

- **Date:** 2026-11-06
- **Type:** process
- **Scope:** `ci`, `docs`, `tooling`
- **PR:** [#12](https://github.com/Staring531/calendo_service/pull/12)
- **Issue:** [#11](https://github.com/Staring531/calendo_service/issues/11)

[English](2026-11-06-adopted-leaf-issue.md)

pull request 现在必须关闭一条由所有者开出或已采纳的 issue，并且这条 issue 不能还有未关闭的子 issue。项目卡片随这些事件移动。

## 细节

- `scripts/check_requirement.py` 在 `records` 作业里运行。所有者是 `Staring531`。采纳是评论里单独一行 `Adopted`。标签 `skip-changelog` 和 `dependencies` 跳过这项检查。
- 一个 pull request 做不完的请求保持为父 issue。Agent 为每个 story 开一条子 issue。子 issue 还开着时，pull request 不能关闭父 issue。
- `.github/workflows/project-status.yml` 把改 RFC 的 pull request 设为 Designing，把所有者的 `Adopted` 行设为 Ready，把实现用的 pull request 设为 Verifying，issue 关闭时设为 Done。这个 workflow 读 `PROJECT_TOKEN`，不用 App 令牌。
- 需求、`Adopted` 行和父子 issue 拆分写进了 `AGENTS.md` 和两份贡献指南。需求表单写明大请求成为父 issue，并把完成标准改成必填。
