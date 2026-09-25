from __future__ import annotations

from gridpulse.repository import explain_latest_event_query, feeder_summary, latest_event_by_meter, list_events, recurring_outage_meters


def test_list_events_joins_meter_dimension(seeded_conn):
    events = list_events(seeded_conn)
    assert len(events) == 6
    assert events[0].feeder_id == "F-North"
    assert events[-1].event_id == 6


def test_feeder_summary_has_baked_in_values(seeded_conn):
    assert feeder_summary(seeded_conn) == [
        {"feeder_id": "F-East", "region": "East", "event_count": 1, "affected_customers": 9, "closed_minutes": 120, "active_events": 0},
        {"feeder_id": "F-North", "region": "North", "event_count": 3, "affected_customers": 28, "closed_minutes": 320, "active_events": 0},
        {"feeder_id": "F-South", "region": "South", "event_count": 2, "affected_customers": 57, "closed_minutes": 60, "active_events": 1},
    ]


def test_latest_event_by_meter_uses_window_logic(seeded_conn):
    latest = latest_event_by_meter(seeded_conn)
    assert [(event.meter_id, event.event_id) for event in latest] == [
        ("M1001", 6), ("M1002", 2), ("M2001", 3), ("M2002", 4), ("M3001", 5)
    ]


def test_recurring_meters_uses_cte_and_having(seeded_conn):
    assert recurring_outage_meters(seeded_conn, min_events=2) == [
        {"meter_id": "M1001", "feeder_id": "F-North", "outage_count": 2, "last_started_at": "2026-09-04 08:30"}
    ]


def test_explain_plan_uses_composite_index(seeded_conn):
    details = explain_latest_event_query(seeded_conn)
    assert any("idx_outage_events_meter_started" in line for line in details)
