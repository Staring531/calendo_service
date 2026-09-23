"""Logging setup and gzip-compressed retention for calendo."""

from __future__ import annotations

import gzip
import logging
import os
import shutil
from collections.abc import Callable
from datetime import datetime, timedelta
from pathlib import Path
from typing import Final

DEFAULT_LOG_DIR: Final[Path] = Path("logs")
DEFAULT_LOG_FILENAME: Final[str] = "calendo.log"
DEFAULT_MAX_BYTES: Final[int] = 32 * 1024 * 1024
DEFAULT_RETENTION_DAYS: Final[int] = 7
DEFAULT_LOG_LEVEL: Final[int] = logging.INFO
LOGGER_NAME: Final[str] = "calendo"


class GzipRotatingFileHandler(logging.Handler):
    """Rotate active logs by day or size and compress completed files."""

    def __init__(
        self,
        filename: str | os.PathLike[str],
        *,
        max_bytes: int = DEFAULT_MAX_BYTES,
        retention_days: int = DEFAULT_RETENTION_DAYS,
        encoding: str = "utf-8",
        clock: Callable[[], datetime] = datetime.now,
    ) -> None:
        super().__init__()
        if max_bytes <= 0:
            raise ValueError("max_bytes must be greater than zero")
        if retention_days < 0:
            raise ValueError("retention_days must not be negative")

        self.base_filename = Path(filename)
        self.max_bytes = max_bytes
        self.retention_days = retention_days
        self.encoding = encoding
        self._clock = clock
        self.terminator = "\n"
        self.base_filename.parent.mkdir(parents=True, exist_ok=True)
        self._stream = self.base_filename.open("a", encoding=encoding)
        self._prune(self._clock())

    def emit(self, record: logging.LogRecord) -> None:
        """Write one record, rotating before it would exceed the size limit."""
        try:
            message = self.format(record) + self.terminator
            encoded_message = message.encode(self.encoding)
            now = self._clock()
            if self._should_rollover(len(encoded_message), now):
                self._rollover(now)
            self._stream.write(message)
            self._stream.flush()
        except Exception:
            self.handleError(record)

    def close(self) -> None:
        """Close the active file without rotating it."""
        if not self._stream.closed:
            self._stream.close()
        super().close()

    def _should_rollover(self, message_size: int, now: datetime) -> bool:
        if self.base_filename.stat().st_size == 0:
            return False
        file_date = datetime.fromtimestamp(self.base_filename.stat().st_mtime).date()
        return (
            file_date < now.date()
            or self.base_filename.stat().st_size + message_size > self.max_bytes
        )

    def _rollover(self, now: datetime) -> None:
        self._stream.close()
        if self.base_filename.exists() and self.base_filename.stat().st_size:
            compressed_path = self._compressed_path(now)
            with (
                self.base_filename.open("rb") as source,
                gzip.open(compressed_path, "wb") as target,
            ):
                shutil.copyfileobj(source, target)
            self.base_filename.unlink()
        self._stream = self.base_filename.open("a", encoding=self.encoding)
        self._prune(now)

    def _compressed_path(self, now: datetime) -> Path:
        timestamp = now.strftime("%Y%m%d-%H%M%S-%f")
        candidate = self.base_filename.with_name(f"{self.base_filename.name}.{timestamp}.gz")
        suffix = 1
        while candidate.exists():
            candidate = self.base_filename.with_name(
                f"{self.base_filename.name}.{timestamp}-{suffix}.gz"
            )
            suffix += 1
        return candidate

    def _prune(self, now: datetime) -> None:
        cutoff = now - timedelta(days=self.retention_days)
        for path in self.base_filename.parent.glob(f"{self.base_filename.name}.*.gz"):
            if datetime.fromtimestamp(path.stat().st_mtime) < cutoff:
                path.unlink()


def configure_logging(
    *,
    log_dir: str | os.PathLike[str] | None = None,
    max_bytes: int | None = None,
    retention_days: int | None = None,
    level: int = DEFAULT_LOG_LEVEL,
) -> logging.Logger:
    """Configure the calendo logger and return it.

    The existing handler is reused so calling this once from each transport
    entry point does not duplicate records.
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    logger.propagate = False
    selected_dir = (
        Path(log_dir)
        if log_dir is not None
        else Path(os.getenv("CALENDO_LOG_DIR") or DEFAULT_LOG_DIR)
    )
    log_path = selected_dir / DEFAULT_LOG_FILENAME
    selected_max_bytes = (
        max_bytes
        if max_bytes is not None
        else int(os.getenv("CALENDO_LOG_MAX_BYTES", str(DEFAULT_MAX_BYTES)))
    )
    selected_retention_days = (
        retention_days
        if retention_days is not None
        else int(os.getenv("CALENDO_LOG_RETENTION_DAYS", str(DEFAULT_RETENTION_DAYS)))
    )
    for handler in tuple(logger.handlers):
        if isinstance(handler, GzipRotatingFileHandler) and handler.base_filename != log_path:
            logger.removeHandler(handler)
            handler.close()
    if not any(
        isinstance(handler, GzipRotatingFileHandler) and handler.base_filename == log_path
        for handler in logger.handlers
    ):
        file_handler = GzipRotatingFileHandler(
            log_path,
            max_bytes=selected_max_bytes,
            retention_days=selected_retention_days,
        )
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
        )
        logger.addHandler(file_handler)
    return logger
