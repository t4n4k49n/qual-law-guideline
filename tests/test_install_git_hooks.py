from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/install_git_hooks.py")


def test_install_sets_core_hooks_path(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)

    scripts = repo / "scripts"
    hooks = repo / ".githooks"
    scripts.mkdir()
    hooks.mkdir()

    (scripts / "install_git_hooks.py").write_text(
        SCRIPT.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (hooks / "pre-commit").write_text("#!/bin/sh\n", encoding="utf-8")
    (hooks / "pre-push").write_text("#!/bin/sh\n", encoding="utf-8")

    subprocess.run([sys.executable, "scripts/install_git_hooks.py"], cwd=repo, check=True)

    proc = subprocess.run(
        ["git", "config", "--get", "core.hooksPath"],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    assert proc.stdout.strip() == ".githooks"
