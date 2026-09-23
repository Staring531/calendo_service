# 增加有界的 gzip 压缩应用日志

- **Date:** 2026-09-23
- Status: Accepted

## Context

MCP 服务需要记录启动和节假日查询事件，以便运维排查，同时不能让无人值守的部署无限增长日志目录。stdio transport 将 stdout 保留给 MCP 协议，因此应用日志不能写入 stdout。

## Decision

默认将 calendo 应用事件写入 `logs/calendo.log`，使用标准库自定义 handler，在活动文件超过 32 MiB 或日历日期变化前轮转。每个完成轮转的文件都压缩为 gzip，并删除超过 7 天的压缩文件。可通过 `CALENDO_LOG_DIR` 修改日志目录，并通过 `CALENDO_LOG_MAX_BYTES` 和 `CALENDO_LOG_RETENTION_DAYS` 覆盖轮转默认值；handler 使用 UTF-8 写入，应用日志不写入 stdout。

## Consequences

日志存储按时间受控，活动文件也有明确大小上限。压缩文件不便于直接人工查看，但可以节省磁盘空间，并能用标准 gzip 工具读取。服务空闲时不会创建空的每日文件，日期变化后的下一条日志到达时才会触发轮转。
