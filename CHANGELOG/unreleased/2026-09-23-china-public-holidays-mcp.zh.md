# 新增中国法定节假日 MCP 工具

- **Date:** 2026-09-23
- **Type:** feature
- **Scope:** `china_holidays`, `server`, `tests`

[English](2026-09-23-china-public-holidays-mcp.md)

## 变更内容

- 新增按年份查询中国节假日的 `china_public_holidays` MCP 工具。
- 新增 vacanza/holidays 适配层，返回 ISO 日期并保留数据源名称。
- 新增 stdio 入口 `calendo` 和参数校验测试。
