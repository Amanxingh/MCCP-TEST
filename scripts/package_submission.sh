#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"
mkdir -p submission

# TODO(candidate): create submission/gridpulse-submission.tar.gz with tar.
# Exclude .git, .venv, caches, data/*.db, artifacts, submission, and old archives.
echo "TODO(candidate): implement package_submission.sh" >&2
exit 1
