#!/usr/bin/env python3
"""Block parent-repo commits/pushes that include local-notes artifacts."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

FORBIDDEN_EXACT = {"TODO.md", "KNOWLEDGE.md"}
FORBIDDEN_PREFIXES = ("local_notes/",)


def _normalize(path: str) -> str:
    return path.replace("\\", "/").strip()


def _from_git_diff_cached() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _from_git_push_ref() -> list[str]:
    lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]
    if not lines:
        return []

    changed: set[str] = set()
    for line in lines:
        parts = line.split()
        if len(parts) < 4:
            continue
        local_sha, remote_sha = parts[1], parts[3]
        if local_sha == "0" * 40:
            continue
        if remote_sha == "0" * 40:
            rev_range = local_sha
        else:
            rev_range = f"{remote_sha}..{local_sha}"
        result = subprocess.run(
            ["git", "diff", "--name-only", rev_range],
            check=True,
            capture_output=True,
            text=True,
        )
        for path in result.stdout.splitlines():
            if path.strip():
                changed.add(path.strip())
    return sorted(changed)


def _collect_paths() -> list[str]:
    args = [a for a in sys.argv[1:] if a and not a.startswith("-")]
    stage = os.environ.get("PRE_COMMIT_STAGE", "")

    if stage == "pre-push":
        return _from_git_push_ref()
    if args:
        return args
    return _from_git_diff_cached()


def main() -> int:
    repo_root = Path.cwd()
    rel_paths = [_normalize(p) for p in _collect_paths()]
    violations: list[str] = []
    for rel in rel_paths:
        if rel in FORBIDDEN_EXACT:
            violations.append(rel)
            continue
        if any(rel.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            violations.append(rel)

    if not violations:
        return 0

    print("[BLOCK] parent repo must not commit/push local-notes managed paths:")
    for v in sorted(set(violations)):
        print(f"  - {v}")
    print("")
    print("Use local_notes repo instead:")
    print(f"  cd {repo_root / 'local_notes'}")
    print("  git add -A && git commit -m \"...\"")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
