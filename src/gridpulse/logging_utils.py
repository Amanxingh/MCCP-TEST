
from __future__ import annotations

import logging
import time
from contextlib import contextmanager
from typing import Iterator


def configure_logging(level: str = "INFO") -> logging.Logger:
    """Configure and return the gridpulse logger.

    TODO(candidate): use logging (not print), support level names, and avoid
    adding duplicate handlers when called repeatedly.
    """
    logger = logging.getLogger("gridpulse")

    # Support level names such as DEBUG, INFO, WARNING, ERROR, and CRITICAL.
    log_level = getattr(logging, level.upper(), None)

    if not isinstance(log_level, int):
        raise ValueError(f"Invalid logging level: {level}")

    logger.setLevel(log_level)

    # Avoid adding duplicate handlers when called repeatedly.
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.propagate = False

    return logger


@contextmanager
def timed_operation(logger: logging.Logger, name: str) -> Iterator[None]:
    """Log the elapsed time for an operation.

    TODO(candidate): yield inside the context and always log completion or failure.
    """
    start_time = time.perf_counter()

    try:
        yield
    except Exception:
        elapsed = time.perf_counter() - start_time
        logger.exception(
            "Operation failed",
            extra={
                "operation": name,
                "elapsed_seconds": round(elapsed, 6),
                "status": "failed",
            },
        )
        raise
    else:
        elapsed = time.perf_counter() - start_time
        logger.info(
            "Operation completed",
            extra={
                "operation": name,
                "elapsed_seconds": round(elapsed, 6),
                "status": "completed",
            },
        )
