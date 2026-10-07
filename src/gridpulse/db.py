from __future__ import annotations

import sqlite3
from pathlib import Path

from .config import normalize_path

SCHEMA_SQL = """
-- TODO(candidate): create meters, outage_events, and a useful composite index.
-- Required columns are described by the seed rows below and by tests/test_db.py.
"""

METER_ROWS = [
    ("M1001", "F-North", "North", 12, "active"),
    ("M1002", "F-North", "North", 4, "active"),
    ("M2001", "F-South", "South", 22, "maintenance"),
    ("M2002", "F-South", "South", 35, "active"),
    ("M3001", "F-East", "East", 9, "active"),
]

EVENT_ROWS = [
    (1, "M1001", "2026-09-01 08:00", "2026-09-01 10:30", "storm", 12),
    (2, "M1002", "2026-09-01 09:15", "2026-09-01 11:45", "storm", 4),
    (3, "M2001", "2026-09-02 14:00", "2026-09-02 15:00", "equipment", 22),
    (4, "M2002", "2026-09-03 06:30", None, "equipment", 35),
    (5, "M3001", "2026-09-03 07:00", "2026-09-03 09:00", "vegetation", 9),
    (6, "M1001", "2026-09-04 08:30", "2026-09-04 08:50", "vegetation", 12),
]


def connect(path: str | Path) -> sqlite3.Connection:
    db_path = normalize_path(path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database(conn: sqlite3.Connection) -> None:
    """Create the schema and indexes.

    TODO(candidate): execute SCHEMA_SQL as a transaction.
    """
    raise NotImplementedError("TODO: create the GridPulse schema")


def seed_database(conn: sqlite3.Connection) -> None:
    """Load deterministic seed data. Re-running must not duplicate rows.

    TODO(candidate): use idempotent upsert statements and commit.
    """
    raise NotImplementedError("TODO: seed the GridPulse database")
