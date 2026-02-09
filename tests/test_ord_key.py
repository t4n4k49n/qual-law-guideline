from __future__ import annotations

from qai_xml2ir.models_ir import Node
from qai_xml2ir.ord_key import assign_document_order, normalize_num_attr


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


def test_assign_document_order_preorder_sequence() -> None:
    root = _node(
        "root",
        [
            _node("a", [_node("a1"), _node("a2")]),
            _node("b", [_node("b1")]),
        ],
    )
    assigned = assign_document_order(root)
    nodes = [n for n in _walk(root) if n.nid != "root"]
    ords = [n.ord for n in nodes]

    assert assigned == 5
    assert root.ord is None
    assert ords == [1, 2, 3, 4, 5]


def test_normalize_num_attr_preserves_underscore_and_maps_colon() -> None:
    assert normalize_num_attr("15:16") == "15__16"
    assert normalize_num_attr("1516") == "1516"
    assert normalize_num_attr("15_16") == "15_16"
