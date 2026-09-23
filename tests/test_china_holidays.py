from __future__ import annotations

import pytest

from calendo.china_holidays import list_china_holidays


def test_lists_china_holidays_in_date_order() -> None:
    holidays = list_china_holidays(2024)

    assert holidays == sorted(holidays, key=lambda item: item["date"])
    assert {"date": "2024-01-01", "name": "元旦"} in holidays
    assert {"date": "2024-10-01", "name": "国庆节"} in holidays
    assert all(set(item) == {"date", "name"} for item in holidays)


@pytest.mark.parametrize("year", [1949, 10000, 0, -1])
def test_rejects_year_outside_vacanza_range(year: int) -> None:
    with pytest.raises(ValueError, match="between 1950 and 9999"):
        list_china_holidays(year)


def test_keeps_source_labels_for_adjusted_days() -> None:
    holidays = list_china_holidays(2025)

    assert any(item["name"].startswith("休息日（由") for item in holidays)
