from __future__ import annotations

import sqlite3

import pytest

from gridpulse.db import connect, initialize_database, seed_database


def table_names(conn):
    return {row["name"] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}


def test_schema_and_deterministic_seed(seeded_conn):
    assert {"meters", "outage_events"}.issubset(table_names(seeded_conn))
    assert seeded_conn.execute("SELECT COUNT(*) FROM meters").fetchone()[0] == 5
    assert seeded_conn.execute("SELECT COUNT(*) FROM outage_events").fetchone()[0] == 6
    seed_database(seeded_conn)
    assert seeded_conn.execute("SELECT COUNT(*) FROM outage_events").fetchone()[0] == 6


def test_relational_constraints(seeded_conn):
    with pytest.raises(sqlite3.IntegrityError):
        seeded_conn.execute(
            "INSERT INTO outage_events(event_id, meter_id, started_at, cause, reported_customers) VALUES (?, ?, ?, ?, ?)",
            (99, "MISSING", "2026-09-05 00:00", "storm", 1),
        )
    with pytest.raises(sqlite3.IntegrityError):
        seeded_conn.execute(
            "INSERT INTO outage_events(event_id, meter_id, started_at, cause, reported_customers) VALUES (?, ?, ?, ?, ?)",
            (100, "M1001", "2026-09-05 00:00", "storm", -1),
        )


def test_composite_index_exists(seeded_conn):
    rows = seeded_conn.execute("SELECT name FROM sqlite_master WHERE type='index'").fetchall()
    assert "idx_outage_events_meter_started" in {row[0] for row in rows}
