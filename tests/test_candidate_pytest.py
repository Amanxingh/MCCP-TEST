
from __future__ import annotations

import pytest

from gridpulse.cli import build_parser
from gridpulse.models import OutageEvent
from gridpulse.service import OutageAnalyzer, OutageDataError


def test_priority_score_uses_duration_customers_and_cause_multiplier() -> None:
    event = OutageEvent(
        event_id=1,
        meter_id="M1001",
        feeder_id="F-North",
        region="North",
        started_at="2026-09-01 08:00",
        restored_at="2026-09-01 09:00",
        cause="storm",
        reported_customers=12,
    )

    analyzer = OutageAnalyzer()

    assert analyzer.priority_score(event) == 60 * 12 * 1.5


def test_cli_rejects_invalid_log_level() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--log-level", "INVALID", "report"])

    assert exc_info.value.code == 2
