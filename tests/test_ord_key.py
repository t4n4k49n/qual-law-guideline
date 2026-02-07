from __future__ import annotations

from qai_xml2ir.models_ir import Node
from qai_xml2ir.ord_key import ORD_WIDTH, assign_document_order


def _node(nid: str, children: list[Node] | None = None) -> Node:
    return Node(
        nid=nid,
        kind="x",
        kind_raw=None,
        num=None,
        ord=None,
        heading=None,
        text=None,
        role="structural",
        normativity=None,
        children=children or [],
    )


def _walk(node: Node) -> list[Node]:
    out = [node]
    for c in node.children:
        out.extend(_walk(c))
    return out


def test_assign_document_order_preorder() -> None:
    root = _node(
        "root",
        [
            _node("a", [_node("a1"), _node("a2")]),
            _node("b", [_node("b1")]),
        ],
    )
    count = assign_document_order(root)
    nodes = _walk(root)
    ords = [n.ord for n in nodes if n.nid != "root"]

    assert count == 5
    assert root.ord is None
    assert len(set(ords)) == len(ords)
    assert all(len(o or "") == ORD_WIDTH for o in ords)
    assert ords == sorted(ords)
    assert ords == ["00000001", "00000002", "00000003", "00000004", "00000005"]
