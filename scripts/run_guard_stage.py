from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], *, env: dict[str, str] | None = None, stdin_text: str | None = None) -> int:
    proc = subprocess.run(cmd, env=env, input=stdin_text, text=True)
    return proc.returncode


def _staged_files() -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB", "-z"],
        check=True,
        capture_output=True,
    )
    files: list[str] = []
    for chunk in proc.stdout.split(b"\x00"):
        if chunk:
            files.append(chunk.decode("utf-8", errors="replace"))
    return files


def _python_exe() -> str:
    candidates = [
        Path(".venv/Scripts/python.exe"),
        Path(".venv/bin/python"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return sys.executable


def run_pre_commit(py: str) -> int:
    files = _staged_files()

    checks: list[list[str]] = [
        [py, "scripts/check_venv_runtime.py"],
        [py, "scripts/check_user_dir_leak.py"],
        [py, "scripts/check_venv_command_policy.py"],
        [py, "scripts/check_parent_root_notes_absent.py"],
    ]

    if files:
        checks.extend(
            [
                [py, "scripts/check_parent_local_notes_boundary.py", *files],
                [py, "scripts/check_bidi_controls.py", *files],
                [py, "scripts/check_pr_body_escape_policy.py", *files],
                [py, "scripts/check_pr_body_content.py", *files],
            ]
        )

    for cmd in checks:
        rc = _run(cmd)
        if rc != 0:
            return rc
    return 0


def run_pre_push(py: str, stdin_text: str) -> int:
    rc = _run([py, "scripts/check_parent_root_notes_absent.py"])
    if rc != 0:
        return rc

    env = os.environ.copy()
    env["PRE_COMMIT_STAGE"] = "pre-push"
    rc = _run(
        [py, "scripts/check_parent_local_notes_boundary.py"],
        env=env,
        stdin_text=stdin_text,
    )
    if rc != 0:
        return rc

    rc = _run([py, "scripts/check_pr_body_live_local.py"])
    if rc != 0:
        return rc
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True, choices=["pre-commit", "pre-push"])
    args = parser.parse_args()

    py = _python_exe()
    if args.stage == "pre-commit":
        return run_pre_commit(py)

    stdin_text = sys.stdin.read()
    return run_pre_push(py, stdin_text)


if __name__ == "__main__":
    raise SystemExit(main())
