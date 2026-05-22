from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class Node:
    nid: str
    kind: str
    num: Optional[str]
    ord: float
    heading: Optional[str]
    text: Optional[str]
    kind_raw: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    visibility: Dict[str, Any] = field(default_factory=dict)
    children: List["Node"] = field(default_factory=list)
    parent_nid: Optional[str] = None


@dataclass
class DocIndex:
    root: Node
    by_nid: Dict[str, Node]
    display_name_by_nid: Dict[str, str]

    def ancestors_of(self, nid: str) -> List[Node]:
        node = self.by_nid.get(nid)
        if node is None:
            return []
        out: List[Node] = []
        while node.parent_nid:
            parent = self.by_nid.get(node.parent_nid)
            if parent is None:
                break
            out.append(parent)
            node = parent
        out.reverse()
        return out

    def descendants_of(
        self,
        nid: str,
        *,
        max_depth: int = 8,
        include_kinds: Optional[Iterable[str]] = None,
    ) -> List[Node]:
        base = self.by_nid.get(nid)
        if base is None or max_depth <= 0:
            return []
        allowed = set(include_kinds) if include_kinds is not None else None
        out: List[Node] = []
        stack: List[tuple[Node, int]] = [(base, 0)]
        while stack:
            node, depth = stack.pop()
            if depth >= max_depth:
                continue
            for child in reversed(node.children):
                next_depth = depth + 1
                if allowed is None or child.kind in allowed:
                    out.append(child)
                stack.append((child, next_depth))
        out.sort(key=lambda n: (n.ord, n.nid))
        return out

    def path_labels(self, nid: str) -> List[str]:
        labels: List[str] = []
        for node in self.ancestors_of(nid):
            if node.kind == "document":
                continue
            label = self.display_name_by_nid.get(node.nid) or node.heading or node.text or node.nid
            labels.append(_single_line(label))
        node = self.by_nid.get(nid)
        if node is not None:
            own = self.display_name_by_nid.get(node.nid) or node.heading or node.nid
            labels.append(_single_line(own))
        return [label for label in labels if label]


def _single_line(text: str) -> str:
    return " ".join(text.strip().split())


def _to_node(raw: Dict[str, Any], *, parent_nid: Optional[str], by_nid: Dict[str, Node]) -> Node:
    nid = str(raw.get("nid") or "")
    kind = str(raw.get("kind") or "")
    ord_raw = raw.get("ord")
    ord_value: float
    if isinstance(ord_raw, (int, float)):
        ord_value = float(ord_raw)
    else:
        ord_value = 0.0
    node = Node(
        nid=nid,
        kind=kind,
        kind_raw=(str(raw.get("kind_raw")) if raw.get("kind_raw") is not None else None),
        num=(str(raw.get("num")) if raw.get("num") is not None else None),
        ord=ord_value,
        heading=raw.get("heading"),
        text=raw.get("text"),
        tags=[str(tag) for tag in (raw.get("tags") or [])],
        data=raw.get("data") if isinstance(raw.get("data"), dict) else {},
        visibility=raw.get("visibility") if isinstance(raw.get("visibility"), dict) else {},
        children=[],
        parent_nid=parent_nid,
    )
    by_nid[nid] = node
    for child_raw in raw.get("children") or []:
        child = _to_node(child_raw, parent_nid=nid, by_nid=by_nid)
        node.children.append(child)
    return node


def build_doc_index(regdoc_ir: Dict[str, Any]) -> DocIndex:
    content = regdoc_ir.get("content")
    if not isinstance(content, dict):
        raise ValueError("regdoc_ir.content が見つからないか、形式が不正です。")
    by_nid: Dict[str, Node] = {}
    root = _to_node(content, parent_nid=None, by_nid=by_nid)
    raw_display = regdoc_ir.get("index", {}).get("display_name_by_nid", {})
    display = {str(k): str(v) for k, v in raw_display.items()} if isinstance(raw_display, dict) else {}
    return DocIndex(root=root, by_nid=by_nid, display_name_by_nid=display)
