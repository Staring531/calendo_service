# Add HTTP transports for the MCP server

- **Date:** 2026-09-23
- Status: Accepted

## Context

The first calendo tool is available over stdio, which is suitable for local
agent processes but not for remote or containerized clients. MCP clients need
an HTTP endpoint that can be configured without changing the holiday tool.

## Decision

Add a `calendo-http` entry point using the MCP SDK's Streamable HTTP transport.
Serve the endpoint at `/mcp`, bind to `127.0.0.1:8000` by default, and allow
the host, port, and transport to be configured with command-line arguments or
`CALENDO_HTTP_HOST`, `CALENDO_HTTP_PORT`, and `CALENDO_HTTP_TRANSPORT`. Support
the SDK's SSE transport as an explicit compatibility option. Keep the stdio
entry point unchanged.

## Consequences

Remote and containerized MCP clients can connect through a standard HTTP
endpoint. Deployment configuration is explicit and remains local by default;
operators must choose a non-loopback host and configure network protection
when exposing the service beyond the local machine. The tool implementation
and holiday data source are shared by both transports.
