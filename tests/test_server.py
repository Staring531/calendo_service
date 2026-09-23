from __future__ import annotations

import asyncio

import pytest

from calendo.server import china_public_holidays, mcp, run_http_server


def test_registers_china_public_holidays_tool() -> None:
    tools = asyncio.run(mcp.list_tools())

    assert [tool.name for tool in tools] == ["china_public_holidays"]


def test_tool_returns_serializable_holiday_records() -> None:
    holidays = china_public_holidays(2024)

    assert holidays[0] == {"date": "2024-01-01", "name": "元旦"}


def test_streamable_http_app_exposes_mcp_endpoint() -> None:
    app = mcp.streamable_http_app()

    assert any(getattr(route, "path", None) == "/mcp" for route in app.routes)


@pytest.mark.parametrize("port", [0, 65536, -1])
def test_http_server_rejects_invalid_ports(port: int) -> None:
    with pytest.raises(ValueError, match="port must be between"):
        run_http_server(port=port)
