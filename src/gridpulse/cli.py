
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .config import get_database_path
from .db import connect, initialize_database, seed_database
from .logging_utils import configure_logging
from .reporting import render_feeder_report
from .repository import feeder_summary, latest_event_by_meter


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gridpulse", description="Energy meter outage analytics")
    parser.add_argument("--db", default=None, help="SQLite database path; defaults to GRIDPULSE_DB or data/gridpulse.db")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init-db", help="Create and seed the database")
    report = sub.add_parser("report", help="Print the feeder outage report")
    report.add_argument("--as-of", default="2026-09-03 12:00", help="Timestamp for active-event calculations")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI.

    TODO(candidate): wire init-db/report commands, logging, errors, and exit codes.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        logger = configure_logging(args.log_level)
        db_path = args.db if args.db is not None else get_database_path()
        db_path = Path(db_path)

        logger.info("Starting GridPulse command: %s", args.command)

        if args.command == "init-db":
            with connect(db_path) as conn:
                initialize_database(conn)
                seed_database(conn)
            logger.info("Database initialized and seeded: %s", db_path)
            return 0

        if args.command == "report":
            with connect(db_path) as conn:
                summary = feeder_summary(conn)
                latest = latest_event_by_meter(conn)

            report_text = render_feeder_report(summary, latest)
            print(report_text)
            logger.info("Report generated successfully")
            return 0

        parser.error(f"Unsupported command: {args.command}")

    except (OSError, ValueError, RuntimeError) as exc:
        logging.getLogger("gridpulse").error("Command failed: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        logging.getLogger("gridpulse").exception("Unexpected CLI failure")
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
