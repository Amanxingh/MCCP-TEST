from __future__ import annotations

from gridpulse.reporting import render_feeder_report
from gridpulse.repository import feeder_summary, latest_event_by_meter


EXPECTED = """GridPulse Feeder Outage Report
================================
F-East | East | events=1 | customers=9 | closed_minutes=120 | active=0
F-North | North | events=3 | customers=28 | closed_minutes=320 | active=0
F-South | South | events=2 | customers=57 | closed_minutes=60 | active=1

Latest event by meter
M1001: event 6 started 2026-09-04 08:30 (restored)
M1002: event 2 started 2026-09-01 09:15 (restored)
M2001: event 3 started 2026-09-02 14:00 (restored)
M2002: event 4 started 2026-09-03 06:30 (ACTIVE)
M3001: event 5 started 2026-09-03 07:00 (restored)"""


def test_render_feeder_report_exact_text(seeded_conn):
    assert render_feeder_report(feeder_summary(seeded_conn), latest_event_by_meter(seeded_conn)) == EXPECTED
