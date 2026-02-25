from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pr_body_guard_lib import (
    find_marker_path,
    is_safe_relative_path,
    normalize_text,
    validate_text_content,
)


def _extract_body_file(args: list[str]) -> str | None:
    body_file: str | None = None
    idx = 0
    while idx < len(args):
        token = args[idx]
        if token == "--body":
            raise ValueError("forbidden --body option; use --body-file <repo-relative-path>")
        if token.startswith("--body="):
            raise ValueError("forbidden --body option; use --body-file <repo-relative-path>")
        if token == "--body-file":
            if idx + 1 >= len(args):
                raise ValueError("--body-file requires a path")
            body_file = args[idx + 1]
            idx += 2
            continue
        if token.startswith("--body-file="):
            body_file = token.split("=", 1)[1]
        idx += 1
    return body_file


def _validate_body_file(path_str: str) -> None:
    if not is_safe_relative_path(path_str):
        raise ValueError(f"body-file must be a safe repo-relative path: {path_str}")

    path = Path(path_str)
    if not path.exists() or not path.is_file():
        raise ValueError(f"body-file not found: {path_str}")

    text = path.read_text(encoding="utf-8")
    issues = validate_text_content(text)
    if issues:
        joined = "; ".join(issues)
        raise ValueError(f"body-file content violation: {joined}")

    marker = find_marker_path(text)
    if not marker:
        raise ValueError("body-file missing marker <!-- PR_BODY_FILE: <path> -->")
    if marker != path_str:
        raise ValueError(f"marker path mismatch: marker='{marker}' expected='{path_str}'")


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] not in {"create", "edit"}:
        print("usage: python scripts/gh_pr_guard.py <create|edit> ... --body-file <repo-relative-path>")
        return 2

    sub = args[0]
    rest = args[1:]
    try:
        body_file = _extract_body_file(rest)
        if not body_file:
            raise ValueError("--body-file is required")
        _validate_body_file(body_file)
    except ValueError as exc:
        print(f"PR command blocked: {exc}", file=sys.stderr)
        return 1

    proc = subprocess.run(["gh", "pr", sub, *rest], check=False)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
