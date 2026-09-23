"""calendo MCP server and tool registration."""

from __future__ import annotations

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


if __name__ == "__main__":
    main()
