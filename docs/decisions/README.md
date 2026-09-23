# docs/decisions/ — ADR rules

> Chinese version: [README.zh.md](README.zh.md).

ADRs in this directory follow Michael Nygard's 2011 format (Title /
Status / Context / Decision / Consequences), a de facto industry
standard (used by adr-tools, and widely at AWS, Azure). This document is
generic and can be dropped into any project as-is; project-specific
context belongs in that project's own AGENTS.md.

## What counts as "architectural," requiring an ADR

Nygard's own definition: a decision counts as architectural if it
affects a system's **structure, non-functional characteristics,
dependencies, interfaces, or construction techniques**.

A more operational version — open an ADR if any of these apply:

- You picked one of several viable technical approaches, ruling out the
  others
- It changes system structure (adding/removing a component, or shifting
  a module boundary)
- It locks in a data source, protocol, or dependency that would be
  expensive to change later
- It explicitly accepts a tradeoff

**When an ADR is not needed**: the decision is reversible within one
iteration, affects only a single module's internals, or is a routine
implementation choice (e.g. swapping a logging library). Writing ADRs
for too many trivial decisions dilutes the visibility of the truly
important ones.

## Resolving ambiguous cases

When it's genuinely unclear, use Olaf Zimmermann's **Architectural
Significance Test** — seven criteria (a judgment checklist, not a
scoring tool, per Zimmermann's own framing):

1. Direct impact on business value or business risk?
2. Something a key stakeholder explicitly cares about?
3. A runtime quality requirement an order of magnitude above what the
   current architecture already meets?
4. Involves an external dependency that's uncontrollable or
   unpredictable?
5. Cuts across multiple parts of the system (e.g. security, monitoring)?
6. First time this team has done this kind of thing?
7. Bitten by a similar problem before?

The first five are relatively objective; the last two are highly
context-dependent. If you're still unsure after running through these,
the default action is to write a lightweight **Y-Statement** first
("In the context of X, facing Y, we decided Z, to achieve W, accepting
V as a cost") rather than skipping the record entirely — this can be
upgraded to a full ADR later.

## Status flow

`Proposed → Accepted`, later possibly `Deprecated` or `Superseded by
ADR-XXXX`.

- **Proposed**: the decision has been put forward, not yet validated
  (e.g. no prototype yet)
- **Accepted**: the decision is in effect; code changes should follow it
- **Deprecated**: no longer applicable, not directly replaced by another
  ADR
- **Superseded by ADR-XXXX**: replaced by a newer decision — name which
  one

## Who can move Proposed to Accepted

Depends on whether the project is team-run or solo-maintained — no
universal answer. Fill this in per-project.

## File naming and directory structure

**Format**: `YYYY-MM-DD-NNNN-short-clear-title.md` (English, the
default version), paired with a `YYYY-MM-DD-NNNN-short-clear-title.zh.md`
(Chinese version).

- Number prefix (`NNNN-title.md`): Nygard/adr-tools' standard approach
- Date prefix: used by the joelparkerhenderson.com family of ADR
  repositories (`YYYY-MM-DD Title.md`), intended for ISO-sortable dates;
  in that family, date and number are an either/or choice, not stacked
- `.en.md` / `.zh.md` bilingual suffix: a real precedent from
  PenguinHarness itself (`architecture.en.md`, `skills.{en,zh}.md`, etc.)
- "Date + number" combined: no external project found using this
  combination as-is — it's this document's own design, stitching
  together the two verified conventions above, not a widely adopted
  external practice
- ADR naming is allowed to be project-specific, not a mandatory single
  format (per jamesmh/architecture_decision_record's own stance) — the
  scheme above is this project's choice, not the only correct answer

**Fixed template**: see `ADR-TEMPLATE.md` (English) and `ADR-TEMPLATE.zh.md`
(Chinese) in this directory. Copy these when starting a new ADR — don't
write one from scratch.
