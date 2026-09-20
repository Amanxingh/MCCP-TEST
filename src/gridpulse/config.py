from __future__ import annotations

import os
from pathlib import Path

APP_NAME = "gridpulse"
DEFAULT_DB_PATH = Path("data/gridpulse.db")


def normalize_path(value: str | os.PathLike[str]) -> Path:
    """Return a Path, converting Git Bash /c/... paths on Windows."""
    text = os.fspath(value)
    if os.name == "nt" and len(text) >= 3 and text[0] == "/" and text[2] == "/" and text[1].isalpha():
        text = f"{text[1].upper()}:/{text[3:]}"
    return Path(text)


def get_database_path() -> Path:
    """Resolve the database path from GRIDPULSE_DB or the project default."""
    return normalize_path(os.environ.get("GRIDPULSE_DB", DEFAULT_DB_PATH))
