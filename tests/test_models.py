from __future__ import annotations

import pytest

from gridpulse.models import OutageEvent


def event(**overrides):
    values = dict(event_id=1, meter_id="M1001", feeder_id="F-North", region="North", started_at="2026-09-01 08:00", restored_at="2026-09-01 10:30", cause="storm", reported_customers=12)
    values.update(overrides)
    return OutageEvent(**values)


def test_closed_event_duration():
    assert event().duration_minutes() == 150


def test_active_event_uses_as_of():
    active = event(event_id=4, meter_id="M2002", feeder_id="F-South", region="South", started_at="2026-09-03 06:30", restored_at=None, cause="equipment", reported_customers=35)
    assert active.duration_minutes("2026-09-03 12:00") == 330


def test_impossible_restore_time_is_rejected():
    with pytest.raises(ValueError, match="before"):
        event(restored_at="2026-09-01 07:00").duration_minutes()


def test_events_sort_by_timestamp_then_id():
    assert sorted([event(event_id=2, started_at="2026-09-01 08:00"), event(event_id=1, started_at="2026-09-01 08:00")])[0].event_id == 1
