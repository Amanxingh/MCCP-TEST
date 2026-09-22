from __future__ import annotations

import sqlite3
from typing import Any

from .models import OutageEvent

EVENT_SELECT = """
SELECT e.event_id, e.meter_id, m.feeder_id, m.region, e.started_at,
       e.restored_at, e.cause, e.reported_customers
FROM outage_events e
JOIN meters m ON m.meter_id = e.meter_id
"""


def _event_from_row(row: sqlite3.Row) -> OutageEvent:
    return OutageEvent(
        event_id=row["event_id"], meter_id=row["meter_id"], feeder_id=row["feeder_id"],
        region=row["region"], started_at=row["started_at"], restored_at=row["restored_at"],
        cause=row["cause"], reported_customers=row["reported_customers"],
    )


def list_events(conn: sqlite3.Connection) -> list[OutageEvent]:
    """Return all events ordered by start time and event id."""
    rows = conn.execute(EVENT_SELECT + " ORDER BY e.started_at, e.event_id").fetchall()
    return [_event_from_row(row) for row in rows]


def feeder_summary(conn: sqlite3.Connection) -> list[dict[str, Any]]:
    """Return per-feeder event, customer, duration, and active-event totals.

    TODO(candidate): use a JOIN, GROUP BY, deterministic ordering, and duration
    calculation. Expected keys: feeder_id, region, event_count,
    affected_customers, closed_minutes, active_events.
    """
    raise NotImplementedError("TODO: implement feeder summary SQL")


def latest_event_by_meter(conn: sqlite3.Connection) -> list[OutageEvent]:
    """Return the latest event for every meter using a window function.

    TODO(candidate): ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...).
    """
    raise NotImplementedError("TODO: implement latest-event window query")


def recurring_outage_meters(conn: sqlite3.Connection, min_events: int = 2) -> list[dict[str, Any]]:
    """Return meters with at least min_events outages, using a CTE.

    TODO(candidate): expected keys: meter_id, feeder_id, outage_count,
    last_started_at; order by outage_count DESC, meter_id ASC.
    """
    raise NotImplementedError("TODO: implement recurring-meter CTE")


def explain_latest_event_query(conn: sqlite3.Connection) -> list[str]:
    """Return EXPLAIN QUERY PLAN detail lines for a meter/time lookup."""
    query = """
    EXPLAIN QUERY PLAN
    SELECT event_id, meter_id, started_at
    FROM outage_events
    WHERE meter_id = ? AND started_at >= ?
    ORDER BY started_at
    """
    rows = conn.execute(query, ("M1001", "2026-09-01 00:00")).fetchall()
    return [row["detail"] for row in rows]
