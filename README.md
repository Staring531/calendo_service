# calendo

> 跨国公共假日 MCP 服务，面向 AI agent/LLM 客户端，支持多语言

## 环境要求

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/)

## 快速开始

```bash
# 安装依赖（含 dev 依赖）
make sync

# 跑测试
make test

# lint + 格式化
make format

# 提交前一次性检查（lint + typecheck + test）
make check
```

### HTTP MCP server

Start the Streamable HTTP MCP server on `127.0.0.1:8000`:

```bash
uv run calendo-http
```

The MCP endpoint is `http://127.0.0.1:8000/mcp`. Bind a different address or
port with `--host` and `--port`; use `--transport sse` for legacy SSE clients.
The same settings are available through `CALENDO_HTTP_HOST`,
`CALENDO_HTTP_PORT`, and `CALENDO_HTTP_TRANSPORT`.

### Logging

Server startup and holiday queries are written to `logs/calendo.log` by
default. The active file rotates at 32 MiB or on a calendar-day change;
completed files are gzip-compressed and files older than 7 days are removed.
Set `CALENDO_LOG_DIR`, `CALENDO_LOG_MAX_BYTES`, and
`CALENDO_LOG_RETENTION_DAYS` to override these defaults.

更多命令见 `make help`。

## 项目结构

```
src/calendo/   # 核心代码（src-layout）
tests/                     # 测试
pyproject.toml             # 项目元数据 + 构建系统 + ruff/mypy/pytest 配置
Makefile                   # 常用命令入口
.python-version            # uv 自动读取的 Python 版本
```

## 开发规范

- 代码检查/格式化统一用 `ruff`（替代 flake8 + isort + black）
- 类型检查用 `mypy`（strict 模式）
- 依赖管理统一用 `uv add` / `uv remove`，不要手改 `pyproject.toml` 里的依赖数组

## License

MIT
