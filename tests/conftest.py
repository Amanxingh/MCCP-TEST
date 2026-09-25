from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from gridpulse.db import connect, initialize_database, seed_database


@pytest.fixture()
def db_path(tmp_path):
    return tmp_path / "gridpulse-test.db"


@pytest.fixture()
def seeded_conn(db_path):
    conn = connect(db_path)
    initialize_database(conn)
    seed_database(conn)
    yield conn
    conn.close()
