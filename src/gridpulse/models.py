
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

TS_FORMAT = "%Y-%m-%d %H:%M"


def parse_ts(value: str) -> datetime:
    """Parse a timestamp using the project's standard format."""
    return datetime.strptime(value, TS_FORMAT)


@dataclass(frozen=True)
class Meter:
    meter_id: str
    feeder_id: str
    region: str
    customer_count: int
    status: str


@dataclass(frozen=True)
class OutageEvent:
    event_id: int
    meter_id: str
    feeder_id: str
    region: str
    started_at: str
    restored_at: str | None
    cause: str
    reported_customers: int

    def duration_minutes(self, as_of: str | None = None) -> int:
        """Return elapsed outage minutes, using as_of for active events.

        Parse timestamps, handle active events, reject an impossible
        restoration time, and return whole minutes.
        """
        start = parse_ts(self.started_at)

        if self.restored_at is not None:
            end = parse_ts(self.restored_at)

            if end < start:
                raise ValueError(
                    "Restoration time cannot be before start time"
                )
        else:
            if as_of is None:
                raise ValueError(
                    "as_of is required for an active outage"
                )

            end = parse_ts(as_of)

            if end < start:
                raise ValueError(
                    "as_of cannot be before start time"
                )

        return int((end - start).total_seconds() // 60)

    def __str__(self) -> str:
        return (
            f"Event({self.event_id}, "
            f"meter={self.meter_id}, cause={self.cause})"
        )

    def __lt__(self, other: "OutageEvent") -> bool:
        if not isinstance(other, OutageEvent):
            return NotImplemented

        return (self.started_at, self.event_id) < (
            other.started_at,
            other.event_id,
        )
