"""calendo MCP server and tool registration."""

from __future__ import annotations

import argparse
import os
from typing import Literal

from mcp.server.fastmcp import FastMCP

from calendo.china_holidays import ChinaHoliday, list_china_holidays

mcp = FastMCP(
    "calendo",
    instructions="提供全球公共节假日数据；当前支持中国法定节假日。",
)


@mcp.tool(
    name="china_public_holidays",
    description="根据年份返回中国法定节假日列表，日期采用 YYYY-MM-DD 格式。",
)
def china_public_holidays(year: int) -> list[ChinaHoliday]:
    """根据年份返回中国法定节假日列表。"""
    return list_china_holidays(year)


def main() -> None:
    """Run the MCP server over stdio for local agent integrations."""
    mcp.run(transport="stdio")


HttpTransport = Literal["streamable-http", "sse"]


def run_http_server(
    *,
    host: str = "127.0.0.1",
    port: int = 8000,
    transport: HttpTransport = "streamable-http",
) -> None:
    """Run the MCP server over an HTTP transport.

    Streamable HTTP is the default and serves the MCP endpoint at ``/mcp``.
    SSE remains available for clients that have not migrated to the newer
    transport.
    """
    if not host:
        raise ValueError("host must not be empty")
    if not 1 <= port <= 65535:
        raise ValueError("port must be between 1 and 65535")
    mcp.settings.host = host
    mcp.settings.port = port
    mcp.run(transport=transport)


def http_main() -> None:
    """Run the HTTP MCP server from command-line arguments or environment."""
    parser = argparse.ArgumentParser(description="Run calendo as an HTTP MCP server")
    parser.add_argument(
        "--host",
        default=os.getenv("CALENDO_HTTP_HOST", "127.0.0.1"),
        help="HTTP bind address (default: CALENDO_HTTP_HOST or 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("CALENDO_HTTP_PORT", "8000")),
        help="HTTP bind port (default: CALENDO_HTTP_PORT or 8000)",
    )
    parser.add_argument(
        "--transport",
        choices=("streamable-http", "sse"),
        default=os.getenv("CALENDO_HTTP_TRANSPORT", "streamable-http"),
        help="HTTP MCP transport (default: streamable-http)",
    )
    args = parser.parse_args()
    run_http_server(host=args.host, port=args.port, transport=args.transport)


if __name__ == "__main__":
    main()
