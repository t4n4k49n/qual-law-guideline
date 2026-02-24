#!/usr/bin/env python3
"""Block commits/pushes when TODO.md/KNOWLEDGE.md exist at parent repo root."""

from __future__ import annotations

from pathlib import Path


def main() -> int:
    repo_root = Path.cwd()
    forbidden = [repo_root / "TODO.md", repo_root / "KNOWLEDGE.md"]
    existing = [p.name for p in forbidden if p.exists()]
    if not existing:
        return 0

    print("[BLOCK] parent repo root must not contain these files:")
    for name in existing:
        print(f"  - {name}")
    print("")
    print("Use local_notes instead:")
    print(f"  - {repo_root / 'local_notes' / 'TODO.md'}")
    print(f"  - {repo_root / 'local_notes' / 'KNOWLEDGE.md'}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
