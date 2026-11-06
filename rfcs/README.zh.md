# 设计 RFC（CRFC）

[English](README.md)

一份文档一个设计决定，成对出现：`CRFC-NNNN-<slug>.md` 与 `CRFC-NNNN-<slug>.zh.md`。[产品背景](../docs/product/calendo-mvp.zh.md)里的待决问题是背景。起草 RFC 的工作由一条 issue 提出，这条 issue 可以引用其中某个问题。

## 约定

1. **RFC 与它所决定的实现从不放在同一个 pull request。** 两者各自合并；实现按编号引用 RFC。
2. **所有者以 `Status: accepted` 合并 RFC，即为接受。** 在此之前它是 `draft`。Agent 可以起草，从不接受。
3. **已落地的 RFC 很少修改。** 必须修改时，提升版本号，并在 `## Changes` 下列出改动项（`### v1.1.0`，然后是 `- Added…` / `- Removed…` / `- Updated…`），中英文都改。
4. `Status` 取 `draft`、`accepted`、`implemented`、`superseded`、`rejected` 之一。被取代的 RFC 在第一段写明取代它的文档。

`scripts/check_rfcs.py` 检查文件名、成对、编号唯一、必需的小节、`Status`；在 pull request 上还检查修订过的 RFC 是否在两个文件中都提升了版本。

## 结构

复制 [`TEMPLATE.md`](TEMPLATE.md) 与 [`TEMPLATE.zh.md`](TEMPLATE.zh.md)。英文文件包含 `## Summary`、`## Motivation`、`## Guide-level explanation`、`## Reference-level explanation`、`## Drawbacks`、`## Rationale and alternatives`、`## Unresolved questions` 与 `## Changes`；中文文件包含相同的小节，标题翻译、顺序一致，只有 `## Changes` 两边都保留英文标题。

## 索引

编号接着最后一行往下取。

| 文档 | 标题 | 状态 |
| --- | --- | --- |
| [CRFC-0001](CRFC-0001-requirement-flow.zh.md) | 从方向到可开工的 issue | draft |
