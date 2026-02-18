from __future__ import annotations

import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from qai_xml2ir.models_ir import IRDocument, Node, build_root
from qai_xml2ir.nid import NidBuilder
from qai_xml2ir.ord_key import assign_document_order

LOGGER = logging.getLogger(__name__)

GAP_WARN_MAX_BY_FAMILY = {
    "alpha": 2,
    "roman": 3,
    "digit": 2,
}

HYPHEN_WRAP_PATTERN = re.compile(r"([A-Za-z]{2,})[-\u2010\u2011]\s+([A-Za-z]{2,})")
HYPHEN_WORD_PATTERN = re.compile(r"\b[A-Za-z]+-[A-Za-z]+\b")
PLAIN_WORD_PATTERN = re.compile(r"\b[A-Za-z]{3,}\b")
PAGE_NUMBER_LINE_PATTERN = re.compile(r"^\s*\d{1,3}\s*$")
TOC_LIKE_HEADING_PATTERN = re.compile(r".+\s{2,}\d{1,3}\s*$")
FIGURE_TABLE_START_PATTERN = re.compile(r"^\s*(?:Figure|Table)\s+\d+[:\.]", re.IGNORECASE)
TABLE_CAPTION_PATTERN = re.compile(r"^\s*(?:Figure|Table|表)\s*\S*[:：\.]?\s+.+$", re.IGNORECASE)
TABLE_NOTE_TRIGGER_PATTERN = re.compile(
    r"^(?:Note|Notes|NOTE|NB|注|注記|備考|※|（注）)\b|^[*†‡•]\s+|^\([a-z0-9]+\)\s+",
    re.IGNORECASE,
)
DEFAULT_NOTE_START_REGEXES = [
    r"^(?:Note|Notes|NB)\b[:：]?\s*",
    r"^(注|注記|備考|※)\s*[:：]?\s*",
    r"^（注）\s*",
]
KEEP_HYPHEN_ALLOWLIST = {
    "time-stamped",
    "time-sequenced",
    "computer-generated",
    "system-based",
    "laboratory-acquired",
}
KEEP_PREFIXES = {
    "time",
    "non",
    "pre",
    "post",
    "re",
    "co",
    "self",
    "semi",
    "multi",
    "inter",
    "intra",
}
HEADING_CONTINUATION_ENDWORDS = {
    "and",
    "for",
    "to",
    "of",
    "in",
    "on",
    "with",
}
HEADING_CONTINUATION_BLOCK_WORDS = {"must", "shall", "should", "may"}


@dataclass
class MarkerMatch:
    marker_id: str
    kind: str
    kind_raw: Optional[str]
    num: Optional[str]
    raw_token: str
    span_end: int
    order: int


@dataclass
class LastSeen:
    value: int
    raw: str
    line_no: int
    sibling_index: int


@dataclass
class AppendState:
    pending_paragraph_break: bool = False
    in_pre: bool = False


@dataclass
class AttachCandidate:
    marker: MarkerMatch
    parent_idx: int
    parent_nid: str
    parent_kind: str
    pop_count: int
    value: Optional[int]
    family: Optional[str]
    continuity_score: int
    total_score: int
    diff: Optional[int]
    gap: Optional[int]
    had_last: bool
    rare_roman_penalized: bool


@dataclass
class SkipBlockRule:
    start_pattern: re.Pattern[str]
    end_pattern: re.Pattern[str]
    include_start: bool
    include_end: bool
    max_lines: int


@dataclass
class SkipBlockState:
    active: bool = False
    rule_index: Optional[int] = None
    seen_lines: int = 0
    start_line: int = 0


class _NodeFactory:
    def __init__(self, structural_kinds: set[str]) -> None:
        self._nid_builder = NidBuilder()
        self._structural_kinds = structural_kinds
        self._kind_prefix = {
            "part": "part",
            "subpart": "subpt",
            "section": "sec",
            "paragraph": "p",
            "item": "i",
            "subitem": "si",
            "table": "tbl",
            "table_header": "tblh",
            "table_row": "tblr",
            "preamble": "pre",
        }
        self._kind_counters: Dict[Tuple[str, str], int] = defaultdict(int)

    @staticmethod
    def _slug(value: Optional[str]) -> str:
        if not value:
            return ""
        slug = value.strip().lower().replace(".", "_")
        slug = re.sub(r"[^a-z0-9_]+", "_", slug)
        slug = re.sub(r"_+", "_", slug).strip("_")
        return slug

    def _token(self, kind: str, num: Optional[str], parent_nid: str) -> str:
        prefix = self._kind_prefix.get(kind, kind[:3])
        slug = self._slug(num)
        if slug:
            return f"{prefix}{slug}"
        key = (parent_nid, kind)
        self._kind_counters[key] += 1
        return f"{prefix}{self._kind_counters[key]}"

    def create_node(
        self,
        *,
        kind: str,
        kind_raw: Optional[str],
        num: Optional[str],
        line_no: int,
        source_label: str,
        parent_nid: str,
    ) -> Node:
        if kind in {"note", "history"}:
            role = "informative"
            normativity = None
        else:
            role = "structural" if kind in self._structural_kinds else "normative"
            normativity = None if role == "structural" else "must"
        token = self._token(kind, num, parent_nid)
        base_nid = token if parent_nid == "root" else f"{parent_nid}.{token}"
        nid = self._nid_builder.unique(base_nid)
        return Node(
            nid=nid,
            kind=kind,
            kind_raw=kind_raw,
            num=num,
            ord=None,
            heading=None,
            text=None,
            role=role,
            normativity=normativity,
            source_spans=[{"source_label": source_label, "locator": f"line:{line_no}"}],
        )


def _compile_markers(parser_profile: Dict[str, Any]) -> List[Tuple[Dict[str, Any], re.Pattern[str]]]:
    compiled: List[Tuple[Dict[str, Any], re.Pattern[str]]] = []
    for marker in parser_profile.get("marker_types", []):
        compiled.append((marker, re.compile(marker["match"])))
    return compiled


def _starts_with_any_marker(
    text: str,
    compiled_markers: List[Tuple[Dict[str, Any], re.Pattern[str]]],
) -> bool:
    for _, pattern in compiled_markers:
        if pattern.match(text):
            return True
    return False


def _find_structural_marker_end(
    text: str,
    compiled_markers: List[Tuple[Dict[str, Any], re.Pattern[str]]],
    structural_kinds: Set[str],
) -> Optional[Tuple[str, int]]:
    for marker, pattern in compiled_markers:
        if marker.get("kind") not in structural_kinds:
            continue
        matched = pattern.match(text)
        if matched:
            return str(marker.get("kind")), matched.end()
    return None


def _looks_like_heading_line(text: str) -> bool:
    candidate = text.strip()
    if not candidate:
        return False
    if len(candidate) > 120:
        return False
    if re.search(r"[.!?]\s*$", candidate):
        return False
    return True


def _strip_inline_patterns(text: str, strip_inline_regexes: List[re.Pattern[str]]) -> str:
    cleaned = text
    for pat in strip_inline_regexes:
        cleaned = pat.sub("", cleaned)
    return cleaned


def _is_md_table_separator(line: str) -> bool:
    candidate = line.strip()
    if not candidate:
        return False
    if "|" not in candidate:
        return False
    if candidate.startswith("|"):
        candidate = candidate[1:]
    if candidate.endswith("|"):
        candidate = candidate[:-1]
    cells = [cell.strip() for cell in candidate.split("|")]
    if not cells:
        return False
    for cell in cells:
        if not re.match(r"^:?-{3,}:?$", cell):
            return False
    return True


def _looks_like_md_table_header(line: str) -> bool:
    candidate = line.strip()
    if not candidate:
        return False
    return candidate.count("|") >= 2 and not _is_md_table_separator(candidate)


def _collect_md_table_block(
    lines: List[str],
    start_idx: int,
    strip_inline_regexes: List[re.Pattern[str]],
) -> Optional[Dict[str, Any]]:
    if start_idx + 2 >= len(lines):
        return None
    header_line = _strip_inline_patterns(lines[start_idx], strip_inline_regexes).strip()
    separator_line = _strip_inline_patterns(lines[start_idx + 1], strip_inline_regexes).strip()
    if not _looks_like_md_table_header(header_line):
        return None
    if not _is_md_table_separator(separator_line):
        return None
    row_entries: List[Tuple[int, str]] = []
    idx = start_idx + 2
    while idx < len(lines):
        row_line = _strip_inline_patterns(lines[idx], strip_inline_regexes).strip()
        if not row_line:
            break
        if "|" not in row_line:
            break
        if _is_md_table_separator(row_line):
            break
        row_entries.append((idx, row_line))
        idx += 1
    if not row_entries:
        return None
    return {
        "header_idx": start_idx,
        "header_line": header_line,
        "separator_idx": start_idx + 1,
        "separator_line": separator_line,
        "rows": row_entries,
        "end_idx": idx,
    }


def _collect_table_notes(
    lines: List[str],
    start_idx: int,
    strip_inline_regexes: List[re.Pattern[str]],
    drop_line_regexes: List[re.Pattern[str]],
    drop_line_exact: Set[str],
    compiled_markers: List[Tuple[Dict[str, Any], re.Pattern[str]]],
) -> Tuple[List[Tuple[int, str]], int]:
    if start_idx >= len(lines):
        return [], start_idx
    first_idx = start_idx
    blanks = 0
    while first_idx < len(lines):
        probe = _strip_inline_patterns(lines[first_idx], strip_inline_regexes).strip()
        if probe:
            break
        blanks += 1
        if blanks > 2:
            return [], start_idx
        first_idx += 1
    if first_idx >= len(lines):
        return [], start_idx
    first = _strip_inline_patterns(lines[first_idx], strip_inline_regexes).strip()
    if not first or not TABLE_NOTE_TRIGGER_PATTERN.match(first):
        return [], start_idx
    note_entries: List[Tuple[int, str]] = []
    idx = first_idx
    while idx < len(lines):
        raw = lines[idx]
        cleaned = _strip_inline_patterns(raw, strip_inline_regexes).strip()
        if not cleaned:
            break
        if cleaned in drop_line_exact or any(pat.match(cleaned) for pat in drop_line_regexes):
            break
        if _starts_with_any_marker(cleaned, compiled_markers):
            break
        if idx > start_idx:
            if TABLE_NOTE_TRIGGER_PATTERN.match(cleaned):
                pass
            elif raw.startswith(" ") or raw.startswith("\t"):
                pass
            else:
                break
        note_entries.append((idx, cleaned))
        idx += 1
    return note_entries, idx


def _find_table_caption(
    lines: List[str],
    header_idx: int,
    strip_inline_regexes: List[re.Pattern[str]],
) -> Optional[Tuple[int, str]]:
    idx = header_idx - 1
    while idx >= 0:
        candidate = _strip_inline_patterns(lines[idx], strip_inline_regexes).strip()
        if not candidate:
            idx -= 1
            continue
        candidate_plain = re.sub(r"^\*{1,2}(.*?)\*{1,2}$", r"\1", candidate).strip()
        candidate_plain = re.sub(r"^_{1,2}(.*?)_{1,2}$", r"\1", candidate_plain).strip()
        if TABLE_CAPTION_PATTERN.match(candidate_plain):
            return idx, candidate_plain
        return None
    return None


def _collect_note_block(
    lines: List[str],
    start_idx: int,
    *,
    strip_inline_regexes: List[re.Pattern[str]],
    drop_line_regexes: List[re.Pattern[str]],
    drop_line_exact: Set[str],
    compiled_markers: List[Tuple[Dict[str, Any], re.Pattern[str]]],
    start_patterns: List[re.Pattern[str]],
    max_lines: int,
) -> Tuple[List[Tuple[int, str]], int]:
    if start_idx >= len(lines):
        return [], start_idx
    first = _strip_inline_patterns(lines[start_idx], strip_inline_regexes).strip()
    if not first:
        return [], start_idx
    if not any(pat.match(first) for pat in start_patterns):
        return [], start_idx

    note_entries: List[Tuple[int, str]] = []
    idx = start_idx
    while idx < len(lines) and len(note_entries) < max_lines:
        raw = lines[idx]
        cleaned = _strip_inline_patterns(raw, strip_inline_regexes).strip()
        if not cleaned:
            break
        if cleaned in drop_line_exact or any(pat.match(cleaned) for pat in drop_line_regexes):
            break
        if idx > start_idx and _starts_with_any_marker(cleaned, compiled_markers):
            break
        if idx > start_idx and not (raw.startswith(" ") or raw.startswith("\t")):
            if any(pat.match(cleaned) for pat in start_patterns):
                pass
            else:
                break
        note_entries.append((idx, cleaned))
        idx += 1
    return note_entries, idx


def _is_punctuation_only(value: str) -> bool:
    return bool(value) and not re.sub(r"[\s\.\:\-–—]", "", value)


def _looks_like_heading_continuation(remainder: str, next_stripped: str) -> bool:
    # Avoid swallowing section labels like "PRINCIPLE" after an already-complete heading.
    if re.match(r"^[A-Z][A-Z\s/&()\-]{0,40}$", next_stripped) and len(next_stripped.split()) == 1:
        return False
    if re.search(r"\bPE\s*\d{3}-\d{2}\b", next_stripped, flags=re.IGNORECASE):
        return False
    if re.search(r"\b\d{1,3}\s+August\s+\d{4}\b", next_stripped, flags=re.IGNORECASE):
        return False
    if (
        len(next_stripped.split()) >= 2
        and re.match(r"^[A-Z0-9][A-Z0-9\s/&()\-]{1,200}$", remainder.strip())
        and re.match(r"^[A-Z0-9][A-Z0-9\s/&()\-]{1,200}$", next_stripped)
    ):
        return True
    if re.match(r"^[a-z]", next_stripped):
        return True
    if re.search(r"[–—\-:/]\s*$", remainder):
        return True
    remainder_words = re.findall(r"[A-Za-z]+", remainder.lower())
    if remainder_words and remainder_words[-1] in HEADING_CONTINUATION_ENDWORDS:
        return True
    if (
        len(remainder.strip()) <= 40
        and len(next_stripped) <= 40
        and not re.search(r"\b(?:must|shall|should|may)\b", next_stripped, flags=re.IGNORECASE)
    ):
        return True
    return False


def _join_mid_sentence_marker_refs_into_prev(
    lines: List[str],
    *,
    strip_inline_regexes: List[re.Pattern[str]],
    join_cfg: Dict[str, Any],
) -> List[str]:
    if not bool(join_cfg.get("enabled")):
        return lines
    kinds = {
        str(v).strip().lower()
        for v in (join_cfg.get("kinds") or [])
        if str(v).strip()
    }
    if not kinds:
        return lines
    max_ref_line_len_raw = join_cfg.get("max_ref_line_len", 40)
    max_ref_line_len = int(max_ref_line_len_raw) if str(max_ref_line_len_raw).strip() else 40
    if max_ref_line_len <= 0:
        max_ref_line_len = 40
    prev_must_not_end = re.compile(str(join_cfg.get("prev_must_not_end_regex") or r"[.!?]\s*$"))
    prev_prefer_endwords = [
        str(v).strip().lower()
        for v in (join_cfg.get("prev_prefer_endwords") or [])
        if str(v).strip()
    ]

    merged = list(lines)
    bare_patterns: List[re.Pattern[str]] = []
    if "annex" in kinds:
        bare_patterns.append(re.compile(r"(?i)^annex\s+\d+\.?\s*$"))
    if not bare_patterns:
        return merged

    for idx in range(1, len(merged)):
        raw = merged[idx]
        cleaned = _strip_inline_patterns(raw.lstrip(), strip_inline_regexes).strip()
        if not cleaned or len(cleaned) > max_ref_line_len:
            continue
        if not any(pat.match(cleaned) for pat in bare_patterns):
            continue
        prev_raw = merged[idx - 1]
        prev_cleaned = _strip_inline_patterns(prev_raw, strip_inline_regexes).strip()
        if not prev_cleaned:
            continue
        if prev_must_not_end.search(prev_cleaned):
            continue
        if prev_prefer_endwords:
            words = re.findall(r"[A-Za-z]+", prev_cleaned.lower())
            if words and words[-1] not in prev_prefer_endwords:
                continue
        merged[idx - 1] = f"{prev_raw.rstrip()} {cleaned}"
        merged[idx] = ""
    return merged


def _merge_structural_marker_heading_lines(
    lines: List[str],
    compiled_markers: List[Tuple[Dict[str, Any], re.Pattern[str]]],
    structural_kinds: Set[str],
    *,
    strip_inline_regexes: List[re.Pattern[str]],
    continuation_cfg: Dict[str, Any],
) -> List[str]:
    # Keep line count stable: merged next line is replaced with an empty line.
    merged = list(lines)
    continuation_enabled = bool(continuation_cfg.get("enabled"))
    continuation_kinds = {
        str(v).strip().lower()
        for v in (continuation_cfg.get("kinds") or [])
        if str(v).strip()
    }
    max_next_line_len_raw = continuation_cfg.get("max_next_line_len", 60)
    max_next_line_len = int(max_next_line_len_raw) if str(max_next_line_len_raw).strip() else 60
    max_merge_lines_raw = continuation_cfg.get("max_merge_lines", 2)
    max_merge_lines = int(max_merge_lines_raw) if str(max_merge_lines_raw).strip() else 2
    max_blank_lookahead_raw = continuation_cfg.get("max_blank_lookahead", 2)
    max_blank_lookahead = (
        int(max_blank_lookahead_raw) if str(max_blank_lookahead_raw).strip() else 2
    )
    if max_next_line_len <= 0:
        max_next_line_len = 60
    if max_merge_lines <= 0:
        max_merge_lines = 1
    if max_blank_lookahead < 0:
        max_blank_lookahead = 0
    idx = 0
    while idx < len(merged) - 1:
        current = merged[idx]
        if not current.strip():
            idx += 1
            continue
        current_stripped = current.lstrip()
        current_cleaned = _strip_inline_patterns(current_stripped, strip_inline_regexes)
        marker_info = _find_structural_marker_end(
            current_cleaned,
            compiled_markers,
            structural_kinds,
        )
        if marker_info is None:
            idx += 1
            continue
        marker_kind, marker_end = marker_info
        merged_any = False
        merged_count = 0
        while merged_count < max_merge_lines:
            current_stripped = merged[idx].lstrip()
            current_cleaned = _strip_inline_patterns(current_stripped, strip_inline_regexes)
            current_marker_info = _find_structural_marker_end(
                current_cleaned,
                compiled_markers,
                structural_kinds,
            )
            if current_marker_info is None:
                break
            marker_kind, marker_end = current_marker_info
            remainder = current_cleaned[marker_end:].strip()
            remainder_for_rule = "" if _is_punctuation_only(remainder) else remainder

            next_idx = idx + 1
            blank_count = 0
            while (
                next_idx < len(merged)
                and not merged[next_idx].strip()
                and blank_count < max_blank_lookahead
            ):
                next_idx += 1
                blank_count += 1
            if next_idx >= len(merged):
                break

            next_line = merged[next_idx]
            next_cleaned = _strip_inline_patterns(next_line, strip_inline_regexes)
            next_stripped = next_cleaned.strip()
            if not next_stripped:
                break
            if _looks_like_md_table_header(next_stripped):
                break
            if TABLE_CAPTION_PATTERN.match(next_stripped):
                probe_idx = next_idx + 1
                while probe_idx < len(merged) and not merged[probe_idx].strip():
                    probe_idx += 1
                if probe_idx + 1 < len(merged):
                    probe_header = _strip_inline_patterns(merged[probe_idx], strip_inline_regexes).strip()
                    probe_sep = _strip_inline_patterns(merged[probe_idx + 1], strip_inline_regexes).strip()
                    if _looks_like_md_table_header(probe_header) and _is_md_table_separator(probe_sep):
                        break
            if _starts_with_any_marker(next_cleaned.lstrip(), compiled_markers):
                break
            if not _looks_like_heading_line(next_stripped):
                break
            should_merge = False
            if not remainder_for_rule:
                if not continuation_enabled:
                    should_merge = True
                elif marker_kind in continuation_kinds and len(next_stripped) <= max_next_line_len:
                    should_merge = True
            elif (
                continuation_enabled
                and marker_kind in continuation_kinds
                and len(next_stripped) <= max_next_line_len
                and _looks_like_heading_continuation(remainder_for_rule, next_stripped)
            ):
                should_merge = True

            if not should_merge:
                break

            merged[idx] = f"{merged[idx].rstrip()} {next_stripped}"
            merged[next_idx] = ""
            merged_any = True
            merged_count += 1

            merged_cleaned = _strip_inline_patterns(merged[idx].lstrip(), strip_inline_regexes)
            merged_marker_info = _find_structural_marker_end(
                merged_cleaned,
                compiled_markers,
                structural_kinds,
            )
            merged_remainder = (
                merged_cleaned[merged_marker_info[1] :].strip() if merged_marker_info else ""
            )
            if re.search(
                r"\b(?:must|shall|should|may)\b",
                merged_remainder,
                flags=re.IGNORECASE,
            ):
                break

        if merged_any:
            idx += 1
        else:
            idx += 1
    return merged


def _extract_num(marker: Dict[str, Any], match: re.Match[str]) -> Optional[str]:
    groups = match.groupdict() if match.groupdict() else {}
    num_group = marker.get("num_group")
    if isinstance(num_group, str):
        selected = groups.get(num_group)
        if selected:
            return selected
    direct = groups.get("num")
    if direct:
        return direct
    for key in groups:
        value = groups.get(key)
        if value:
            return value
    return None


def _structure_children(parent_kind: str, structure: Dict[str, Any]) -> List[str]:
    key = "root" if parent_kind == "document" else parent_kind
    row = structure.get(key) or {}
    children = row.get("children") or []
    return [str(v) for v in children]


def _find_parent_candidate(
    stack: List[Node],
    new_kind: str,
    structure: Dict[str, Any],
) -> Optional[int]:
    for idx in range(len(stack) - 1, -1, -1):
        allowed = _structure_children(stack[idx].kind, structure)
        if new_kind in allowed:
            return idx
    return None


def _find_parent_candidates(
    stack: List[Node],
    new_kind: str,
    structure: Dict[str, Any],
) -> List[int]:
    matches: List[int] = []
    for idx in range(len(stack) - 1, -1, -1):
        allowed = _structure_children(stack[idx].kind, structure)
        if new_kind in allowed:
            matches.append(idx)
    return matches


def _roman_to_int(value: str) -> Optional[int]:
    roman_values = {
        "i": 1,
        "v": 5,
        "x": 10,
        "l": 50,
        "c": 100,
        "d": 500,
        "m": 1000,
    }
    text = value.strip().lower()
    if not text or any(ch not in roman_values for ch in text):
        return None
    total = 0
    prev = 0
    for ch in reversed(text):
        cur = roman_values[ch]
        if cur < prev:
            total -= cur
        else:
            total += cur
            prev = cur
    return total


def _marker_family(marker: MarkerMatch) -> Optional[str]:
    marker_id = marker.marker_id.lower()
    if "alpha" in marker_id:
        return "alpha"
    if "roman" in marker_id:
        return "roman"
    if "digit" in marker_id:
        return "digit"
    if marker.num and marker.num.isdigit():
        return "digit"
    if marker.num and len(marker.num) == 1 and marker.num.isalpha():
        return "alpha"
    if marker.num and re.fullmatch(r"[ivxlcdm]+", marker.num.lower()):
        return "roman"
    return None


def _parse_marker_value(marker: MarkerMatch) -> Optional[int]:
    if marker.num is None:
        return None
    family = _marker_family(marker)
    raw = marker.num.strip().lower()
    if family == "alpha" and len(raw) == 1 and raw.isalpha():
        return ord(raw) - ord("a") + 1
    if family == "digit" and raw.isdigit():
        return int(raw)
    if family == "roman":
        return _roman_to_int(raw)
    return None


def _score_candidate(
    *,
    candidate: AttachCandidate,
    parent_last_seen: Dict[str, LastSeen],
) -> AttachCandidate:
    score = 0
    continuity_score = 0
    diff: Optional[int] = None
    gap: Optional[int] = None
    had_last = False
    rare_roman_penalized = False

    score -= candidate.pop_count * 5

    if candidate.value is not None:
        last = parent_last_seen.get(candidate.marker.marker_id)
        if last is not None:
            had_last = True
            diff = candidate.value - last.value
            if diff == 1:
                continuity_score = 100
            elif diff >= 2:
                gap = diff - 1
                max_gap = GAP_WARN_MAX_BY_FAMILY.get(candidate.family or "", 0)
                if gap <= max_gap:
                    continuity_score = 60 - 10 * gap
                else:
                    continuity_score = -30
            else:
                continuity_score = -50
        if (
            candidate.family == "roman"
            and not had_last
            and candidate.marker.num is not None
            and len(candidate.marker.num.strip()) == 1
            and candidate.value >= 50
        ):
            score -= 40
            rare_roman_penalized = True

    score += continuity_score
    candidate.total_score = score
    candidate.continuity_score = continuity_score
    candidate.diff = diff
    candidate.gap = gap
    candidate.had_last = had_last
    candidate.rare_roman_penalized = rare_roman_penalized
    return candidate


def _choose_best_candidate(candidates: List[AttachCandidate]) -> AttachCandidate:
    return max(
        candidates,
        key=lambda c: (
            c.total_score,
            c.continuity_score,
            -c.pop_count,
            -c.marker.order,
        ),
    )


def _select_marker_with_context(
    text: str,
    compiled_markers: List[Tuple[Dict[str, Any], re.Pattern[str]]],
    stack: List[Node],
    structure: Dict[str, Any],
    parent_last_seen: Dict[str, Dict[str, LastSeen]],
    line_no: int,
) -> Tuple[Optional[AttachCandidate], List[MarkerMatch]]:
    marker_matches: List[MarkerMatch] = []
    for order, (marker, pattern) in enumerate(compiled_markers):
        m = pattern.match(text)
        if not m:
            continue
        marker_matches.append(
            MarkerMatch(
                marker_id=str(marker.get("id") or f"marker_{order}"),
                kind=marker["kind"],
                kind_raw=marker.get("kind_raw"),
                num=_extract_num(marker, m),
                raw_token=m.group(0).strip(),
                span_end=m.end(),
                order=order,
            )
        )
    if not marker_matches:
        return None, []

    candidates: List[AttachCandidate] = []
    top_idx = len(stack) - 1
    for marker_match in marker_matches:
        for parent_idx in _find_parent_candidates(stack, marker_match.kind, structure):
            parent = stack[parent_idx]
            parent_state = parent_last_seen.get(parent.nid, {})
            value = _parse_marker_value(marker_match)
            family = _marker_family(marker_match)
            base = AttachCandidate(
                marker=marker_match,
                parent_idx=parent_idx,
                parent_nid=parent.nid,
                parent_kind=parent.kind,
                pop_count=top_idx - parent_idx,
                value=value,
                family=family,
                continuity_score=0,
                total_score=0,
                diff=None,
                gap=None,
                had_last=False,
                rare_roman_penalized=False,
            )
            candidates.append(
                _score_candidate(
                    candidate=base,
                    parent_last_seen=parent_state,
                )
            )

    if not candidates:
        return None, marker_matches

    chosen = _choose_best_candidate(candidates)
    if len(marker_matches) > 1:
        raw_marker = text[: chosen.marker.span_end].strip()
        matched_marker_ids = ",".join(m.marker_id for m in marker_matches)
        alpha_last = parent_last_seen.get(chosen.parent_nid, {}).get("paren_alpha")
        roman_last = parent_last_seen.get(chosen.parent_nid, {}).get("paren_roman")
        LOGGER.warning(
            "marker ambiguity resolved at line=%s raw=%r matched=[%s] chosen=%s/%s parent=%s/%s alpha_last=%s roman_last=%s diff=%s gap=%s score=%s",
            line_no,
            raw_marker,
            matched_marker_ids,
            chosen.marker.marker_id,
            chosen.marker.kind,
            chosen.parent_kind,
            chosen.parent_nid,
            alpha_last.raw if alpha_last else None,
            roman_last.raw if roman_last else None,
            chosen.diff,
            chosen.gap,
            chosen.total_score,
        )
    if chosen.gap is not None and chosen.gap >= 1:
        LOGGER.warning(
            "marker gap adopted at line=%s marker=%s raw=%r parent=%s/%s diff=%s gap=%s",
            line_no,
            chosen.marker.marker_id,
            text[: chosen.marker.span_end].strip(),
            chosen.parent_kind,
            chosen.parent_nid,
            chosen.diff,
            chosen.gap,
        )
    if chosen.rare_roman_penalized and chosen.marker.marker_id == "paren_roman":
        LOGGER.warning(
            "rare roman adoption at line=%s marker=%s raw=%r parent=%s/%s score=%s",
            line_no,
            chosen.marker.marker_id,
            text[: chosen.marker.span_end].strip(),
            chosen.parent_kind,
            chosen.parent_nid,
            chosen.total_score,
        )
    return chosen, marker_matches


def normalize_visible_chars(s: str) -> str:
    return s.replace("\r", "").replace("\u00ad", "").rstrip()


def _leading_space_count(raw_line: str) -> int:
    return len(raw_line) - len(raw_line.lstrip(" "))


def is_preformatted_line(raw_line: str) -> bool:
    if not raw_line:
        return False
    if re.match(r"^\s*[↓↑←→↕↔]+\s*$", raw_line):
        return True
    leading_spaces = _leading_space_count(raw_line)
    if raw_line.startswith("\t"):
        return True
    if leading_spaces >= 12:
        return True
    if "|" in raw_line:
        return True
    if re.search(r"[-=]{5,}", raw_line):
        return True
    core = raw_line.lstrip(" ")
    if leading_spaces >= 4 and re.search(r" {2,}", core):
        return True
    if len(re.findall(r" {2,}", core)) >= 2:
        return True
    return False


def _is_preformatted_text_block(text: str) -> bool:
    if "\n" not in text:
        return False
    if any(FIGURE_TABLE_START_PATTERN.match(line) for line in text.splitlines()):
        return True
    return any(is_preformatted_line(line) for line in text.splitlines())


def _get_append_state(
    states: Dict[Tuple[str, str], AppendState],
    node: Node,
    field: str,
) -> AppendState:
    key = (node.nid, field)
    state = states.get(key)
    if state is None:
        state = AppendState()
        states[key] = state
    return state


def _append_content(
    node: Node,
    raw_line: str,
    *,
    field: str,
    line_no: int,
    source_label: str,
    states: Dict[Tuple[str, str], AppendState],
) -> None:
    state = _get_append_state(states, node, field)
    normalized = normalize_visible_chars(raw_line)
    if not normalized.strip():
        state.pending_paragraph_break = True
        return

    pre = is_preformatted_line(normalized)
    current_value = getattr(node, field) or ""
    incoming = normalized if pre else normalized.lstrip()
    if not incoming:
        state.pending_paragraph_break = True
        return

    if not current_value:
        updated = incoming
    else:
        if state.in_pre or pre:
            sep = "\n"
        elif state.pending_paragraph_break:
            sep = "\n\n"
        else:
            sep = " "
        updated = f"{current_value}{sep}{incoming}"

    setattr(node, field, updated)
    state.pending_paragraph_break = False
    state.in_pre = pre

    span = {"source_label": source_label, "locator": f"line:{line_no}"}
    if not node.source_spans or node.source_spans[-1] != span:
        node.source_spans.append(span)


def _mark_pending_break(
    node: Node,
    *,
    field: str,
    states: Dict[Tuple[str, str], AppendState],
) -> None:
    state = _get_append_state(states, node, field)
    state.pending_paragraph_break = True


def _append_text(
    node: Node,
    line: str,
    line_no: int,
    source_label: str,
    states: Dict[Tuple[str, str], AppendState],
) -> None:
    _append_content(
        node,
        line,
        field="text",
        line_no=line_no,
        source_label=source_label,
        states=states,
    )


def _append_heading(
    node: Node,
    line: str,
    line_no: int,
    source_label: str,
    states: Dict[Tuple[str, str], AppendState],
) -> None:
    _append_content(
        node,
        line,
        field="heading",
        line_no=line_no,
        source_label=source_label,
        states=states,
    )


def _repair_hyphenated_wraps(
    text: str,
    *,
    hyphen_words: Set[str],
    plain_words: Set[str],
) -> str:
    def _choose(match: re.Match[str]) -> str:
        left = match.group(1)
        right = match.group(2)
        keep = f"{left}-{right}"
        drop = f"{left}{right}"
        keep_l = keep.lower()
        drop_l = drop.lower()
        left_l = left.lower()
        if keep_l in KEEP_HYPHEN_ALLOWLIST or keep_l in hyphen_words:
            return keep
        if drop_l in plain_words:
            return drop
        if left_l in KEEP_PREFIXES:
            return keep
        return drop

    previous = text
    while True:
        updated = HYPHEN_WRAP_PATTERN.sub(_choose, previous)
        if updated == previous:
            return updated
        previous = updated


def _collect_word_sets(root: Node) -> Tuple[Set[str], Set[str]]:
    hyphen_words: Set[str] = set()
    plain_words: Set[str] = set()

    def _visit(node: Node) -> None:
        for value in (node.heading, node.text):
            if not value:
                continue
            hyphen_words.update(word.lower() for word in HYPHEN_WORD_PATTERN.findall(value))
            plain_words.update(word.lower() for word in PLAIN_WORD_PATTERN.findall(value))
        for child in node.children:
            _visit(child)

    _visit(root)
    return hyphen_words, plain_words


def _postprocess_node_text(
    root: Node,
    *,
    hyphen_words: Set[str],
    plain_words: Set[str],
) -> None:
    def _visit(node: Node) -> None:
        for field in ("heading", "text"):
            value = getattr(node, field)
            if not value:
                continue
            parts = value.split("\n\n")
            processed: List[str] = []
            for part in parts:
                if _is_preformatted_text_block(part):
                    processed.append(
                        _repair_hyphenated_wraps(
                            part,
                            hyphen_words=hyphen_words,
                            plain_words=plain_words,
                        )
                    )
                    continue
                folded = part.replace("\n", " ")
                processed.append(
                    _repair_hyphenated_wraps(
                        folded,
                        hyphen_words=hyphen_words,
                        plain_words=plain_words,
                    )
                )
            setattr(
                node,
                field,
                _repair_hyphenated_wraps(
                    "\n\n".join(processed),
                    hyphen_words=hyphen_words,
                    plain_words=plain_words,
                ),
            )
        for child in node.children:
            _visit(child)

    _visit(root)


def _qualitycheck_structure(parent: Node, warnings: List[str]) -> None:
    sibling_counts: Dict[Tuple[str, str], int] = defaultdict(int)
    for child in parent.children:
        if child.role == "structural" and child.num:
            sibling_counts[(child.kind, child.num)] += 1
    for (kind, num), count in sibling_counts.items():
        if count > 1:
            warnings.append(
                f"{parent.nid}: duplicate structural siblings kind={kind} num={num} count={count}"
            )
    for child in parent.children:
        _qualitycheck_structure(child, warnings)


def _qualitycheck_toc_like_headings(node: Node, warnings: List[str]) -> None:
    if node.kind in {"chapter", "annex"} and node.heading:
        heading = node.heading.strip()
        if len(heading) >= 20 and TOC_LIKE_HEADING_PATTERN.match(heading):
            warnings.append(f"{node.nid}: heading looks like TOC entry")
    for child in node.children:
        _qualitycheck_toc_like_headings(child, warnings)


def _nest_root_chapters_under_parts(root: Node) -> None:
    if not root.children:
        return
    if not any(child.kind == "part" for child in root.children):
        return

    nested_root_children: List[Node] = []
    active_part: Optional[Node] = None
    pending_chapters_before_first_part: List[Node] = []
    for child in root.children:
        if child.kind == "part":
            if pending_chapters_before_first_part:
                child.children = pending_chapters_before_first_part + child.children
                pending_chapters_before_first_part = []
            active_part = child
            nested_root_children.append(child)
            continue
        if child.kind == "chapter" and active_part is not None:
            active_part.children.append(child)
            continue
        if child.kind == "chapter":
            pending_chapters_before_first_part.append(child)
            continue
        if child.kind == "annex":
            active_part = None
        nested_root_children.append(child)
    if pending_chapters_before_first_part:
        nested_root_children.extend(pending_chapters_before_first_part)
    root.children = nested_root_children


def qualitycheck_document(root: Node) -> List[str]:
    warnings: List[str] = []

    def _visit(node: Node) -> None:
        for field in ("heading", "text"):
            value = getattr(node, field)
            if not value:
                continue
            for line in value.splitlines():
                if PAGE_NUMBER_LINE_PATTERN.match(line):
                    warnings.append(f"{node.nid}:{field}: page-number-only line remains")
                    break
            if HYPHEN_WRAP_PATTERN.search(value):
                warnings.append(f"{node.nid}:{field}: unresolved hyphen-space pattern remains")
            is_pre = _is_preformatted_text_block(value)
            if "\n" in value and "\n\n" not in value and not is_pre:
                warnings.append(f"{node.nid}:{field}: single newline remains in prose")
        for child in node.children:
            _visit(child)

    _visit(root)
    _qualitycheck_structure(root, warnings)
    _qualitycheck_toc_like_headings(root, warnings)
    return warnings


def run_text_postprocess_and_qualitycheck(root: Node) -> List[str]:
    hyphen_words, plain_words = _collect_word_sets(root)
    _postprocess_node_text(root, hyphen_words=hyphen_words, plain_words=plain_words)
    return qualitycheck_document(root)


def _find_latest_non_note_stack_index(stack: List[Node]) -> Optional[int]:
    for idx in range(len(stack) - 1, -1, -1):
        kind = stack[idx].kind
        if kind in {"document", "note", "history"}:
            continue
        return idx
    return None


def _resolved_kind_raw(marker: MarkerMatch) -> Optional[str]:
    if marker.kind in {"paragraph", "item", "subitem"}:
        return marker.raw_token or marker.kind_raw
    return marker.kind_raw or marker.raw_token


def _normalize_structural_heading(kind: str, heading: str) -> str:
    if kind in {"part", "subpart"}:
        return heading.lstrip("—–- ").strip()
    return heading.strip()


def _split_section_heading_and_chapeau(remaining: str) -> Tuple[str, Optional[str]]:
    text = remaining.strip()
    if not text:
        return "", None
    m = re.search(r"\.\s+([A-Z0-9(])", text)
    if not m:
        return text, None
    split_pos = m.start() + 1
    heading = text[:split_pos].strip()
    chapeau = text[split_pos:].strip()
    return heading, chapeau or None


def _build_display_name(node: Node) -> str:
    if node.heading:
        return node.heading
    if node.num:
        return f"{node.kind} {node.num}"
    return node.kind


def _find_last_in_stack(stack: List[Node], kind: str) -> Optional[Node]:
    for node in reversed(stack):
        if node.kind == kind:
            return node
    return None


def _norm(value: str) -> str:
    lowered = value.lower().strip()
    lowered = re.sub(r"[\(\)\[\]\{\}:;,.]", " ", lowered)
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered.strip()


def _is_same_or_prefix(left: str, right: str) -> bool:
    return left == right or left.startswith(right) or right.startswith(left)


def _should_drop_repeated_structural_header_line(
    stripped_raw: str,
    stack: List[Node],
    kinds: Set[str],
) -> bool:
    if not stripped_raw:
        return False
    root = stack[0] if stack else None
    if "part" in kinds:
        part_match = re.match(r"(?i)^PART\s+(?P<n>[IVXLCDM]+)\.?\s*(?P<title>.*)$", stripped_raw)
        if part_match:
            part_num = part_match.group("n").strip().upper()
            part_title = part_match.group("title").strip()
            part = _find_last_in_stack(stack, "part")
            # Empty-title lines can be real structural markers, so only drop when
            # the same part is clearly repeated while already inside that part.
            if not part_title:
                if part and part.num and part.num.upper() == part_num:
                    return True
            else:
                line_heading = _norm(part_title)
                if part and part.num and part.num.upper() == part_num and part.heading:
                    part_heading = _norm(part.heading)
                    if line_heading and part_heading and _is_same_or_prefix(line_heading, part_heading):
                        return True
                if root:
                    for sibling in root.children:
                        if sibling.kind != "part" or not sibling.num:
                            continue
                        if sibling.num.upper() != part_num or not sibling.heading:
                            continue
                        part_heading = _norm(sibling.heading)
                        if line_heading and part_heading and _is_same_or_prefix(line_heading, part_heading):
                            return True
    if "chapter" in kinds:
        chapter = _find_last_in_stack(stack, "chapter")
        chapter_match = re.match(r"^(?P<n>\d{1,2})\.\s+(?P<title>.+)$", stripped_raw)
        if chapter and chapter.num and chapter.heading and chapter_match and chapter_match.group("n") == chapter.num:
            line_heading = _norm(chapter_match.group("title"))
            chapter_heading = _norm(chapter.heading)
            if line_heading and chapter_heading and _is_same_or_prefix(line_heading, chapter_heading):
                return True
        chapter_word_match = re.match(r"(?i)^chapter\s+(?P<n>\d{1,2})\b\s*(?P<title>.*)$", stripped_raw)
        if chapter and chapter.num and chapter_word_match and chapter_word_match.group("n") == chapter.num:
            chapter_word_title = chapter_word_match.group("title").strip()
            chapter_word_title = chapter_word_title.lstrip(".:- ").strip()
            if not chapter_word_title:
                return True
            if chapter.heading:
                line_heading = _norm(chapter_word_title)
                chapter_heading = _norm(chapter.heading)
                if line_heading and chapter_heading and _is_same_or_prefix(line_heading, chapter_heading):
                    return True
        if chapter_match and root:
            chapter_num = chapter_match.group("n")
            line_heading = _norm(chapter_match.group("title"))
            for sibling in root.children:
                if sibling.kind != "chapter" or sibling.num != chapter_num or not sibling.heading:
                    continue
                chapter_heading = _norm(sibling.heading)
                if line_heading and chapter_heading and _is_same_or_prefix(line_heading, chapter_heading):
                    return True
    if "annex" in kinds:
        annex_match = re.match(r"(?i)^annex\s+(?P<n>\d+)\b", stripped_raw)
        annex_title = ""
        if annex_match:
            annex_title = stripped_raw[annex_match.end() :].strip()
            annex_title = annex_title.lstrip(".:- ").strip()
        annex = _find_last_in_stack(stack, "annex")
        in_same_annex_context = bool(
            annex and annex.num and annex_match and annex_match.group("n") == annex.num
        )
        if in_same_annex_context:
            if not annex.heading or not annex_title:
                return True
            line_heading = _norm(annex_title)
            annex_heading = _norm(annex.heading)
            if line_heading and annex_heading and _is_same_or_prefix(line_heading, annex_heading):
                return True
            return True
        if annex_match and root and in_same_annex_context:
            annex_num = annex_match.group("n")
            for sibling in root.children:
                if sibling.kind != "annex" or sibling.num != annex_num:
                    continue
                if not sibling.heading or not annex_title:
                    return True
                line_heading = _norm(annex_title)
                annex_heading = _norm(sibling.heading)
                if line_heading and annex_heading and _is_same_or_prefix(line_heading, annex_heading):
                    return True
                return True
    return False


def _collect_display_names(node: Node, table: Dict[str, str]) -> None:
    table[node.nid] = _build_display_name(node)
    for child in node.children:
        _collect_display_names(child, table)


def _compile_skip_blocks(preprocess: Dict[str, Any]) -> List[SkipBlockRule]:
    raw_blocks = preprocess.get("skip_blocks") or []
    rules: List[SkipBlockRule] = []
    for raw in raw_blocks:
        if not isinstance(raw, dict):
            continue
        start_regex = raw.get("start_regex")
        end_regex = raw.get("end_regex")
        if not isinstance(start_regex, str) or not start_regex:
            continue
        if not isinstance(end_regex, str) or not end_regex:
            continue
        include_start = bool(raw.get("include_start", False))
        include_end = bool(raw.get("include_end", True))
        max_lines_raw = raw.get("max_lines", 2000)
        max_lines = int(max_lines_raw) if isinstance(max_lines_raw, (int, float, str)) else 2000
        if max_lines <= 0:
            max_lines = 2000
        rules.append(
            SkipBlockRule(
                start_pattern=re.compile(start_regex),
                end_pattern=re.compile(end_regex),
                include_start=include_start,
                include_end=include_end,
                max_lines=max_lines,
            )
        )
    return rules


def _locator_line_number(locator: str) -> Optional[int]:
    matched = re.match(r"^line:(\d+)$", locator.strip())
    if not matched:
        return None
    return int(matched.group(1))


def _node_start_line(node: Node) -> Optional[int]:
    lines: List[int] = []
    for span in node.source_spans or []:
        locator = span.get("locator")
        if not isinstance(locator, str):
            continue
        line_no = _locator_line_number(locator)
        if line_no is not None:
            lines.append(line_no)
    if not lines:
        return None
    return min(lines)


def _rewrite_subtree_nid_prefix(node: Node, old_prefix: str, new_prefix: str) -> None:
    if node.nid == old_prefix:
        node.nid = new_prefix
    elif node.nid.startswith(f"{old_prefix}."):
        node.nid = f"{new_prefix}{node.nid[len(old_prefix):]}"
    for child in node.children:
        _rewrite_subtree_nid_prefix(child, old_prefix, new_prefix)


def _refine_subtrees(
    *,
    root: Node,
    raw_lines: List[str],
    line_no_offset: int,
    input_path: Path,
    doc_id: str,
    parser_profile: Dict[str, Any],
    profiles_dir_override: Optional[Path] = None,
) -> None:
    refine_cfg = (parser_profile.get("postprocess") or {}).get("refine_subtrees") or {}
    if not bool(refine_cfg.get("enabled")):
        return

    refine_kind = str(refine_cfg.get("kind") or "annex")
    refine_key = str(refine_cfg.get("key") or "num")
    dispatch_by_num_raw = refine_cfg.get("dispatch_by_num") or {}
    if not isinstance(dispatch_by_num_raw, dict) or not dispatch_by_num_raw:
        return
    dispatch_by_num = {
        str(k): str(v)
        for k, v in dispatch_by_num_raw.items()
        if isinstance(k, str) and isinstance(v, str) and k and v
    }
    if not dispatch_by_num:
        dispatch_by_num = {}
    fallback_profile_id_raw = refine_cfg.get("fallback_profile_id")
    fallback_profile_id = (
        str(fallback_profile_id_raw).strip()
        if isinstance(fallback_profile_id_raw, str) and fallback_profile_id_raw.strip()
        else None
    )
    keep_unmapped = bool(refine_cfg.get("keep_unmapped", True))

    absolute_last_line = line_no_offset + len(raw_lines)
    target_indexes = [idx for idx, child in enumerate(root.children) if child.kind == refine_kind]
    if not target_indexes:
        return

    from .profile_loader import load_parser_profile

    for pos, idx in enumerate(target_indexes):
        node = root.children[idx]
        dispatch_value_raw = getattr(node, refine_key, None)
        dispatch_value = str(dispatch_value_raw) if dispatch_value_raw is not None else ""
        profile_id = dispatch_by_num.get(dispatch_value)
        if not profile_id:
            if keep_unmapped and fallback_profile_id:
                profile_id = fallback_profile_id
            else:
                continue

        start_line = _node_start_line(node)
        if start_line is None:
            continue

        if pos + 1 < len(target_indexes):
            next_node = root.children[target_indexes[pos + 1]]
            next_start = _node_start_line(next_node)
            end_line = (next_start - 1) if next_start is not None else absolute_last_line
        else:
            end_line = absolute_last_line

        start_idx = max(0, start_line - 1 - line_no_offset)
        end_idx = min(len(raw_lines), end_line - line_no_offset)
        if start_idx >= end_idx:
            continue
        slice_lines = raw_lines[start_idx:end_idx]
        if not slice_lines:
            continue

        sub_profile = load_parser_profile(
            profile_id=profile_id,
            profiles_dir_override=profiles_dir_override,
        )
        sub_doc = parse_text_to_ir(
            input_path=input_path,
            doc_id=f"{doc_id}__refine_{refine_kind}_{dispatch_value}",
            parser_profile=sub_profile,
            lines_override=slice_lines,
            line_no_offset=start_line - 1,
            finalize=False,
            profiles_dir_override=profiles_dir_override,
        )
        sub_root = sub_doc.content
        sub_nodes = [child for child in sub_root.children if child.kind == refine_kind]
        if not sub_nodes:
            continue
        refined = sub_nodes[0]
        if refined.nid != node.nid:
            _rewrite_subtree_nid_prefix(refined, refined.nid, node.nid)

        node.kind_raw = refined.kind_raw
        node.num = refined.num
        node.heading = refined.heading
        node.text = refined.text
        node.role = refined.role
        node.normativity = refined.normativity
        node.source_spans = refined.source_spans
        node.children = refined.children
        if f"refined_by={profile_id}" not in node.tags:
            node.tags.append(f"refined_by={profile_id}")
        if f"refine_kind={refine_kind}" not in node.tags:
            node.tags.append(f"refine_kind={refine_kind}")
        if f"refine_key={dispatch_value}" not in node.tags:
            node.tags.append(f"refine_key={dispatch_value}")


def parse_text_to_ir(
    *,
    input_path: Path,
    doc_id: str,
    parser_profile: Dict[str, Any],
    lines_override: Optional[List[str]] = None,
    line_no_offset: int = 0,
    finalize: bool = True,
    profiles_dir_override: Optional[Path] = None,
) -> IRDocument:
    source_label = parser_profile.get("source_label") or input_path.name
    compiled_markers = _compile_markers(parser_profile)
    structure = parser_profile.get("structure") or {}
    compound = parser_profile.get("compound_prefix") or {}
    structural_kinds = set(
        parser_profile.get("structural_kinds") or ["part", "subpart", "section"]
    )
    structural_kinds.update({"table", "table_header"})
    compound_enabled = bool(compound.get("enabled"))
    max_depth = int(compound.get("max_depth", 1))
    preprocess = parser_profile.get("preprocess") or {}
    drop_line_regexes = [re.compile(p) for p in (preprocess.get("drop_line_regexes") or [])]
    drop_line_exact = {v for v in (preprocess.get("drop_line_exact") or []) if isinstance(v, str) and v}
    strip_inline_regexes = [re.compile(p) for p in (preprocess.get("strip_inline_regexes") or [])]
    use_indent_dedent = bool(preprocess.get("use_indent_dedent"))
    dedent_pop_kinds = set(preprocess.get("dedent_pop_kinds") or [])
    skip_block_rules = _compile_skip_blocks(preprocess)
    repeated_header_cfg = preprocess.get("drop_repeated_structural_headers") or {}
    drop_repeated_structural_headers_enabled = bool(repeated_header_cfg.get("enabled"))
    repeated_header_kinds = {
        str(v).strip().lower()
        for v in (repeated_header_cfg.get("kinds") or [])
        if str(v).strip()
    }
    heading_continuation_cfg = preprocess.get("merge_structural_heading_continuations") or {}
    join_mid_sentence_cfg = preprocess.get("join_mid_sentence_marker_refs_into_prev") or {}
    extract_notes_cfg = preprocess.get("extract_notes") or {}
    extract_notes_enabled = bool(extract_notes_cfg.get("enabled"))
    note_start_regexes = extract_notes_cfg.get("start_regexes") or DEFAULT_NOTE_START_REGEXES
    note_start_patterns = [
        re.compile(p, flags=re.IGNORECASE) for p in note_start_regexes if isinstance(p, str) and p.strip()
    ]
    note_max_lines_raw = extract_notes_cfg.get("max_lines", 50)
    note_max_lines = int(note_max_lines_raw) if str(note_max_lines_raw).strip() else 50
    if note_max_lines <= 0:
        note_max_lines = 50

    root = build_root([])
    stack: List[Node] = [root]
    current = root
    node_indent_by_nid: Dict[str, int] = {root.nid: 0}
    node_factory = _NodeFactory(structural_kinds=structural_kinds)
    parent_last_seen: Dict[str, Dict[str, LastSeen]] = {}
    append_states: Dict[Tuple[str, str], AppendState] = {}
    skip_block_state = SkipBlockState()
    last_attachable_node: Optional[Node] = None

    lines_base = (
        list(lines_override)
        if lines_override is not None
        else input_path.read_text(encoding="utf-8").splitlines()
    )
    raw_lines = list(lines_base)
    lines = list(lines_base)
    lines = _join_mid_sentence_marker_refs_into_prev(
        lines,
        strip_inline_regexes=strip_inline_regexes,
        join_cfg=join_mid_sentence_cfg,
    )
    lines = _merge_structural_marker_heading_lines(
        lines,
        compiled_markers,
        structural_kinds,
        strip_inline_regexes=strip_inline_regexes,
        continuation_cfg=heading_continuation_cfg,
    )
    for idx, raw_line in enumerate(lines):
        line_no = idx + 1 + line_no_offset
        raw_blank = not raw_line.strip()
        cleaned_line = raw_line
        for pat in strip_inline_regexes:
            cleaned_line = pat.sub("", cleaned_line)
        stripped_raw = cleaned_line.strip()
        if skip_block_state.active and skip_block_state.rule_index is not None:
            active_rule = skip_block_rules[skip_block_state.rule_index]
            skip_block_state.seen_lines += 1
            if active_rule.end_pattern.match(stripped_raw):
                skip_block_state.active = False
                skip_block_state.rule_index = None
                skip_block_state.seen_lines = 0
                skip_block_state.start_line = 0
                if not active_rule.include_end:
                    continue
            elif skip_block_state.seen_lines > active_rule.max_lines:
                LOGGER.warning(
                    "skip_blocks end not found within max_lines=%s start_line=%s end_regex=%r",
                    active_rule.max_lines,
                    skip_block_state.start_line,
                    active_rule.end_pattern.pattern,
                )
                skip_block_state.active = False
                skip_block_state.rule_index = None
                skip_block_state.seen_lines = 0
                skip_block_state.start_line = 0
            else:
                continue
        if not skip_block_state.active and skip_block_rules:
            for idx, rule in enumerate(skip_block_rules):
                if not rule.start_pattern.match(stripped_raw):
                    continue
                skip_block_state.active = True
                skip_block_state.rule_index = idx
                skip_block_state.seen_lines = 0
                skip_block_state.start_line = line_no
                if not rule.include_start:
                    continue
                break
            if skip_block_state.active and skip_block_state.rule_index is not None:
                active_rule = skip_block_rules[skip_block_state.rule_index]
                if not active_rule.include_start:
                    continue
        if not stripped_raw:
            if raw_blank and current is not root:
                _mark_pending_break(current, field="text", states=append_states)
            continue
        if drop_repeated_structural_headers_enabled and _should_drop_repeated_structural_header_line(
            stripped_raw,
            stack,
            repeated_header_kinds,
        ):
            continue
        if stripped_raw in drop_line_exact:
            continue
        if any(pat.match(stripped_raw) for pat in drop_line_regexes):
            continue

        table_block = _collect_md_table_block(
            lines,
            idx,
            strip_inline_regexes,
        )
        if table_block is not None:
            parent = current if current is not root else root
            table_node = node_factory.create_node(
                kind="table",
                kind_raw="table",
                num=None,
                line_no=table_block["header_idx"] + 1 + line_no_offset,
                source_label=source_label,
                parent_nid=parent.nid,
            )
            caption = _find_table_caption(lines, table_block["header_idx"], strip_inline_regexes)
            if caption is not None:
                caption_idx, caption_text = caption
                table_node.heading = caption_text
                table_node.source_spans.append(
                    {"source_label": source_label, "locator": f"line:{caption_idx + 1 + line_no_offset}"}
                )
            parent.children.append(table_node)
            node_indent_by_nid[table_node.nid] = _leading_space_count(lines[table_block["header_idx"]])

            header_node = node_factory.create_node(
                kind="table_header",
                kind_raw="table_header",
                num=None,
                line_no=table_block["header_idx"] + 1 + line_no_offset,
                source_label=source_label,
                parent_nid=table_node.nid,
            )
            header_node.text = f"{table_block['header_line']}\n{table_block['separator_line']}"
            header_node.source_spans.append(
                {"source_label": source_label, "locator": f"line:{table_block['separator_idx'] + 1 + line_no_offset}"}
            )
            table_node.children.append(header_node)
            node_indent_by_nid[header_node.nid] = _leading_space_count(lines[table_block["header_idx"]])

            for row_idx, row_text in table_block["rows"]:
                row_node = node_factory.create_node(
                    kind="table_row",
                    kind_raw="table_row",
                    num=None,
                    line_no=row_idx + 1 + line_no_offset,
                    source_label=source_label,
                    parent_nid=header_node.nid,
                )
                row_node.text = row_text
                header_node.children.append(row_node)
                node_indent_by_nid[row_node.nid] = _leading_space_count(lines[row_idx])
                last_attachable_node = row_node

            notes, note_end_idx = _collect_table_notes(
                lines,
                table_block["end_idx"],
                strip_inline_regexes,
                drop_line_regexes,
                drop_line_exact,
                compiled_markers,
            )
            if notes:
                first_note_idx = notes[0][0]
                note_node = node_factory.create_node(
                    kind="note",
                    kind_raw="note",
                    num=None,
                    line_no=first_note_idx + 1 + line_no_offset,
                    source_label=source_label,
                    parent_nid=table_node.nid,
                )
                note_node.text = "\n\n".join(text for _, text in notes)
                for note_idx, _ in notes[1:]:
                    note_node.source_spans.append(
                        {"source_label": source_label, "locator": f"line:{note_idx + 1 + line_no_offset}"}
                    )
                table_node.children.append(note_node)

            lines[table_block["header_idx"]] = ""
            lines[table_block["separator_idx"]] = ""
            for row_idx, _ in table_block["rows"]:
                lines[row_idx] = ""
            for note_idx, _ in notes:
                lines[note_idx] = ""
            continue

        if extract_notes_enabled and note_start_patterns:
            notes_block, _ = _collect_note_block(
                lines,
                idx,
                strip_inline_regexes=strip_inline_regexes,
                drop_line_regexes=drop_line_regexes,
                drop_line_exact=drop_line_exact,
                compiled_markers=compiled_markers,
                start_patterns=note_start_patterns,
                max_lines=note_max_lines,
            )
            if notes_block:
                attach_parent = last_attachable_node or (current if current is not root else root)
                note_node = node_factory.create_node(
                    kind="note",
                    kind_raw="note",
                    num=None,
                    line_no=notes_block[0][0] + 1 + line_no_offset,
                    source_label=source_label,
                    parent_nid=attach_parent.nid,
                )
                note_node.text = "\n\n".join(text for _, text in notes_block)
                for note_idx, _ in notes_block[1:]:
                    note_node.source_spans.append(
                        {"source_label": source_label, "locator": f"line:{note_idx + 1 + line_no_offset}"}
                    )
                attach_parent.children.append(note_node)
                for note_idx, _ in notes_block:
                    lines[note_idx] = ""
                continue

        stripped_for_match = cleaned_line.lstrip()
        current_indent = _leading_space_count(cleaned_line)

        remaining = stripped_for_match
        created_nodes: List[Node] = []
        depth = 0
        while depth < max_depth:
            selected, matched = _select_marker_with_context(
                remaining,
                compiled_markers,
                stack,
                structure,
                parent_last_seen,
                line_no,
            )
            if selected is None:
                if matched:
                    structural_match = next((m for m in matched if m.kind in structural_kinds), None)
                    if structural_match is not None:
                        LOGGER.warning(
                            "orphan structural marker adopted at line=%s kind=%s token=%r -> root",
                            line_no,
                            structural_match.kind,
                            structural_match.raw_token,
                        )
                        parent = root
                        node = node_factory.create_node(
                            kind=structural_match.kind,
                            kind_raw=_resolved_kind_raw(structural_match),
                            num=structural_match.num,
                            line_no=line_no,
                            source_label=source_label,
                            parent_nid=parent.nid,
                        )
                        parent.children.append(node)
                        node_indent_by_nid[node.nid] = current_indent
                        stack = [root, node]
                        current = node
                        created_nodes.append(node)
                        depth += 1
                        remaining = remaining[structural_match.span_end :].lstrip()
                        if not compound_enabled:
                            break
                        continue
                break
            marker_match = selected.marker
            actual_parent_idx = selected.parent_idx
            parent = stack[actual_parent_idx]
            node = node_factory.create_node(
                kind=marker_match.kind,
                kind_raw=_resolved_kind_raw(marker_match),
                num=marker_match.num,
                line_no=line_no,
                source_label=source_label,
                parent_nid=parent.nid,
            )
            parent.children.append(node)
            node_indent_by_nid[node.nid] = current_indent
            parent_state = parent_last_seen.setdefault(parent.nid, {})
            if marker_match.num is not None:
                value = _parse_marker_value(marker_match)
                if value is not None:
                    parent_state[marker_match.marker_id] = LastSeen(
                        value=value,
                        raw=marker_match.num,
                        line_no=line_no,
                        sibling_index=len(parent.children) - 1,
                    )
            stack = stack[: actual_parent_idx + 1] + [node]
            current = node
            created_nodes.append(node)
            if node.kind in {"subitem", "item", "paragraph", "statement", "table_row"}:
                last_attachable_node = node
            depth += 1
            remaining = remaining[marker_match.span_end :].lstrip()
            if not compound_enabled:
                break

        if created_nodes:
            if current.kind in {"note", "history"}:
                _append_text(current, cleaned_line, line_no, source_label, append_states)
            elif current.kind in structural_kinds:
                if remaining:
                    if current.kind == "section":
                        heading, chapeau = _split_section_heading_and_chapeau(remaining)
                    else:
                        heading = _normalize_structural_heading(current.kind, remaining)
                        chapeau = None
                    _append_heading(current, heading, line_no, source_label, append_states)
                    if chapeau:
                        _append_text(current, chapeau, line_no, source_label, append_states)
            elif remaining:
                _append_text(current, remaining, line_no, source_label, append_states)
            continue

        if use_indent_dedent:
            while len(stack) > 1:
                top = stack[-1]
                if top.kind not in dedent_pop_kinds:
                    break
                created_indent = node_indent_by_nid.get(top.nid, 0)
                if current_indent >= created_indent:
                    break
                stack = stack[:-1]
            current = stack[-1]

        if current is root:
            preamble = node_factory.create_node(
                kind="preamble",
                kind_raw=None,
                num=None,
                line_no=line_no,
                source_label=source_label,
                parent_nid=root.nid,
            )
            preamble.role = "informative"
            preamble.normativity = None
            root.children.append(preamble)
            stack = [root, preamble]
            current = preamble
        elif current.kind in {"note", "history"}:
            fallback: Optional[Node] = None
            if len(stack) >= 2 and stack[-1] is current:
                note_parent = stack[-2]
                for sibling in reversed(note_parent.children[:-1]):
                    if sibling.kind not in {"note", "history"}:
                        fallback = sibling
                        break
            if fallback is not None:
                LOGGER.warning(
                    "non-marker line after %s at line=%s attached to previous sibling=%s/%s",
                    current.kind,
                    line_no,
                    fallback.kind,
                    fallback.nid,
                )
                stack = stack[:-1] + [fallback]
                current = fallback
            else:
                fallback_idx = _find_latest_non_note_stack_index(stack)
                if fallback_idx is not None:
                    fallback = stack[fallback_idx]
                    LOGGER.warning(
                        "non-marker line after %s at line=%s attached to previous non-note node=%s/%s",
                        current.kind,
                        line_no,
                        fallback.kind,
                        fallback.nid,
                    )
                    stack = stack[: fallback_idx + 1]
                    current = fallback
        _append_text(current, cleaned_line, line_no, source_label, append_states)

    if finalize:
        _refine_subtrees(
            root=root,
            raw_lines=raw_lines,
            line_no_offset=line_no_offset,
            input_path=input_path,
            doc_id=doc_id,
            parser_profile=parser_profile,
            profiles_dir_override=profiles_dir_override,
        )
        _nest_root_chapters_under_parts(root)
        _quality_warnings = run_text_postprocess_and_qualitycheck(root)
        for warning in _quality_warnings:
            LOGGER.warning("qualitycheck: %s", warning)
        assign_document_order(root)
        index = {"display_name_by_nid": {}}
        _collect_display_names(root, index["display_name_by_nid"])
    else:
        index = {"display_name_by_nid": {}}
    return IRDocument(doc_id=doc_id, content=root, index=index)
