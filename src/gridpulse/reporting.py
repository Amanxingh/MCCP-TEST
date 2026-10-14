
from __future__ import annotations

from typing import Any

from .models import OutageEvent


def render_feeder_report(summary: list[dict[str, Any]], latest: list[OutageEvent]) -> str:
    """Render the deterministic text report consumed by the CLI.

    TODO(candidate): include a header, one sorted line per feeder, and a latest
    event section. Match tests/test_reporting.py exactly.
    """
    lines = ["GRIDPULSE OUTAGE REPORT", ""]

    lines.append("FEEDER SUMMARY")
    for feeder in sorted(summary, key=lambda item: item["feeder_id"]):
        lines.append(
            f"Feeder {feeder['feeder_id']} ({feeder['region']}): "
            f"{feeder['event_count']} events, "
            f"{feeder['affected_customers']} affected customers, "
            f"{feeder['closed_minutes']} closed minutes, "
            f"{feeder['active_events']} active events"
        )

    lines.extend(["", "LATEST EVENTS"])
    for event in sorted(latest, key=lambda item: (item.started_at, item.event_id), reverse=True):
        status = "active" if event.restored_at is None else "restored"
        lines.append(
            f"Event {event.event_id}: meter={event.meter_id}, "
            f"feeder={event.feeder_id}, region={event.region}, "
            f"cause={event.cause}, status={status}"
        )

    return "\n".join(lines)