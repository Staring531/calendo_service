# GitHub 模板实施说明

本包包含可放入仓库根目录的 `.github/` 配置。它只提供模板文件，不会自动创建 GitHub Labels、Project 或 CI 工作流。

## 安装

1. 将本包中的 `.github/` 目录复制到 仓库根目录。
2. 在 GitHub 仓库中创建下方列出的 Labels。
3. 将这些文件提交到仓库默认分支；Issue 模板和 PR 模板需要位于默认分支才会对创建者生效。
4. 打开 GitHub 的 New issue 页面，逐个检查三个模板；再创建一个测试 PR，确认 PR 模板内容符合预期。
5. 验证通过后，删除测试 Issue/PR 或明确标记为测试记录。

## 必须先创建的 Labels

| 名称 | 建议说明 |
|---|---|
| `type:feature` | 需求或功能改进；由需求模板自动添加 |
| `type:bug` | 缺陷；由缺陷模板自动添加 |
| `type:investigation` | 技术调查；由调查模板自动添加 |
| `type:chore` | 工程维护或非功能性任务 |
| `type:docs` | 文档任务 |
| `priority:high` | 应优先处理；延迟会造成显著影响 |
| `priority:medium` | 正常优先级；按计划处理 |
| `priority:low` | 影响较低或可延后处理 |
| `risk:high` | 潜在影响大、难回滚或不确定性高，需要增强审查和验证 |
| `risk:medium` | 存在可控影响或一定不确定性，需要针对性验证 |
| `risk:low` | 影响范围小、容易检查和回退 |

模板中的 `labels` 仅会自动应用已经存在的标签。因此，应先创建 `type:feature`、`type:bug` 和 `type:investigation`，再启用模板。

## 标签使用规则

- 每个 Issue 应有且仅有一个 `type:*` 标签。
- `priority:*` 在初步评估后选择一个；尚未评估时暂不添加。
- `risk:*` 在调查/方案阶段评估后选择一个；尚未评估时暂不添加。
- 不使用 `status:*` 标签；任务状态由后续 GitHub Projects 状态字段管理。
- `priority` 表示处理顺序，`risk` 表示实施控制强度，不得相互替代。
- `type:chore` 和 `type:docs` 适用于人工创建的维护/文档任务；当前没有单独模板，避免模板数量过多。

## 重要说明

- `config.yml` 中 `blank_issues_enabled: false` 用于引导创建者选择模板；仓库维护者仍可能看到仅维护者可用的空白 Issue 入口。
- Issue Forms 的 YAML 标签名必须与仓库中已创建的标签完全一致。
- 本包未设置 assignee、项目编号、Issue Type 或技术栈字段，避免依赖尚未确定的仓库/组织设置。
- 当前 GitHub 文档将 Issue Forms 标注为公开预览；建议检查模板实际渲染效果，并保留 Issue 内容本身作为可读的 Markdown 记录。
