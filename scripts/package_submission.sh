
#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHIVE_NAME="gridpulse-submission.tar.gz"
ARCHIVE_PATH="$PROJECT_ROOT/$ARCHIVE_NAME"

cd "$PROJECT_ROOT"

# Exclude Git metadata, virtual environments, caches, and previous archives.
tar -czf "$ARCHIVE_PATH" \
    --exclude=".git" \
    --exclude=".venv" \
    --exclude="venv" \
    --exclude="__pycache__" \
    --exclude=".pytest_cache" \
    --exclude=".mypy_cache" \
    --exclude=".ruff_cache" \
    --exclude="$ARCHIVE_NAME" \
    .

echo "Submission archive created:"
echo "$ARCHIVE_PATH"
echo "Archive size:"
du -h "$ARCHIVE_PATH"
