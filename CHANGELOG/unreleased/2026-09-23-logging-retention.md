# Add bounded application logging

- **Date:** 2026-09-23
- **Type:** feature
- **Scope:** `log_config`, `server`, `tests`, `docs`

[中文版](2026-09-23-logging-retention.zh.md)

## What changed

- Added startup and holiday-query application logs.
- Added 32 MiB size and calendar-day rotation with gzip compression.
- Added seven-day compressed-log retention and `CALENDO_LOG_DIR` configuration.
