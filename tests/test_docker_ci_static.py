from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    return (ROOT / rel).read_text(encoding="utf-8")


def test_dockerfile_uses_reproducible_offline_test_install():
    text = read("docker/Dockerfile")
    for token in ["FROM python:3.12-slim", "WORKDIR /app", "COPY requirements-dev.txt", "COPY vendor/", "--no-index", "--find-links=vendor", "COPY src/", "COPY tests/", "CMD"]:
        assert token in text
    assert "TODO(candidate)" not in text


def test_compose_declares_volume_network_and_environment():
    text = read("docker/docker-compose.yml")
    for token in ["services:", "build:", "volumes:", "networks:", "GRIDPULSE_DB", "gridpulse-data"]:
        assert token in text
    assert "TODO(candidate)" not in text


def test_ci_has_test_gate_promotion_and_safe_secrets():
    text = read(".github/workflows/ci.yml")
    for token in ["pull_request", "windows-latest", "--no-index --find-links=vendor", "python -m pytest", "workflow_dispatch", "environment: staging", "environment: production", "secrets.GRIDPULSE_DEPLOY_HOST"]:
        assert token in text
    assert "TODO(candidate)" not in text
    forbidden = ["password:", "BEGIN PRIVATE KEY", "AKIA"]
    assert not any(token in text for token in forbidden)
