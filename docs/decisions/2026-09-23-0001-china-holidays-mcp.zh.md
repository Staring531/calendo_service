# 使用 vacanza/holidays 实现第一个中国节假日 MCP 工具

- **Date:** 2026-09-23
- Status: Accepted

## Context

calendo 需要第一个面向用户的 MCP 工具，以及一个支持离线部署的中国法定节假日数据源。数据源需要覆盖历史年份且不依赖在线 API，同时 MCP 边界应返回稳定的小型 JSON 结构，避免暴露第三方对象。

## Decision

使用 vacanza 的 `holidays` 包作为数据源，并用 Python MCP SDK 注册
`china_public_holidays` 工具。工具接收年份，返回包含 ISO `date` 和数据源 `name` 字段的记录，并按日期排序。支持年份范围遵循中国日历的 1950-9999 范围。数据源对调休和补假的标注原样保留。

## Consequences

依赖安装完成后，第一个工具可以离线工作，并受益于 vacanza 持续维护的中国日历数据。调用方依赖两个字段组成的 JSON 记录结构；数据源覆盖范围或名称变化会直接反映在返回值中，可能需要同步更新测试夹具。在明确迁移 MCP 集成前，SDK 约束在 1.x API。
