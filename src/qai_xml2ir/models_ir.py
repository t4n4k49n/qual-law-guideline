from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Node:
    nid: str
    kind: str
    kind_raw: Optional[str]
    num: Optional[str]
    ord: Optional[str]
    heading: Optional[str]
    text: Optional[str]
    role: str
    normativity: Optional[str]
    tags: List[str] = field(default_factory=list)
    refs: Dict[str, Any] = field(
        default_factory=lambda: {"internal": [], "external": []}
    )
    source_spans: List[Dict[str, Optional[str]]] = field(default_factory=list)
    children: List["Node"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nid": self.nid,
            "kind": self.kind,
            "kind_raw": self.kind_raw,
            "num": self.num,
            "ord": self.ord,
            "heading": self.heading,
            "text": self.text,
            "role": self.role,
            "normativity": self.normativity,
            "tags": list(self.tags),
            "refs": self.refs,
            "source_spans": list(self.source_spans),
            "children": [c.to_dict() for c in self.children],
        }


@dataclass
class IRDocument:
    doc_id: str
    content: Node
    index: Dict[str, Any] = field(default_factory=dict)
    schema: str = "qai.regdoc_ir.v2"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema": self.schema,
            "doc_id": self.doc_id,
            "content": self.content.to_dict(),
            "index": self.index,
        }


def build_root(children: List[Node]) -> Node:
    return Node(
        nid="root",
        kind="document",
        kind_raw=None,
        num=None,
        ord=None,
        heading=None,
        text=None,
        role="structural",
        normativity=None,
        children=children,
    )
