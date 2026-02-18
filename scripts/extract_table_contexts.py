from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


HEADING_PATTERNS = [
    re.compile(r"^\s*第[0-9０-９一二三四五六七八九十百千]+章"),
    re.compile(r"^\s*\d+(?:\.\d+){1,3}\s+"),
    re.compile(r"^\s*[IVXLC]+\.\s+", re.IGNORECASE),
]

TABLE_CAPTION_PATTERN = re.compile(r"^\s*(?:Table|表)\s*[0-9０-９一二三四五六七八九十]+\s*[:：]?.*$", re.IGNORECASE)
NOTE_START_PATTERN = re.compile(r"^\s*(?:Note|Notes|NB|注|注記|備考|※|（注）)\s*[:：]?.*$", re.IGNORECASE)


def looks_like_md_separator(line: str) -> bool:
    s = line.strip()
    if "|" not in s:
        return False
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    parts = [p.strip() for p in s.split("|")]
    if not parts:
        return False
    for p in parts:
        if not re.match(r"^:?-{3,}:?$", p):
            return False
    return True


def is_heading_line(line: str) -> bool:
    t = line.strip()
    if not t:
        return False
    return any(pat.match(t) for pat in HEADING_PATTERNS)


def find_ancestor_headings(lines: List[str], idx: int, max_count: int = 3) -> List[Tuple[int, str]]:
    found: List[Tuple[int, str]] = []
    cur = idx - 1
    while cur >= 0 and len(found) < max_count:
        t = lines[cur].strip()
        if t and is_heading_line(t):
            found.append((cur + 1, t))
        cur -= 1
    found.reverse()
    return found


def find_prev_non_empty(lines: List[str], idx: int) -> Optional[Tuple[int, str]]:
    cur = idx - 1
    while cur >= 0:
        t = lines[cur].strip()
        if t:
            return cur, t
        cur -= 1
    return None


def find_nearby_caption(lines: List[str], table_start_idx: int, max_lookback: int = 6) -> Optional[Tuple[int, str]]:
    cur = table_start_idx - 1
    looked = 0
    while cur >= 0 and looked < max_lookback:
        t = lines[cur].strip()
        if not t:
            cur -= 1
            looked += 1
            continue
        if TABLE_CAPTION_PATTERN.match(t):
            return cur, lines[cur]
        if "|" in t:
            return None
        cur -= 1
        looked += 1
    return None


def collect_table_from(lines: List[str], start_idx: int) -> Optional[Tuple[int, List[Tuple[int, str]]]]:
    # caption + md table
    if start_idx + 2 > len(lines) - 1:
        return None
    line = lines[start_idx].strip()
    if "|" not in line:
        return None
    if start_idx + 1 >= len(lines) or not looks_like_md_separator(lines[start_idx + 1]):
        return None
    rows: List[Tuple[int, str]] = [(start_idx + 1, lines[start_idx])]
    rows.append((start_idx + 2, lines[start_idx + 1]))
    cur = start_idx + 2
    while cur + 1 < len(lines):
        nxt = lines[cur + 1]
        if not nxt.strip():
            break
        if "|" not in nxt:
            break
        rows.append((cur + 2, nxt))
        cur += 1
    if len(rows) < 3:
        return None
    return cur + 1, rows


def collect_notes(lines: List[str], idx: int) -> Tuple[int, List[Tuple[int, str]]]:
    notes: List[Tuple[int, str]] = []
    cur = idx
    while cur < len(lines):
        t = lines[cur].strip()
        if not t:
            break
        if not notes and not NOTE_START_PATTERN.match(t):
            break
        if notes and is_heading_line(t):
            break
        if notes and not (NOTE_START_PATTERN.match(t) or lines[cur].startswith((" ", "\t"))):
            break
        notes.append((cur + 1, lines[cur]))
        cur += 1
    return cur, notes


def extract_from_file(path: Path) -> List[Dict[str, object]]:
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    out: List[Dict[str, object]] = []
    i = 0
    while i < len(lines):
        caption_line_no: Optional[int] = None
        caption_text: Optional[str] = None
        table_start = i

        line = lines[i].strip()
        if TABLE_CAPTION_PATTERN.match(line):
            caption_line_no = i + 1
            caption_text = lines[i]
            table_start = i + 1

        table_info = collect_table_from(lines, table_start)
        if table_info is None:
            i += 1
            continue
        if caption_text is None:
            nearby = find_nearby_caption(lines, table_start)
            if nearby is not None:
                caption_idx, caption_raw = nearby
                caption_line_no = caption_idx + 1
                caption_text = caption_raw
        end_idx, table_lines = table_info
        after_idx, note_lines = collect_notes(lines, end_idx + 1)
        ancestor_idx_base = (caption_line_no - 1) if caption_line_no else table_start
        ancestors = find_ancestor_headings(lines, ancestor_idx_base)

        rec = {
            "source_path": str(path),
            "ancestors": [{"line": ln, "text": txt} for ln, txt in ancestors],
            "table_caption": {"line": caption_line_no, "text": caption_text} if caption_text else None,
            "table_lines": [{"line": ln, "text": txt} for ln, txt in table_lines],
            "note_lines": [{"line": ln, "text": txt} for ln, txt in note_lines],
            "start_line": (caption_line_no or table_lines[0][0]),
            "end_line": (note_lines[-1][0] if note_lines else table_lines[-1][0]),
        }
        out.append(rec)
        i = after_idx
    return out


def gather_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for ext in ("*.txt", "*.md"):
        files.extend(root.rglob(ext))
    return sorted(files)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract table blocks with ancestor context.")
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    args = parser.parse_args()

    files = gather_files(args.input_root)
    all_records: List[Dict[str, object]] = []
    for f in files:
        all_records.extend(extract_from_file(f))

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)

    with args.output_jsonl.open("w", encoding="utf-8", newline="\n") as fj:
        for rec in all_records:
            fj.write(json.dumps(rec, ensure_ascii=False) + "\n")

    lines: List[str] = []
    lines.append("# Table Context Extraction")
    lines.append("")
    lines.append(f"- input_root: `{args.input_root}`")
    lines.append(f"- extracted_blocks: **{len(all_records)}**")
    lines.append("")
    for idx, rec in enumerate(all_records, start=1):
        lines.append(f"## {idx}. `{rec['source_path']}`")
        lines.append("")
        lines.append(f"- lines: {rec['start_line']}..{rec['end_line']}")
        ancestors = rec.get("ancestors") or []
        lines.append("- ancestors:")
        if ancestors:
            for a in ancestors:
                lines.append(f"  - L{a['line']}: {a['text']}")
        else:
            lines.append("  - (none)")
        caption = rec.get("table_caption")
        lines.append("- table_caption:")
        if caption:
            lines.append(f"  - L{caption['line']}: {caption['text']}")
        else:
            lines.append("  - (none)")
        lines.append("- table_block:")
        for t in rec.get("table_lines") or []:
            lines.append(f"  - L{t['line']}: {t['text']}")
        lines.append("- notes:")
        if rec.get("note_lines"):
            for n in rec["note_lines"]:
                lines.append(f"  - L{n['line']}: {n['text']}")
        else:
            lines.append("  - (none)")
        lines.append("")

    args.output_md.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote: {args.output_md}")
    print(f"wrote: {args.output_jsonl}")
    print(f"extracted_blocks={len(all_records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
