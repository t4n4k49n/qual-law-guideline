from __future__ import annotations

import logging
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from qai_xml2ir.models_ir import IRDocument, Node, build_root
from qai_xml2ir.nid import NidBuilder
from qai_xml2ir.ord_key import assign_document_order

LOGGER = logging.getLogger(__name__)

GAP_WARN_MAX_BY_FAMILY = {
    "alpha": 2,
    "roman": 3,
    "digit": 2,
}


@dataclass
class MarkerMatch:
    marker_id: str
    kind: str
    kind_raw: Optional[str]
    num: Optional[str]
    span_end: int
    order: int


@dataclass
class LastSeen:
    value: int
    raw: str
    line_no: int
    sibling_index: int


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


def _append_text(node: Node, line: str, line_no: int, source_label: str) -> None:
    if not line:
        return
    if node.text:
        node.text = f"{node.text}\n{line}"
    else:
        node.text = line
    node.source_spans.append({"source_label": source_label, "locator": f"line:{line_no}"})


def _find_latest_non_note_stack_index(stack: List[Node]) -> Optional[int]:
    for idx in range(len(stack) - 1, -1, -1):
        kind = stack[idx].kind
        if kind in {"document", "note", "history"}:
            continue
        return idx
    return None


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
    source_label = input_path.name
    compiled_markers = _compile_markers(parser_profile)
    structure = parser_profile.get("structure") or {}
    compound = parser_profile.get("compound_prefix") or {}
    structural_kinds = set(
        parser_profile.get("structural_kinds") or ["part", "subpart", "section"]
    )
    compound_enabled = bool(compound.get("enabled"))
    max_depth = int(compound.get("max_depth", 1))

    root = build_root([])
    stack: List[Node] = [root]
    current = root
    node_factory = _NodeFactory(structural_kinds=structural_kinds)
    parent_last_seen: Dict[str, Dict[str, LastSeen]] = {}

    lines = input_path.read_text(encoding="utf-8").splitlines()
    for line_no, raw_line in enumerate(lines, start=1):
        stripped_for_match = raw_line.lstrip()
        if not stripped_for_match:
            continue

        remaining = stripped_for_match
        created_nodes: List[Node] = []
        depth = 0
        while depth < max_depth:
            selected, _matched = _select_marker_with_context(
                remaining,
                compiled_markers,
                stack,
                structure,
                parent_last_seen,
                line_no,
            )
            if selected is None:
                break
            marker_match = selected.marker
            actual_parent_idx = selected.parent_idx
            parent = stack[actual_parent_idx]
            node = node_factory.create_node(
                kind=marker_match.kind,
                kind_raw=marker_match.kind_raw,
                num=marker_match.num,
                line_no=line_no,
                source_label=source_label,
                parent_nid=parent.nid,
            )
            parent.children.append(node)
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
                _append_text(current, stripped_for_match, line_no, source_label)
            elif current.kind in structural_kinds:
                if remaining:
                    if current.heading is None:
                        current.heading = remaining
                    else:
                        _append_text(current, remaining, line_no, source_label)
            elif remaining:
                _append_text(current, remaining, line_no, source_label)
            continue

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
        _append_text(current, stripped_for_match, line_no, source_label)

    assign_document_order(root)
    index = {"display_name_by_nid": {}}
    _collect_display_names(root, index["display_name_by_nid"])
    return IRDocument(doc_id=doc_id, content=root, index=index)
