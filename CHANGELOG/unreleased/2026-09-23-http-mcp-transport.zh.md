# 新增 HTTP MCP 服务入口

- **Date:** 2026-09-23
- **Type:** feature
- **Scope:** `server`, `tests`, `docs`

[English](2026-09-23-http-mcp-transport.md)

## 变更内容

- 新增面向 Streamable HTTP MCP 客户端的 `calendo-http` 入口。
- 新增 `/mcp` endpoint，并支持配置主机、端口和 SSE 兼容 transport。
- 补充 HTTP 启动命令和环境变量文档。
