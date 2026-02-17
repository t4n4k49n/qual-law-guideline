from __future__ import annotations

import argparse
import re
from pathlib import Path


def slice_annex(*, input_path: Path, output_path: Path, annex_no: int) -> int:
    lines = input_path.read_text(encoding="utf-8", errors="ignore").splitlines()
    start_pat = re.compile(rf"^ANNEX\s+{annex_no}\s*$", flags=re.IGNORECASE)
    end_pat = re.compile(rf"^ANNEX\s+{annex_no + 1}\b", flags=re.IGNORECASE)

    start = None
    end = None
    for idx, line in enumerate(lines):
        if start is None and start_pat.match(line.strip()):
            start = idx
            continue
        if start is not None and end_pat.match(line.strip()):
            end = idx
            break

    if start is None:
        raise SystemExit(f"ANNEX {annex_no} start not found in {input_path}")
    if end is None:
        end = len(lines)

    out_lines = lines[start:end]
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
    parser.add_argument("--annex", "--annex-no", dest="annex_no", required=True, type=int)
    args = parser.parse_args()

    count = slice_annex(
        input_path=args.input,
        output_path=args.output,
        annex_no=args.annex_no,
    )
    print(f"wrote {count} lines to {args.output}")


if __name__ == "__main__":
    main()
