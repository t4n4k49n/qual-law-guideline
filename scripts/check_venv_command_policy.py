from __future__ import annotations

import re
import sys
from pathlib import Path

TARGET_FILES = (
    "README.md",
    "docs/TESTPLAN_XML2IR.md",
    ".github/workflows/forbid.yml",
)

DISALLOWED_PATTERNS = (
    re.compile(r"\bpython\s+-m\s+pytest\b"),
    re.compile(r"\bpython\s+-m\s+pip\s+install\b"),
    re.compile(r"(^|\s)pip\s+install\s", re.IGNORECASE),
)

ALLOWED_HINTS = (
    ".venv\\Scripts\\python.exe -m pytest",
    "./.venv/bin/python -m pytest",
    ".venv\\Scripts\\python.exe -m pip install",
    "./.venv/bin/python -m pip install",
)


def _is_allowed_line(line: str) -> bool:
    lowered = line.lower()
    return any(hint.lower() in lowered for hint in ALLOWED_HINTS)


def main() -> int:
    violations: list[tuple[str, int, str]] = []
    for raw_path in TARGET_FILES:
        path = Path(raw_path)
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        for idx, line in enumerate(lines, start=1):
            if _is_allowed_line(line):
                continue
            if any(pattern.search(line) for pattern in DISALLOWED_PATTERNS):
                violations.append((raw_path, idx, line.strip()))

    if not violations:
        return 0

    print("ERROR: .venv 未固定のコマンド記述を検出しました。", file=sys.stderr)
    print("Reason: 実行環境のずれで再現性が落ちるため。", file=sys.stderr)
    print("Fix examples:", file=sys.stderr)
    print("  Windows: .\\.venv\\Scripts\\python.exe -m pytest", file=sys.stderr)
    print("  Linux/macOS: ./.venv/bin/python -m pytest", file=sys.stderr)
    for file_path, line_no, line in violations:
        print(f"  - {file_path}:{line_no}: {line}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
