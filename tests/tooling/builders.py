"""Builders shared by the repository-tooling tests: well-formed entry pairs and RFC pairs."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

EN_ENTRY = """\
# Working days count both ends

- **Date:** 2026-11-05
- **Type:** feature
- **Scope:** `core`, `http`
- **PR:** [#12](https://github.com/Staring531/calendo_service/pull/12)

[中文版](2026-11-05-inclusive-ranges.zh.md)

`count_workdays` counted both ends of the range.

## Details

- 2025-09-29 to 2025-10-12 returned 5.
"""

ZH_ENTRY = """\
# 工作日计数包含两端

- **Date:** 2026-11-05
- **Type:** feature
- **Scope:** `core`, `http`
- **PR:** [#12](https://github.com/Staring531/calendo_service/pull/12)

[English](2026-11-05-inclusive-ranges.md)

`count_workdays` 改为包含区间两端。

## 细节

- 2025-09-29 到 2025-10-12 返回 5。
"""

STEM = "2026-11-05-inclusive-ranges"

EN_RFC = """\
# CRFC-0001 Day types

- Status: draft
- Start Date: 2026-11-05

[中文版](CRFC-0001-day-types.zh.md)

## Summary
s
## Motivation
m
## Guide-level explanation
g
## Reference-level explanation
r
## Drawbacks
d
## Rationale and alternatives
a
## Unresolved questions
u

---

## Changes

### v1.0.0

- Initial version
"""

ZH_RFC = """\
# CRFC-0001 日期类型

- Status: draft
- Start Date: 2026-11-05

[English](CRFC-0001-day-types.md)

## 摘要
s
## 动机
m
## 指南级说明
g
## 参考级说明
r
## 缺点
d
## 理由与备选方案
a
## 未决问题
u

---

## Changes

### v1.0.0

- 初始版本
"""


def write_pair(directory: Path, en: str = EN_ENTRY, zh: str = ZH_ENTRY, stem: str = STEM) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{stem}.md").write_text(en, encoding="utf-8")
    (directory / f"{stem}.zh.md").write_text(zh, encoding="utf-8")
    return directory


def write_rfc(directory: Path, en: str = EN_RFC, zh: str = ZH_RFC) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "CRFC-0001-day-types.md").write_text(en, encoding="utf-8")
    (directory / "CRFC-0001-day-types.zh.md").write_text(zh, encoding="utf-8")
    return directory


Git = Callable[..., str]
