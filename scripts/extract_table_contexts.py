from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


CHAPTER_HEADING_PATTERN = re.compile(r"^\s*第[0-9０-９一二三四五六七八九十百千]+章(?:\s+[^\s].*)?$")
NUMERIC_HEADING_PATTERN = re.compile(r"^\s*\d+(?:\.\d+){1,3}\s+[^\s].*$")
ROMAN_HEADING_PATTERN = re.compile(r"^\s*[IVXLC]+\.\s+[^\s].*$", re.IGNORECASE)

TABLE_CAPTION_PATTERN = re.compile(r"^\s*(?:Table|表)\s*[0-9０-９一二三四五六七八九十]+\s*[:：]?.*$", re.IGNORECASE)
NOTE_START_PATTERN = re.compile(r"^\s*(?:Note|Notes|NB|注|注記|備考|※|（注）)\s*[:：]?.*$", re.IGNORECASE)


def normalize_for_match(line: str) -> str:
    t = line.strip()
    # Strip common markdown emphasis wrappers.
    t = t.strip("*").strip()
    t = re.sub(r"\*\*(.*?)\*\*", r"\1", t)
    t = re.sub(r"__(.*?)__", r"\1", t)
    return t


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
    t = normalize_for_match(line)
    if not t:
        return False
    if "。" in t:
        return False
    if len(t) > 80:
        return False
    if "には" in t and CHAPTER_HEADING_PATTERN.match(t):
        return False
    if CHAPTER_HEADING_PATTERN.match(t):
        return True
    if NUMERIC_HEADING_PATTERN.match(t):
        return True
    if re.match(r"^[０-９]+(?:[．.][０-９]+){1,3}\s*[^\s].*$", t):
        return True
    if ROMAN_HEADING_PATTERN.match(t):
        return True
    if re.match(r"^[０-９一二三四五六七八九十百千]+[．.][０-９一二三四五六七八九十百千]+\s*[^\s].*$", t):
        return True
    if re.match(r"^[A-Z][A-Z0-9 /,&()'-]{5,}$", t):
        # Treat plain all-caps section banners as headings.
        alpha = [c for c in t if c.isalpha()]
        if alpha and sum(1 for c in alpha if c.isupper()) / len(alpha) >= 0.9:
            return True
    return False


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
        if TABLE_CAPTION_PATTERN.match(normalize_for_match(t)):
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
    while cur < len(lines):
        nxt = lines[cur]
        if not nxt.strip():
            break
        if "|" not in nxt:
            break
        rows.append((cur + 1, nxt))
        cur += 1
    if len(rows) < 3:
        return None
    last_row_zero_based = rows[-1][0] - 1
    return last_row_zero_based, rows


def collect_notes(lines: List[str], idx: int) -> Tuple[int, List[Tuple[int, str]]]:
    notes: List[Tuple[int, str]] = []
    cur = idx
    skipped_blank = 0
    while cur < len(lines):
        t = lines[cur].strip()
        if not t and not notes and skipped_blank < 2:
            skipped_blank += 1
            cur += 1
            continue
        if not t:
            break
        if not notes and not NOTE_START_PATTERN.match(normalize_for_match(t)):
            break
        if notes and is_heading_line(t):
            break
        if notes and not (NOTE_START_PATTERN.match(normalize_for_match(t)) or lines[cur].startswith((" ", "\t"))):
            break
        notes.append((cur + 1, lines[cur]))
        cur += 1
    return cur, notes


def read_text_with_fallback(path: Path) -> str:
    last_exc: Optional[Exception] = None
    for enc in ("utf-8", "cp932", "utf-16"):
        try:
            return path.read_text(encoding=enc)
        except Exception as exc:
            last_exc = exc
            continue
    if last_exc is not None:
        raise last_exc
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_from_file(path: Path) -> List[Dict[str, object]]:
    lines = read_text_with_fallback(path).splitlines()
    out: List[Dict[str, object]] = []
    i = 0
    while i < len(lines):
        caption_line_no: Optional[int] = None
        caption_text: Optional[str] = None
        caption_inferred = False
        caption_source: Optional[str] = None
        table_start = i

        line = normalize_for_match(lines[i])
        if TABLE_CAPTION_PATTERN.match(line):
            caption_line_no = i + 1
            caption_text = lines[i]
            caption_source = "inline_caption"
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
                caption_source = "nearby_caption"
        end_idx, table_lines = table_info
        after_idx, note_lines = collect_notes(lines, end_idx + 1)
        ancestor_idx_base = (caption_line_no - 1) if caption_line_no else table_start
        ancestors = find_ancestor_headings(lines, ancestor_idx_base)
        if caption_text is None and ancestors:
            nearest = ancestors[-1]
            caption_line_no = nearest[0]
            caption_text = nearest[1]
            caption_inferred = True
            caption_source = "heading_fallback"

        rec = {
            "source_path": _sanitize_path_for_output(str(path)),
            "ancestors": [{"line": ln, "text": txt} for ln, txt in ancestors],
            "table_caption": {"line": caption_line_no, "text": caption_text} if caption_text else None,
            "caption_inferred": caption_inferred,
            "caption_source": caption_source,
            "table_lines": [{"line": ln, "text": txt} for ln, txt in table_lines],
            "note_lines": [{"line": ln, "text": txt} for ln, txt in note_lines],
            "start_line": (caption_line_no or table_lines[0][0]),
            "end_line": (note_lines[-1][0] if note_lines else table_lines[-1][0]),
        }
        out.append(rec)
        i = after_idx
    return out


def _block_signature(rec: Dict[str, object]) -> str:
    payload = {
        "caption": rec.get("table_caption"),
        "table_lines": [x.get("text") for x in (rec.get("table_lines") or [])],
        "note_lines": [x.get("text") for x in (rec.get("note_lines") or [])],
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def dedupe_records(records: List[Dict[str, object]]) -> List[Dict[str, object]]:
    by_sig: Dict[str, Dict[str, object]] = {}
    order: List[str] = []
    for rec in records:
        sig = _block_signature(rec)
        if sig not in by_sig:
            rec_copy = dict(rec)
            rec_copy["source_paths"] = [rec["source_path"]]
            by_sig[sig] = rec_copy
            order.append(sig)
            continue
        existing = by_sig[sig]
        srcs = existing.setdefault("source_paths", [])
        if isinstance(srcs, list) and rec["source_path"] not in srcs:
            srcs.append(rec["source_path"])
    return [by_sig[sig] for sig in order]


def build_quality_summary(records: List[Dict[str, object]]) -> Dict[str, object]:
    caption_missing = 0
    caption_inferred_count = 0
    ancestors_missing = 0
    suspicious_ancestor = 0
    notes_found = 0
    for rec in records:
        if not rec.get("table_caption"):
            caption_missing += 1
        if rec.get("caption_inferred"):
            caption_inferred_count += 1
        ancestors = rec.get("ancestors") or []
        if not ancestors:
            ancestors_missing += 1
        for a in ancestors:
            text = str(a.get("text") or "")
            if text.endswith("。") or "には" in text:
                suspicious_ancestor += 1
                break
        if rec.get("note_lines"):
            notes_found += 1
    total = len(records)
    return {
        "records": total,
        "caption_missing_count": caption_missing,
        "caption_missing_ratio": (caption_missing / total) if total else 0.0,
        "caption_inferred_count": caption_inferred_count,
        "ancestors_missing_count": ancestors_missing,
        "ancestors_missing_ratio": (ancestors_missing / total) if total else 0.0,
        "suspicious_ancestor_count": suspicious_ancestor,
        "records_with_notes_count": notes_found,
    }


def gather_files(root: Path) -> List[Path]:
    files: List[Path] = []
    for ext in ("*.txt", "*.md"):
        files.extend(root.rglob(ext))
    return sorted(files)


def _sanitize_path_for_output(path: str) -> str:
    user_home = os.path.expanduser("~")
    if user_home:
        normalized = path.replace("\\", "/")
        home_normalized = user_home.replace("\\", "/")
        if normalized.lower().startswith(home_normalized.lower()):
            return "%USERPROFILE%" + normalized[len(home_normalized):]
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract table blocks with ancestor context.")
    parser.add_argument("--input-root", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-summary-json", type=Path, required=False)
    args = parser.parse_args()

    files = gather_files(args.input_root)
    all_records: List[Dict[str, object]] = []
    for f in files:
        all_records.extend(extract_from_file(f))
    unique_records = dedupe_records(all_records)
    summary = build_quality_summary(unique_records)

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)

    with args.output_jsonl.open("w", encoding="utf-8", newline="\n") as fj:
        for rec in unique_records:
            fj.write(json.dumps(rec, ensure_ascii=False) + "\n")
    if args.output_summary_json is not None:
        args.output_summary_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_summary_json.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    lines: List[str] = []
    lines.append("# Table Context Extraction")
    lines.append("")
    lines.append(f"- input_root: `{_sanitize_path_for_output(str(args.input_root))}`")
    lines.append(f"- extracted_blocks_raw: **{len(all_records)}**")
    lines.append(f"- extracted_blocks_unique: **{len(unique_records)}**")
    lines.append("- quality_summary:")
    lines.append(f"  - caption_missing_count: {summary['caption_missing_count']}")
    lines.append(f"  - caption_missing_ratio: {summary['caption_missing_ratio']:.3f}")
    lines.append(f"  - caption_inferred_count: {summary['caption_inferred_count']}")
    lines.append(f"  - ancestors_missing_count: {summary['ancestors_missing_count']}")
    lines.append(f"  - suspicious_ancestor_count: {summary['suspicious_ancestor_count']}")
    lines.append(f"  - records_with_notes_count: {summary['records_with_notes_count']}")
    lines.append("")
    for idx, rec in enumerate(unique_records, start=1):
        lines.append(f"## {idx}. `{rec['source_path']}`")
        srcs = rec.get("source_paths") or []
        if isinstance(srcs, list) and len(srcs) > 1:
            lines.append("")
            lines.append(f"- merged_sources: {len(srcs)}")
            for s in srcs:
                lines.append(f"  - `{s}`")
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
            caption_suffix = ""
            if rec.get("caption_inferred"):
                caption_suffix = " [inferred]"
            lines.append(f"  - L{caption['line']}: {caption['text']}{caption_suffix}")
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
    print(f"extracted_blocks_raw={len(all_records)}")
    print(f"extracted_blocks_unique={len(unique_records)}")
    print(
        "quality_summary="
        + json.dumps(summary, ensure_ascii=False, separators=(",", ":"))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
