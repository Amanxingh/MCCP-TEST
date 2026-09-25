from __future__ import annotations

from typing import Any

from .models import OutageEvent


def render_feeder_report(summary: list[dict[str, Any]], latest: list[OutageEvent]) -> str:
    """Render the deterministic text report consumed by the CLI.

    TODO(candidate): include a header, one sorted line per feeder, and a latest
    event section. Match tests/test_reporting.py exactly.
    """
    raise NotImplementedError("TODO: render feeder report")
