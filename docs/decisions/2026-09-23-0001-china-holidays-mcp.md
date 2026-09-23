# Use vacanza/holidays for the first China holidays MCP tool

- **Date:** 2026-09-23
- Status: Accepted

## Context

calendo needs its first user-facing MCP tool and an offline-capable source of
China public holiday data. The source must cover historical years without
requiring a live API, while the MCP boundary should expose a small stable JSON
shape rather than third-party objects.

## Decision

Use the `holidays` package from vacanza as the source and register a
`china_public_holidays` tool with the Python MCP SDK. The tool accepts a year
and returns records containing ISO `date` and source-provided `name` fields,
sorted by date. The supported year range follows the China calendar's
1950-9999 range. Source labels for adjusted and substitute rest days are
preserved.

## Consequences

The first tool works offline after dependency installation and benefits from
vacanza's maintained China calendar data. Consumers depend on the two-field
JSON record shape, while changes to source coverage or labels remain visible
in returned data and may require fixture updates. The MCP SDK is constrained
to its 1.x API until the server integration is deliberately migrated.
