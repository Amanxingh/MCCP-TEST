from __future__ import annotations

import logging

import pytest

from gridpulse.logging_utils import configure_logging, timed_operation


def test_configure_logging_does_not_duplicate_handlers():
    logger = configure_logging("DEBUG")
    count = len(logger.handlers)
    logger = configure_logging("DEBUG")
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) == count


def test_timed_operation_logs_completion(caplog):
    logger = configure_logging("INFO")
    with caplog.at_level(logging.INFO, logger="gridpulse"):
        with timed_operation(logger, "report"):
            pass
    assert "report" in caplog.text
    assert "elapsed" in caplog.text


def test_timed_operation_logs_failure(caplog):
    logger = configure_logging("INFO")
    with caplog.at_level(logging.ERROR, logger="gridpulse"):
        with pytest.raises(RuntimeError):
            with timed_operation(logger, "report"):
                raise RuntimeError("boom")
    assert "failed" in caplog.text
