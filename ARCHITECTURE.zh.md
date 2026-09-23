# ARCHITECTURE.zh.md

> English version: [ARCHITECTURE.md](ARCHITECTURE.md)。

## 这是什么系统

calendo 是一个支持离线部署的 MCP 服务，向 AI agent 和 LLM 客户端提供公共节假日数据。第一个实现通过 vacanza/holidays 提供中国节假日。数据源和协议决策见 [ADR-0001](docs/decisions/2026-09-23-0001-china-holidays-mcp.md)。

## 组成部分

- **节假日数据源适配器**：将 vacanza/holidays 的中国日历记录转换为稳定的 ISO 日期 JSON 记录。见 [ADR-0001](docs/decisions/2026-09-23-0001-china-holidays-mcp.md)。
- **MCP 服务**：注册 `china_public_holidays` 工具并通过 stdio 提供服务。见 [ADR-0001](docs/decisions/2026-09-23-0001-china-holidays-mcp.md)。

## 部署模式

当前入口通过 stdio 提供 MCP 服务。节假日数据随依赖本地安装，运行时不需要访问在线节假日 API。

## 这份文档不是什么

这是当前架构决策的快照，不是实现指南。想知道某个决定"为什么"这样做，
去看它链接的那份ADR——这份文档只说"现在是什么样"，不解释理由。
