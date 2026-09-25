from __future__ import annotations

import logging

import pytest

from gridpulse.models import OutageEvent
from gridpulse.service import OutageAnalyzer, OutageDataError, log_call, parse_feeder_code, summarize_regions


def make_event(event_id, cause="storm", started="2026-09-01 08:00", restored="2026-09-01 10:30", customers=12, region="North"):
    return OutageEvent(event_id, "M1001", "F-North", region, started, restored, cause, customers)


def test_priority_scores_are_deterministic():
    analyzer = OutageAnalyzer()
    assert analyzer.priority_score(make_event(1)) == 2700.0
    active = OutageEvent(4, "M2002", "F-South", "South", "2026-09-03 06:30", None, "equipment", 35)
    assert analyzer.priority_score(active, "2026-09-03 12:00") == 13860.0


def test_unknown_cause_raises_domain_error():
    with pytest.raises(OutageDataError, match="unknown cause"):
        OutageAnalyzer().priority_score(make_event(9, cause="cyber"))


def test_classification_boundaries():
    analyzer = OutageAnalyzer()
    assert analyzer.classify_event(make_event(1, restored="2026-09-01 08:29")) == "brief"
    assert analyzer.classify_event(make_event(2, restored="2026-09-01 09:30")) == "standard"
    assert analyzer.classify_event(make_event(3)) == "extended"
    assert analyzer.classify_event(make_event(4, restored=None), "2026-09-01 09:00") == "active"


def test_high_priority_generator_orders_by_score():
    events = [
        make_event(5, cause="vegetation", started="2026-09-03 07:00", restored="2026-09-03 09:00", customers=9, region="East"),
        make_event(1),
        OutageEvent(4, "M2002", "F-South", "South", "2026-09-03 06:30", None, "equipment", 35),
    ]
    result = list(OutageAnalyzer().high_priority_events(events, 1000, "2026-09-03 12:00"))
    assert [event.event_id for event in result] == [4, 1, 5]


def test_parse_feeder_code_with_regex():
    assert parse_feeder_code(" F-North ") == "F-North"
    with pytest.raises(OutageDataError):
        parse_feeder_code("North-1")


def test_summarize_regions_functionally():
    events = [make_event(1), make_event(2, customers=4), make_event(3, customers=9, region="East")]
    assert summarize_regions(iter(events)) == {"North": 16, "East": 9}


def test_log_call_decorator_preserves_metadata_and_logs(caplog):
    logger = logging.getLogger("gridpulse.test")
    @log_call(logger)
    def add(a: int, b: int) -> int:
        """Add two values."""
        return a + b
    with caplog.at_level(logging.INFO, logger="gridpulse.test"):
        assert add(2, 3) == 5
    assert add.__name__ == "add"
    assert "add" in caplog.text
