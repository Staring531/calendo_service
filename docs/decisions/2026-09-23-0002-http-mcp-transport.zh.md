# 为 MCP 服务增加 HTTP 传输

- **Date:** 2026-09-23
- Status: Accepted

## Context

第一个 calendo 工具通过 stdio 提供服务，适合本地 agent 进程，但不适合远程或容器化客户端。MCP 客户端需要一个无需修改节假日工具即可配置的 HTTP endpoint。

## Decision

新增使用 MCP SDK Streamable HTTP transport 的 `calendo-http` 入口。在 `/mcp` 提供 endpoint，默认监听 `127.0.0.1:8000`，并允许通过命令行参数或 `CALENDO_HTTP_HOST`、`CALENDO_HTTP_PORT`、`CALENDO_HTTP_TRANSPORT` 配置主机、端口和 transport。支持显式选择 SDK 的 SSE transport 作为兼容选项。保持 stdio 入口不变。

## Consequences

远程和容器化 MCP 客户端可以通过标准 HTTP endpoint 连接。服务默认仅本机监听，若暴露到本机之外，运维人员必须选择非 loopback 主机并配置网络防护。两种 transport 共享同一工具实现和节假日数据源。
