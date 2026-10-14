
from __future__ import annotations

import functools
import logging
import re
from collections.abc import Iterable, Iterator
from typing import Any

from .models import OutageEvent

CAUSE_MULTIPLIERS = {"storm": 1.5, "equipment": 1.2, "vegetation": 1.1}
FEEDER_PATTERN = r"^F-[A-Za-z][A-Za-z0-9]*$"


class OutageDataError(ValueError):
    """Raised when outage input data is invalid."""


def log_call(logger: logging.Logger):
    """Return a decorator that logs function entry, success, and failure.

    TODO(candidate): preserve the wrapped function metadata with functools.wraps.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info("Function entered: %s", func.__name__)
            try:
                result = func(*args, **kwargs)
            except Exception:
                logger.exception("Function failed: %s", func.__name__)
                raise
            logger.info("Function completed: %s", func.__name__)
            return result

        return wrapper

    return decorator


class OutageAnalyzer:
    def __init__(self, cause_multipliers: dict[str, float] | None = None):
        self.cause_multipliers = (
            cause_multipliers
            if cause_multipliers is not None
            else CAUSE_MULTIPLIERS
        )

    def priority_score(self, event: OutageEvent, as_of: str | None = None) -> float:
        """Score an event as duration_minutes * customers * cause multiplier.

        TODO(candidate): reject unknown causes with OutageDataError.
        """
        multiplier = self.cause_multipliers.get(event.cause)

        if multiplier is None:
            raise OutageDataError(f"Unknown outage cause: {event.cause}")

        duration = event.duration_minutes(as_of=as_of)

        return float(
            duration * event.reported_customers * multiplier
        )

    def classify_event(self, event: OutageEvent, as_of: str | None = None) -> str:
        """Classify as active, brief (<30), standard (<120), or extended."""
        if event.restored_at is None:
            return "active"

        duration = event.duration_minutes(as_of=as_of)

        if duration < 30:
            return "brief"
        if duration < 120:
            return "standard"
        return "extended"

    def high_priority_events(
        self,
        events: Iterable[OutageEvent],
        minimum_score: float,
        as_of: str | None = None,
    ) -> Iterator[OutageEvent]:
        """Yield events at or above minimum_score in descending score order.

        TODO(candidate): implement as a generator.
        """
        scored_events = (
            (self.priority_score(event, as_of), event)
            for event in events
        )

        eligible = (
            (score, event)
            for score, event in scored_events
            if score >= minimum_score
        )

        yield from (
            event
            for _, event in sorted(
                eligible,
                key=lambda item: (
                    -item[0],
                    item[1].started_at,
                    item[1].event_id,
                ),
            )
        )


_FEEDER_REGEX = re.compile(FEEDER_PATTERN)


def parse_feeder_code(feeder_id: str) -> str:
    """Validate F-Name feeder codes and return the normalized code.

    TODO(candidate): use a compiled regex; reject bad input with OutageDataError.
    """
    if not isinstance(feeder_id, str):
        raise OutageDataError("Feeder code must be a string")

    normalized = feeder_id.strip()

    if not _FEEDER_REGEX.fullmatch(normalized):
        raise OutageDataError(f"Invalid feeder code: {feeder_id!r}")

    return normalized


def summarize_regions(events: Iterable[OutageEvent]) -> dict[str, int]:
    """Return affected-customer totals by region.

    TODO(candidate): use map/filter/zip or another functional style without
    mutating the input iterable.
    """
    event_list = list(events)

    regions = map(lambda event: event.region, event_list)
    customers = map(
        lambda event: event.reported_customers,
        event_list,
    )

    totals: dict[str, int] = {}

    for region, count in zip(regions, customers):
        totals[region] = totals.get(region, 0) + count

    return totals