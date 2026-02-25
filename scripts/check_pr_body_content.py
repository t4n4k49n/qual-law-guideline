from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

from pr_body_guard_lib import find_marker_path, validate_text_content


TARGET_SUFFIXES = {".md"}


def _is_candidate(path: Path) -> bool:
    posix = path.as_posix()
    if path.name == "PR.md":
        return True
    if posix.startswith("out/pr") and path.suffix.lower() == ".md":
        return True
    return False


def _iter_tracked_files() -> Iterable[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    for chunk in proc.stdout.split(b"\x00"):
        if not chunk:
            continue
        p = Path(chunk.decode("utf-8", errors="replace"))
        if p.suffix.lower() not in TARGET_SUFFIXES:
            continue
        if _is_candidate(p):
            yield p


def _iter_files_from_args(args: Sequence[str]) -> Iterable[Path]:
    for raw in args:
        p = Path(raw)
        if p.suffix.lower() not in TARGET_SUFFIXES:
            continue
        if not p.exists() or not p.is_file():
            continue
        if _is_candidate(p):
            yield p


def _scan(path: Path) -> int:
    total = 0
    text = path.read_text(encoding="utf-8")
    issues = validate_text_content(text)
    marker = find_marker_path(text)
    if marker is None:
        issues.append("missing PR body marker: <!-- PR_BODY_FILE: <path> -->")

    for issue in issues:
        print(f"{path}: {issue}")
        total += 1
    return total


def main() -> int:
    targets = list(_iter_files_from_args(sys.argv[1:]))
    if not targets:
        targets = list(_iter_tracked_files())

    total = 0
    for path in targets:
        total += _scan(path)

    if total:
        print("Detected PR body content policy violations.", file=sys.stderr)
        return 1
    print("No PR body content policy violations found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

