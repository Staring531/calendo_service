# Add bounded gzip-compressed application logging

- **Date:** 2026-09-23
- Status: Accepted

## Context

The MCP server needs operational logs for startup and holiday queries without
allowing an unattended deployment to grow its log directory indefinitely.
stdio transport also reserves stdout for the MCP protocol, so application
logging must avoid writing there.

## Decision

Write calendo application events to `logs/calendo.log` by default and use a
custom standard-library handler that rotates before the active file exceeds
32 MiB or when the calendar day changes. Every completed file is compressed to
gzip, and compressed files older than 7 days are removed. The log directory
can be changed with `CALENDO_LOG_DIR`; `CALENDO_LOG_MAX_BYTES` and
`CALENDO_LOG_RETENTION_DAYS` override the rotation defaults. The handler
writes UTF-8 records and does not write application logs to stdout.

## Consequences

Log storage is bounded by age and each active file has a predictable size
limit. Compressed files are slightly harder to inspect manually but preserve
disk space and remain readable with standard gzip tools. Rotation occurs when
the next record arrives after a day boundary, so an idle service does not
create empty daily files.
