from __future__ import annotations

import argparse
import re
from pathlib import Path

ANNEX_HEADING_RE = re.compile(
    r"(?i)^\s*(?:\[\s*)?ANNEX\s+(?P<id>\d+[A-Z]?)\s*(?:\]\s*)?$"
)


def _norm_annex_id(value: str) -> str:
    normalized = value.strip().upper()
    if not re.fullmatch(r"\d+[A-Z]?", normalized):
        raise SystemExit(
            f"Invalid annex id: {value!r}. Expected format like 1, 2A, 18."
        )
    return normalized


def slice_annex(*, input_path: Path, output_path: Path, annex_id: str) -> int:
    lines = input_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    target_annex_id = _norm_annex_id(annex_id)

    heading_positions: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        match = ANNEX_HEADING_RE.match(line.strip())
        if not match:
            continue
        heading_positions.append((idx, match.group("id").upper()))

    target_starts = [idx for idx, annex in heading_positions if annex == target_annex_id]
    if not target_starts:
        raise SystemExit(f"ANNEX {target_annex_id} start not found in {input_path}")

    best_start = None
    best_end = None
    best_len = -1
    for start in target_starts:
        end = len(lines)
        for idx, annex in heading_positions:
            if idx <= start:
                continue
            if annex != target_annex_id:
                end = idx
                break
        span_len = end - start
        if span_len > best_len:
            best_start = start
            best_end = end
            best_len = span_len

    if best_start is None or best_end is None:
        raise SystemExit(f"ANNEX {target_annex_id} range could not be determined in {input_path}")

    out_lines = lines[best_start:best_end]
    while out_lines and not out_lines[0].strip():
        out_lines.pop(0)
    while out_lines and not out_lines[-1].strip():
        out_lines.pop()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(out_lines) + "\n", encoding="utf-8", newline="\n")
    return len(out_lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Slice one annex block from PE 009-17 Annexes text."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--annex-id",
        "--annex",
        "--annex-no",
        dest="annex_id",
        required=True,
        type=str,
    )
    args = parser.parse_args()

    count = slice_annex(
        input_path=args.input,
        output_path=args.output,
        annex_id=args.annex_id,
    )
    print(f"wrote {count} lines to {args.output}")


if __name__ == "__main__":
    main()
