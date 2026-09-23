# ARCHITECTURE.md

> Chinese version: [ARCHITECTURE.zh.md](ARCHITECTURE.zh.md).

## What this system is

calendo is an offline-capable MCP server that exposes public holiday data to
AI agent and LLM clients. The first implementation serves China holidays from
vacanza/holidays. See [ADR-0001](docs/decisions/2026-09-23-0001-china-holidays-mcp.md)
for the source and protocol decision.

## Components

- **Holiday source adapter**: Converts vacanza/holidays China records into
  stable ISO-date JSON records. See
  [ADR-0001](docs/decisions/2026-09-23-0001-china-holidays-mcp.md).
- **MCP server**: Registers `china_public_holidays` and serves it over stdio
  or Streamable HTTP (`/mcp`).
  See [ADR-0001](docs/decisions/2026-09-23-0001-china-holidays-mcp.md).
- **Logging**: Writes timestamped server events to a size- and day-rotated log,
  compresses completed files with gzip, and retains seven days by default. See
  [ADR-0003](docs/decisions/2026-09-23-0003-logging-retention.md).

## Deployment modes

The `calendo` entry point serves MCP over stdio. The `calendo-http` entry point
serves Streamable HTTP on `/mcp` by default and can optionally serve SSE. The
holiday data is packaged locally, so runtime access to a holiday API is not
required.

## What this document is not

This is a snapshot of current architectural decisions, not an
implementation guide. For *why* a given decision was made, read the ADR
it links to — this document only states *what* the current shape is.
