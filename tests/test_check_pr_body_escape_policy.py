from __future__ import annotations

import subprocess
import sys
from pathlib import Path


SCRIPT = Path("scripts/check_pr_body_escape_policy.py")


def _run_check(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(target)],
        text=True,
        capture_output=True,
        check=False,
    )


def test_detects_gh_pr_body_usage(tmp_path: Path) -> None:
    f = tmp_path / "sample.md"
    f.write_text('gh pr create --body "bad"\n', encoding="utf-8", newline="\n")
    proc = _run_check(f)
    assert proc.returncode == 1
    assert "forbidden `gh pr ... --body` usage" in proc.stdout


def test_allows_gh_pr_body_file_usage(tmp_path: Path) -> None:
    f = tmp_path / "sample.md"
    f.write_text("gh pr create --body-file body.md\n", encoding="utf-8", newline="\n")
    proc = _run_check(f)
    assert proc.returncode == 0
    assert "No forbidden PR body / PowerShell escaping patterns found." in proc.stdout


def test_detects_powershell_double_quote_herestring(tmp_path: Path) -> None:
    f = tmp_path / "sample.ps1"
    f.write_text('@\"\nhello\n\"@\n', encoding="utf-8", newline="\n")
    proc = _run_check(f)
    assert proc.returncode == 1
    assert "forbidden PowerShell @\" here-string" in proc.stdout
