from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    subprocess.run(["git", "config", "core.hooksPath", ".githooks"], check=True, cwd=repo_root)

    hook_dir = repo_root / ".githooks"
    required = [hook_dir / "pre-commit", hook_dir / "pre-push"]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        print("missing hook files:", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)
        return 1

    if os.name != "nt":
        for p in required:
            mode = p.stat().st_mode
            p.chmod(mode | 0o111)

    print("Configured git hooks:")
    print("  core.hooksPath = .githooks")
    print("  hooks: pre-commit, pre-push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
