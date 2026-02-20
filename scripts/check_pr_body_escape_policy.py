from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


TARGET_SUFFIXES = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".sh",
    ".ps1",
    ".psm1",
}

RE_FORBID_GH_PR_BODY = re.compile(
    r"\bgh\s+pr\s+(?:create|edit)\b[^\r\n]*\s--body(?!-file)(?:\s|=)",
    re.IGNORECASE,
)
RE_FORBID_POWERSHELL_DQ_HERESTRING = re.compile(r'@"')


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
        if ".git" in p.parts or "vendor" in p.parts:
            continue
        if p.suffix.lower() not in TARGET_SUFFIXES:
            continue
        yield p


def _iter_files_from_args(args: Sequence[str]) -> Iterable[Path]:
    for raw in args:
        p = Path(raw)
        if ".git" in p.parts or "vendor" in p.parts:
            continue
        if p.suffix.lower() not in TARGET_SUFFIXES:
            continue
        if not p.exists() or not p.is_file():
            continue
        yield p


def _scan_file(path: Path) -> List[Tuple[int, str]]:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []

    findings: List[Tuple[int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if RE_FORBID_GH_PR_BODY.search(line):
            findings.append(
                (
                    line_no,
                    "forbidden `gh pr ... --body` usage; use `--body-file <path>`",
                )
            )
        if RE_FORBID_POWERSHELL_DQ_HERESTRING.search(line):
            findings.append(
                (
                    line_no,
                    "forbidden PowerShell @\" here-string; use @'... '@ style",
                )
            )
    return findings


def main() -> int:
    total = 0
    targets = list(_iter_files_from_args(sys.argv[1:]))
    if not targets:
        targets = list(_iter_tracked_files())

    for path in targets:
        findings = _scan_file(path)
        for line_no, reason in findings:
            print(f"{path}:{line_no}: {reason}")
        total += len(findings)

    if total:
        print(
            "Detected forbidden PR body / PowerShell escaping patterns.",
            file=sys.stderr,
        )
        return 1

    print("No forbidden PR body / PowerShell escaping patterns found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
