#!/usr/bin/env python
from __future__ import annotations

import os
import shutil
import sqlite3
import subprocess
import sys
from pathlib import Path


def normalize_path(value: str | os.PathLike[str]) -> Path:
    text = os.fspath(value)
    if os.name == "nt" and len(text) >= 3 and text[0] == "/" and text[2] == "/" and text[1].isalpha():
        text = f"{text[1].upper()}:/{text[3:]}"
    return Path(text)


def check(name: str, ok: bool, detail: str, required: bool = True) -> bool:
    status = "OK" if ok else ("FAIL" if required else "WARN")
    print(f"[{status}] {name}: {detail}")
    return ok or not required


def command_version(command: list[str]) -> str:
    try:
        result = subprocess.run(command, text=True, capture_output=True, timeout=10, check=False)
        return (result.stdout or result.stderr).splitlines()[0].strip()
    except Exception as exc:  # deliberately broad: this is a diagnostic script
        return str(exc)


def main() -> int:
    root = normalize_path(Path(__file__).resolve().parent)
    os.chdir(root)
    print(f"GridPulse environment check — {root}")
    ok = True
    ok &= check("Python", sys.version_info >= (3, 12), sys.version.split()[0])
    ok &= check("SQLite", sqlite3.sqlite_version_info >= (3, 35), sqlite3.sqlite_version)
    git = shutil.which("git")
    ok &= check("Git", git is not None, command_version(["git", "--version"]) if git else "not found")
    tar = shutil.which("tar")
    ok &= check("tar/bsdtar", tar is not None, command_version(["tar", "--version"]) if tar else "not found")
    vendor = root / "vendor"
    wheels = list(vendor.glob("*.whl")) if vendor.exists() else []
    ok &= check("Vendored pytest wheels", len(wheels) >= 3, f"{len(wheels)} wheel(s) found")
    docker = shutil.which("docker")
    check("Docker (optional)", docker is not None, command_version(["docker", "--version"]) if docker else "not found; use static review path", required=False)
    if os.name == "nt":
        print("[INFO] Windows note: chmod executable bits are a filesystem no-op; run scripts with bash script-name.sh.")
    print("Environment check " + ("passed" if ok else "failed"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
