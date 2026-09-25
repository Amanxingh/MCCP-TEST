from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_run_checks_auto_detects_interpreter_and_writes_summary():
    text = read("scripts/run_checks.sh")
    assert "command -v python3" in text
    assert "command -v python" in text
    assert "command -v py" in text
    assert "TODO(candidate)" not in text
    assert "verify_env.py" in text
    assert "pytest" in text
    assert "grep" in text
    assert "artifacts/test-summary.txt" in text


def test_package_script_uses_tar_and_excludes_generated_files():
    text = read("scripts/package_submission.sh")
    assert "tar" in text
    assert "--exclude=.git" in text or "--exclude='.git'" in text or '--exclude=".git"' in text
    assert "--exclude=.venv" in text or "--exclude='.venv'" in text or '--exclude=".venv"' in text
    assert "submission" in text
    assert "TODO(candidate)" not in text


def test_remote_deploy_validates_environment_and_does_not_connect():
    text = read("scripts/remote_deploy.sh")
    for name in ["GRIDPULSE_REMOTE_HOST", "GRIDPULSE_REMOTE_USER", "GRIDPULSE_SSH_KEY"]:
        assert name in text
    assert "ssh" in text
    assert "DRY_RUN" in text
    assert "TODO(candidate)" not in text
