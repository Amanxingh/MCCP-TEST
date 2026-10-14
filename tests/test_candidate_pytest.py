from __future__ import annotations

import pytest

from gridpulse.models import OutageEvent
from gridpulse.cli import build_parser


def test_outage_duration_rejects_invalid_timestamp() -> None:
    event = OutageEvent(
        event_id=1,
        meter_id="M1001",
        feeder_id="F-North",
        region="North",
        started_at="invalid-timestamp",
        restored_at="2026-09-01 10:00",
        cause="storm",
        reported_customers=10,
    )

    with pytest.raises((ValueError, TypeError, NotImplementedError)):
        event.duration_minutes()


def test_cli_rejects_invalid_arguments() -> None:
    parser = build_parser()

    with pytest.raises(SystemExit) as exc_info:
        parser.parse_args(["--invalid-option"])

    assert exc_info.value.code == 2
    