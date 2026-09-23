"""中国法定节假日的数据模型和 vacanza 数据源适配。"""

from __future__ import annotations

from typing import TypedDict

from holidays.countries.china import China

MIN_SUPPORTED_YEAR = 1950
MAX_SUPPORTED_YEAR = 9999


class ChinaHoliday(TypedDict):
    """MCP 对外返回的一条节假日记录。"""

    date: str
    name: str


def list_china_holidays(year: int) -> list[ChinaHoliday]:
    """返回指定年份的中国节假日，按日期升序排列。

    数据来自 vacanza/holidays 的 ``China`` 日历。其记录中的“补假”和
    “调休”标注会原样保留，便于调用方区分来源数据中的休假类型。
    """
    if not MIN_SUPPORTED_YEAR <= year <= MAX_SUPPORTED_YEAR:
        raise ValueError(f"year must be between {MIN_SUPPORTED_YEAR} and {MAX_SUPPORTED_YEAR}")

    holidays = China(years=year)  # type: ignore[no-untyped-call]
    return [
        {"date": holiday_date.isoformat(), "name": name}
        for holiday_date, name in sorted(holidays.items(), key=lambda item: item[0])
    ]
