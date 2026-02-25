from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

try:
    from pr_body_guard_lib import (
        find_marker_path,
        is_safe_relative_path,
        normalize_text,
        validate_text_content,
    )
except ModuleNotFoundError:
    from scripts.pr_body_guard_lib import (
        find_marker_path,
        is_safe_relative_path,
        normalize_text,
        validate_text_content,
    )


def _run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def _load_current_pr() -> dict | None:
    proc = _run_gh(["pr", "view", "--json", "number,body,headRefName,baseRefName"])
    if proc.returncode != 0:
        stderr = (proc.stderr or "").strip().lower()
        if "no pull requests found" in stderr or "could not find pull request" in stderr:
            return None
        print("pre-push PR body guard: failed to query current PR via gh", file=sys.stderr)
        print((proc.stderr or proc.stdout or "").strip(), file=sys.stderr)
        return {"_error": True}

    raw = proc.stdout or ""
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print("pre-push PR body guard: invalid JSON from gh pr view", file=sys.stderr)
        return {"_error": True}


def main() -> int:
    pr = _load_current_pr()
    if pr is None:
        return 0
    if pr.get("_error"):
        return 1

    body = pr.get("body") or ""
    issues = validate_text_content(body)
    for issue in issues:
        print(f"PR body violation: {issue}", file=sys.stderr)

    marker_path = find_marker_path(body)
    if not marker_path:
        print("PR body violation: missing marker <!-- PR_BODY_FILE: <path> -->", file=sys.stderr)
        return 1
    if not is_safe_relative_path(marker_path):
        print(f"PR body violation: unsafe marker path: {marker_path}", file=sys.stderr)
        return 1

    marker_file = Path(marker_path)
    if not marker_file.exists() or not marker_file.is_file():
        print(f"PR body violation: marker file not found in repo: {marker_path}", file=sys.stderr)
        return 1

    file_text = marker_file.read_text(encoding="utf-8")
    file_issues = validate_text_content(file_text)
    for issue in file_issues:
        print(f"PR body file violation ({marker_path}): {issue}", file=sys.stderr)

    if normalize_text(body).rstrip("\n") != normalize_text(file_text).rstrip("\n"):
        print("PR body violation: body content does not match marker file content", file=sys.stderr)
        return 1

    if issues or file_issues:
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
