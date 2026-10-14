
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
    query = """
    SELECT
        m.feeder_id,
        m.region,
        COUNT(e.event_id) AS event_count,
        COALESCE(SUM(e.reported_customers), 0) AS affected_customers,
        COALESCE(
            SUM(
                CASE
                    WHEN e.restored_at IS NOT NULL THEN
                        MAX(
                            0,
                            (julianday(e.restored_at)
                             - julianday(e.started_at)) * 1440
                        )
                    ELSE 0
                END
            ),
            0
        ) AS closed_minutes,
        COALESCE(
            SUM(
                CASE
                    WHEN e.restored_at IS NULL THEN 1
                    ELSE 0
                END
            ),
            0
        ) AS active_events
    FROM meters AS m
    LEFT JOIN outage_events AS e ON e.meter_id = m.meter_id
    GROUP BY m.feeder_id, m.region
    ORDER BY m.feeder_id ASC
    """
    rows = conn.execute(query).fetchall()
    return [dict(row) for row in rows]


def latest_event_by_meter(conn: sqlite3.Connection) -> list[OutageEvent]:
    """Return the latest event for every meter using a window function.

    TODO(candidate): ROW_NUMBER() OVER (PARTITION BY ... ORDER BY ...).
    """
    query = """
    WITH ranked_events AS (
        SELECT
            e.event_id,
            e.meter_id,
            m.feeder_id,
            m.region,
            e.started_at,
            e.restored_at,
            e.cause,
            e.reported_customers,
            ROW_NUMBER() OVER (
                PARTITION BY e.meter_id
                ORDER BY e.started_at DESC, e.event_id DESC
            ) AS row_num
        FROM outage_events AS e
        JOIN meters AS m ON m.meter_id = e.meter_id
    )
    SELECT
        event_id,
        meter_id,
        feeder_id,
        region,
        started_at,
        restored_at,
        cause,
        reported_customers
    FROM ranked_events
    WHERE row_num = 1
    ORDER BY meter_id ASC
    """
    rows = conn.execute(query).fetchall()
    return [_event_from_row(row) for row in rows]


def recurring_outage_meters(
    conn: sqlite3.Connection, min_events: int = 2
) -> list[dict[str, Any]]:
    """Return meters with at least min_events outages, using a CTE.

    TODO(candidate): expected keys: meter_id, feeder_id, outage_count,
    last_started_at; order by outage_count DESC, meter_id ASC.
    """
    if min_events < 1:
        raise ValueError("min_events must be at least 1")

    query = """
    WITH meter_outages AS (
        SELECT
            meter_id,
            COUNT(*) AS outage_count,
            MAX(started_at) AS last_started_at
        FROM outage_events
        GROUP BY meter_id
        HAVING COUNT(*) >= ?
    )
    SELECT
        mo.meter_id,
        m.feeder_id,
        mo.outage_count,
        mo.last_started_at
    FROM meter_outages AS mo
    JOIN meters AS m ON m.meter_id = mo.meter_id
    ORDER BY mo.outage_count DESC, mo.meter_id ASC
    """
    rows = conn.execute(query, (min_events,)).fetchall()
    return [dict(row) for row in rows]


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
