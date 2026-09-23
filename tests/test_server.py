from __future__ import annotations

import asyncio

from calendo.server import china_public_holidays, mcp


def test_registers_china_public_holidays_tool() -> None:
    tools = asyncio.run(mcp.list_tools())

    assert [tool.name for tool in tools] == ["china_public_holidays"]


def test_tool_returns_serializable_holiday_records() -> None:
    holidays = china_public_holidays(2024)

    assert holidays[0] == {"date": "2024-01-01", "name": "元旦"}
