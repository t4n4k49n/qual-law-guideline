from __future__ import annotations

import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


TEXT_SUFFIXES = {
    ".py",
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".tsv",
    ".xml",
    ".html",
    ".css",
    ".js",
    ".ts",
    ".sh",
    ".ps1",
}

BIDI_RANGES: Sequence[Tuple[int, int]] = (
    (0x202A, 0x202E),
    (0x2066, 0x2069),
)
BIDI_SINGLES = {0x200E, 0x200F, 0x061C}
ALLOWED_CONTROL_CHARS = {0x09}


def _is_forbidden(cp: int) -> bool:
    if cp in BIDI_SINGLES:
        return True
    for lo, hi in BIDI_RANGES:
        if lo <= cp <= hi:
            return True
    if unicodedata.category(chr(cp)) == "Cc" and cp not in ALLOWED_CONTROL_CHARS:
        return True
    return False


def _iter_tracked_files() -> Iterable[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        check=True,
        capture_output=True,
    )
    raw = proc.stdout
    for chunk in raw.split(b"\x00"):
        if not chunk:
            continue
        p = Path(chunk.decode("utf-8", errors="replace"))
        if ".git" in p.parts or "vendor" in p.parts:
            continue
        if p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        yield p


def _iter_text_files_from_args(args: Sequence[str]) -> Iterable[Path]:
    for raw in args:
        p = Path(raw)
        if ".git" in p.parts or "vendor" in p.parts:
            continue
        if p.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if not p.exists() or not p.is_file():
            continue
        yield p


def _looks_binary(raw: bytes) -> bool:
    if b"\x00" in raw:
        return True
    return False


def _scan_file(path: Path) -> List[Tuple[int, int, int, str]]:
    raw = path.read_bytes()
    if _looks_binary(raw):
        return []
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return []
    findings: List[Tuple[int, int, int, str]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for col_no, ch in enumerate(line, start=1):
            cp = ord(ch)
            if not _is_forbidden(cp):
                continue
            findings.append((line_no, col_no, cp, unicodedata.name(ch, "UNKNOWN")))
    return findings


def main() -> int:
    total = 0
    targets = list(_iter_text_files_from_args(sys.argv[1:]))
    if not targets:
        targets = list(_iter_tracked_files())
    for path in targets:
        findings = _scan_file(path)
        for line_no, col_no, cp, name in findings:
            print(f"{path}:{line_no}:{col_no}: U+{cp:04X} {name}")
        total += len(findings)
    if total:
        print(
            f"Detected {total} forbidden character(s) "
            "(hidden/bidirectional or disallowed control).",
            file=sys.stderr,
        )
        return 1
    print("No hidden/bidirectional or disallowed control characters found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
