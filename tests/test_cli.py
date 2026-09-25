from __future__ import annotations

from gridpulse.cli import main


def test_init_and_report_cli(db_path, capsys):
    assert main(["--db", str(db_path), "init-db"]) == 0
    assert db_path.exists()
    assert main(["--db", str(db_path), "report"]) == 0
    out = capsys.readouterr().out
    assert "GridPulse Feeder Outage Report" in out
    assert "F-South | South | events=2" in out


def test_cli_uses_environment_database(monkeypatch, db_path):
    monkeypatch.setenv("GRIDPULSE_DB", str(db_path))
    assert main(["init-db"]) == 0
    assert db_path.exists()


def test_cli_rejects_bad_database_path(tmp_path, capsys):
    blocked = tmp_path / "not-a-directory"
    blocked.write_text("occupied", encoding="utf-8")
    assert main(["--db", str(blocked / "gridpulse.db"), "init-db"]) == 2
    assert "error" in capsys.readouterr().err.lower()
