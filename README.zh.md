# Calendo

[English](README.md)

面向 AI Agent 的节假日与工作日服务，每个日期都写明来源。

Calendo 回答模型不该靠猜的日期问题：2025-10-11 在中国要不要上班，2025-09-26 之后的第 3 个工作日是哪天，2025-09-29 到 2025-10-12 有几个工作日，2026 年有哪些连休。每个回答都带上这一天的类型（法定节日、调休休息日、补班日、周末或工作日）、数据的核验程度，以及所依据的数据版本。

## 现状

Calendo 尚未发布，也还没有实现任何回答。本仓库目前包含工程基线（检查、CI、发布流程、变更日志与 RFC 格式），以及 MVP 所依据的[产品背景](docs/product/calendo-mvp.zh.md)。

MVP 计划在同一个 Python 核心之上建三层：

| 层 | 面向 | 计划内容 |
| --- | --- | --- |
| MCP 服务 | Claude、Cursor 等 MCP 客户端中的 AI Agent | 一个公共远程端点，7 个只读工具 |
| HTTP API | 开发者与官网 | `/v1` 下的 7 个只读接口 |
| calendo.day | 正在决定是否接入的开发者 | 单页：接入客户端、试查一个日期、了解数据如何核对 |

中国先行，逐日核对国务院放假通知。其他国家通过同一套工具，由 [holidays](https://github.com/vacanza/holidays) 库给出回答，核对之前一律标注为未核验。服务回答问题时不发起任何网络调用。

## 开发

```sh
uv sync
sh scripts/check.sh
```

[贡献指南](.github/CONTRIBUTING.zh.md)说明了环境准备、检查、工作规则，以及一个改动如何发布。编码 Agent 从 [AGENTS.md](AGENTS.md) 开始读。

| 阅读 | 用途 |
| --- | --- |
| [产品背景](docs/product/calendo-mvp.zh.md) | MVP 是什么，以及仍待决定的问题 |
| [设计 RFC](rfcs/README.zh.md) | 后续工作所依赖的决定 |
| [更新日志](CHANGELOG.zh.md) | 每个版本发布了什么 |
| [安全策略](.github/SECURITY.zh.md) | 如何报告漏洞 |

## 许可

[MIT](LICENSE)
