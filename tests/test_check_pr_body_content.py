from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/check_pr_body_content.py")


def _run_check(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(target)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_candidate_requires_marker(tmp_path: Path) -> None:
    f = tmp_path / "PR.md"
    f.write_text("## title\n", encoding="utf-8", newline="\n")
    proc = _run_check(f)
    assert proc.returncode == 1
    assert "missing PR body marker" in proc.stdout


def test_candidate_passes_with_marker_and_clean_content(tmp_path: Path) -> None:
    f = tmp_path / "PR.md"
    f.write_text(
        "## title\n\n<!-- PR_BODY_FILE: runs/20260101-000000000_x/PR.md -->\n",
        encoding="utf-8",
        newline="\n",
    )
    proc = _run_check(f)
    assert proc.returncode == 0


def test_candidate_detects_replacement_character(tmp_path: Path) -> None:
    f = tmp_path / "PR.md"
    f.write_text(
        "bad � text\n<!-- PR_BODY_FILE: runs/20260101-000000000_x/PR.md -->\n",
        encoding="utf-8",
        newline="\n",
    )
    proc = _run_check(f)
    assert proc.returncode == 1
    assert "replacement character" in proc.stdout


def test_non_candidate_arg_does_not_fallback_to_repo_scan(tmp_path: Path) -> None:
    f = tmp_path / "README.md"
    f.write_text("hello\n", encoding="utf-8", newline="\n")
    proc = _run_check(f)
    assert proc.returncode == 0
    assert "No PR body content policy violations found." in proc.stdout
