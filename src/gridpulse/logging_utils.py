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
    raise NotImplementedError("TODO: configure logging")


@contextmanager
def timed_operation(logger: logging.Logger, name: str) -> Iterator[None]:
    """Log the elapsed time for an operation.

    TODO(candidate): yield inside the context and always log completion or failure.
    """
    raise NotImplementedError("TODO: implement timed operation")
