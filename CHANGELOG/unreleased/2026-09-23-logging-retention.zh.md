# 新增有界应用日志

- **Date:** 2026-09-23
- **Type:** feature
- **Scope:** `log_config`, `server`, `tests`, `docs`

[English](2026-09-23-logging-retention.md)

## 变更内容

- 新增服务启动和节假日查询应用日志。
- 新增 32 MiB 大小轮转和按日历日轮转，并使用 gzip 压缩。
- 新增压缩日志默认 7 天保留策略和 `CALENDO_LOG_DIR` 配置。
