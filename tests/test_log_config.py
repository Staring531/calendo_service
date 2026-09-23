from __future__ import annotations

import gzip
import logging
import os
from datetime import datetime, timedelta

import pytest

from calendo.log_config import GzipRotatingFileHandler, configure_logging


def _record(message: str) -> logging.LogRecord:
    return logging.LogRecord("test", logging.INFO, __file__, 1, message, (), None)


def test_rotates_by_size_and_compresses_previous_file(tmp_path) -> None:
    log_path = tmp_path / "calendo.log"
    handler = GzipRotatingFileHandler(log_path, max_bytes=10)
    handler.setFormatter(logging.Formatter("%(message)s"))
    try:
        handler.emit(_record("12345"))
        handler.emit(_record("67890"))
        handler.emit(_record("x"))
    finally:
        handler.close()

    compressed = list(tmp_path.glob("calendo.log.*.gz"))
    assert len(compressed) == 1
    with gzip.open(compressed[0], "rt", encoding="utf-8") as stream:
        assert stream.read() == "12345\n"
    assert log_path.read_text(encoding="utf-8") == "67890\nx\n"


def test_rotates_when_calendar_day_changes(tmp_path) -> None:
    current = datetime(2026, 9, 23, 12)
    handler = GzipRotatingFileHandler(tmp_path / "calendo.log", clock=lambda: current)
    handler.setFormatter(logging.Formatter("%(message)s"))
    try:
        handler.emit(_record("day one"))
        timestamp = current.timestamp()
        os.utime(tmp_path / "calendo.log", (timestamp, timestamp))
        current = current + timedelta(days=1)
        handler.emit(_record("day two"))
    finally:
        handler.close()

    compressed = list(tmp_path.glob("calendo.log.*.gz"))
    assert len(compressed) == 1
    with gzip.open(compressed[0], "rt", encoding="utf-8") as stream:
        assert stream.read() == "day one\n"


def test_prunes_compressed_logs_older_than_retention(tmp_path) -> None:
    old_log = tmp_path / "calendo.log.20260901-000000-000000.gz"
    old_log.write_bytes(gzip.compress(b"old\n"))
    old_timestamp = datetime.now().timestamp() - 8 * 24 * 60 * 60
    os.utime(old_log, (old_timestamp, old_timestamp))

    handler = GzipRotatingFileHandler(tmp_path / "calendo.log", retention_days=7)
    handler._prune(datetime.now())
    handler.close()

    assert not old_log.exists()


def test_rejects_invalid_rotation_settings(tmp_path) -> None:
    with pytest.raises(ValueError, match="max_bytes"):
        GzipRotatingFileHandler(tmp_path / "calendo.log", max_bytes=0)
    with pytest.raises(ValueError, match="retention_days"):
        GzipRotatingFileHandler(tmp_path / "calendo.log", retention_days=-1)


def test_configure_logging_reuses_file_handler(tmp_path) -> None:
    logger = configure_logging(log_dir=tmp_path)
    same_logger = configure_logging(log_dir=tmp_path)

    assert logger is same_logger
    assert sum(isinstance(handler, GzipRotatingFileHandler) for handler in logger.handlers) == 1
    for handler in logger.handlers:
        handler.close()
    logger.handlers.clear()


def test_configure_logging_reads_rotation_environment(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("CALENDO_LOG_MAX_BYTES", "4096")
    monkeypatch.setenv("CALENDO_LOG_RETENTION_DAYS", "3")

    logger = configure_logging(log_dir=tmp_path)
    handler = next(
        handler for handler in logger.handlers if isinstance(handler, GzipRotatingFileHandler)
    )

    assert handler.max_bytes == 4096
    assert handler.retention_days == 3
    handler.close()
    logger.handlers.clear()
