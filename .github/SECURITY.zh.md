# 安全策略

[English](SECURITY.md)

## 支持的版本

Calendo 尚未发布。从首个版本起，它从 `main` 发布，没有维护分支：修复进入下一个版本，只支持最新的版本。

## 报告漏洞

请通过 GitHub 的[「Report a vulnerability」](https://github.com/Staring531/calendo_service/security/advisories/new)表单私下报告。它会创建一份只有维护者可见的草稿安全公告，让报告、修复和披露保持在一起。安全问题不要发公开 issue 或 pull request。

报告里最有用的信息是：受影响的版本或 commit，在哪里运行（公共端点、官网，还是本地），以及能复现问题的最小请求。收到报告后几天内会确认，随后给出影响评估。

## 范围

Calendo 是一个只读服务，无需认证即可回答日期问题。在这一设计之内，以下属于安全问题：

- 某个请求让服务访问了网络、读取了自身数据以外的文件，或运行了它本不该运行的东西。
- 单个请求的开销与其回答严重不成比例，例如占满一个 worker，或让内存无限增长。
- 输入以数据以外的身份到达 MCP 客户端或官网：通过参数夹带、又被原样返回的标记或指令。
- 发布资产与 tag 的源码或随附的 `SHA256SUMS` 不一致；凭据暴露在仓库、CI 日志或发布中。

以下不属于安全问题：

- Calendo 判定错的日期。这是数据缺陷，请用[数据表单](https://github.com/Staring531/calendo_service/issues/new?template=data.yml)报告。
- 针对公共端点的请求量。请报告本身开销就很大的单个请求，而不是大量廉价请求。
- 依赖（例如 `holidays`）中无法经由 Calendo 触达的漏洞。请报告给该依赖的维护者。
