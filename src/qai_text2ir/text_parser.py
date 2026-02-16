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
KEEP_HYPHEN_ALLOWLIST = {
    "time-stamped",
    "time-sequenced",
    "computer-generated",
    "system-based",
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
) -> Optional[int]:
    for marker, pattern in compiled_markers:
        if marker.get("kind") not in structural_kinds:
            continue
        matched = pattern.match(text)
        if matched:
            return matched.end()
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


def _merge_structural_marker_heading_lines(
    lines: List[str],
    compiled_markers: List[Tuple[Dict[str, Any], re.Pattern[str]]],
    structural_kinds: Set[str],
) -> List[str]:
    # Keep line count stable: merged next line is replaced with an empty line.
    merged = list(lines)
    idx = 0
    while idx < len(merged) - 1:
        current = merged[idx]
        if not current.strip():
            idx += 1
            continue
        current_stripped = current.lstrip()
        marker_end = _find_structural_marker_end(
            current_stripped,
            compiled_markers,
            structural_kinds,
        )
        if marker_end is None:
            idx += 1
            continue
        if current_stripped[marker_end:].strip():
            idx += 1
            continue
        next_line = merged[idx + 1]
        next_stripped = next_line.strip()
        if not next_stripped:
            idx += 1
            continue
        if _starts_with_any_marker(next_line.lstrip(), compiled_markers):
            idx += 1
            continue
        if not _looks_like_heading_line(next_stripped):
            idx += 1
            continue
        merged[idx] = f"{current.rstrip()} {next_stripped}"
        merged[idx + 1] = ""
        idx += 2
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
                "\n\n".join(processed),
            )
        for child in node.children:
            _visit(child)

    _visit(root)


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


def _collect_display_names(node: Node, table: Dict[str, str]) -> None:
    table[node.nid] = _build_display_name(node)
    for child in node.children:
        _collect_display_names(child, table)


def parse_text_to_ir(
    *,
    input_path: Path,
    doc_id: str,
    parser_profile: Dict[str, Any],
) -> IRDocument:
    source_label = parser_profile.get("source_label") or input_path.name
    compiled_markers = _compile_markers(parser_profile)
    structure = parser_profile.get("structure") or {}
    compound = parser_profile.get("compound_prefix") or {}
    structural_kinds = set(
        parser_profile.get("structural_kinds") or ["part", "subpart", "section"]
    )
    compound_enabled = bool(compound.get("enabled"))
    max_depth = int(compound.get("max_depth", 1))
    preprocess = parser_profile.get("preprocess") or {}
    drop_line_regexes = [re.compile(p) for p in (preprocess.get("drop_line_regexes") or [])]
    drop_line_exact = {v for v in (preprocess.get("drop_line_exact") or []) if isinstance(v, str) and v}
    use_indent_dedent = bool(preprocess.get("use_indent_dedent"))
    dedent_pop_kinds = set(preprocess.get("dedent_pop_kinds") or [])

    root = build_root([])
    stack: List[Node] = [root]
    current = root
    node_indent_by_nid: Dict[str, int] = {root.nid: 0}
    node_factory = _NodeFactory(structural_kinds=structural_kinds)
    parent_last_seen: Dict[str, Dict[str, LastSeen]] = {}
    append_states: Dict[Tuple[str, str], AppendState] = {}

    lines = input_path.read_text(encoding="utf-8").splitlines()
    lines = _merge_structural_marker_heading_lines(lines, compiled_markers, structural_kinds)
    for line_no, raw_line in enumerate(lines, start=1):
        stripped_raw = raw_line.strip()
        if stripped_raw in drop_line_exact:
            continue
        if any(pat.match(stripped_raw) for pat in drop_line_regexes):
            continue
        if not raw_line.strip():
            if current is not root:
                _mark_pending_break(current, field="text", states=append_states)
            continue
        stripped_for_match = raw_line.lstrip()
        current_indent = _leading_space_count(raw_line)

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
            depth += 1
            remaining = remaining[marker_match.span_end :].lstrip()
            if not compound_enabled:
                break

        if created_nodes:
            if current.kind in {"note", "history"}:
                _append_text(current, raw_line, line_no, source_label, append_states)
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
        _append_text(current, raw_line, line_no, source_label, append_states)

    _quality_warnings = run_text_postprocess_and_qualitycheck(root)
    for warning in _quality_warnings:
        LOGGER.warning("qualitycheck: %s", warning)
    assign_document_order(root)
    index = {"display_name_by_nid": {}}
    _collect_display_names(root, index["display_name_by_nid"])
    return IRDocument(doc_id=doc_id, content=root, index=index)
