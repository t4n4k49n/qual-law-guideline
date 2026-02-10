from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from qai_xml2ir.models_ir import IRDocument, Node, build_root
from qai_xml2ir.nid import NidBuilder
from qai_xml2ir.ord_key import assign_document_order


@dataclass
class MarkerMatch:
    kind: str
    kind_raw: Optional[str]
    num: Optional[str]
    span_end: int


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


def _select_marker_with_context(
    text: str,
    compiled_markers: List[Tuple[Dict[str, Any], re.Pattern[str]]],
    stack: List[Node],
    structure: Dict[str, Any],
) -> Tuple[Optional[MarkerMatch], Optional[int]]:
    best: Optional[Tuple[int, int, MarkerMatch]] = None
    for order, (marker, pattern) in enumerate(compiled_markers):
        m = pattern.match(text)
        if not m:
            continue
        kind = marker["kind"]
        parent_idx = _find_parent_candidate(stack, kind, structure)
        parent_rank = parent_idx if parent_idx is not None else -1
        if parent_idx is None:
            parent_idx = None
        candidate = (
            parent_rank,
            -order,
            MarkerMatch(
                kind=kind,
                kind_raw=marker.get("kind_raw"),
                num=_extract_num(marker, m),
                span_end=m.end(),
            ),
        )
        if best is None or candidate > best:
            best = candidate
    if best is None:
        return None, None
    return best[2], best[0]


def _append_text(node: Node, line: str, line_no: int, source_label: str) -> None:
    if not line:
        return
    if node.text:
        node.text = f"{node.text}\n{line}"
    else:
        node.text = line
    node.source_spans.append({"source_label": source_label, "locator": f"line:{line_no}"})


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

    lines = input_path.read_text(encoding="utf-8").splitlines()
    for line_no, raw_line in enumerate(lines, start=1):
        stripped_for_match = raw_line.lstrip()
        if not stripped_for_match:
            continue

        remaining = stripped_for_match
        created_nodes: List[Node] = []
        depth = 0
        while depth < max_depth:
            marker_match, parent_idx = _select_marker_with_context(
                remaining,
                compiled_markers,
                stack,
                structure,
            )
            if marker_match is None:
                break
            actual_parent_idx = 0 if parent_idx is None else parent_idx
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
            stack = stack[: actual_parent_idx + 1] + [node]
            current = node
            created_nodes.append(node)
            depth += 1
            remaining = remaining[marker_match.span_end :].lstrip()
            if not compound_enabled:
                break

        if created_nodes:
            if current.kind in structural_kinds:
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
        _append_text(current, stripped_for_match, line_no, source_label)

    assign_document_order(root)
    index = {"display_name_by_nid": {}}
    _collect_display_names(root, index["display_name_by_nid"])
    return IRDocument(doc_id=doc_id, content=root, index=index)
