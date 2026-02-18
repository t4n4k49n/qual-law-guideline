from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from qai_text2ir.cli import _build_regdoc_profile
from qai_text2ir.context_display import resolve_context_nodes
from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _profile() -> Dict[str, object]:
    return {
        "schema": "qai.parser_profile.v1",
        "id": "normal_note_test_profile",
        "language": "en",
        "source_label": "test",
        "context_root_kind": "section",
        "structural_kinds": ["section"],
        "marker_types": [
            {
                "id": "section",
                "kind": "section",
                "kind_raw": "Section",
                "match": r"^Section\s+(?P<n>\d+)\.\s+(?P<title>.+)$",
                "num_group": "n",
            },
            {
                "id": "paragraph_decimal",
                "kind": "paragraph",
                "kind_raw": "1.1",
                "match": r"^(?P<n>\d+\.\d+)\s+",
                "num_group": "n",
            },
            {
                "id": "item_paren_alpha",
                "kind": "item",
                "kind_raw": "(a)",
                "match": r"^\((?P<n>[a-z])\)\s+",
                "num_group": "n",
            },
        ],
        "preprocess": {
            "extract_notes": {
                "enabled": True,
                "start_regexes": [
                    r"^(?:Note|Notes|NB)\b[:：]?\s*",
                    r"^(注|注記|備考|※)\s*[:：]?\s*",
                    r"^（注）\s*",
                ],
                "max_lines": 50,
            }
        },
        "structure": {
            "root": {"children": ["section"]},
            "section": {"children": ["paragraph", "item", "subitem", "note", "history"]},
            "paragraph": {"children": ["item", "subitem", "note", "history"]},
            "item": {"children": ["subitem", "note", "history"]},
            "subitem": {"children": ["note", "history"]},
            "note": {"children": []},
            "history": {"children": []},
        },
    }


def test_normal_note_block_attaches_to_previous_node() -> None:
    input_path = Path("tests/fixtures/normal_note_sample.txt")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="normal_note_sample",
        parser_profile=_profile(),
    )
    ir = ir_doc.to_dict()
    nodes = _flatten(ir["content"])

    paragraph = next(n for n in nodes if n.get("kind") == "paragraph" and n.get("num") == "1.1")
    item = next(n for n in nodes if n.get("kind") == "item" and n.get("num") == "a")

    p_notes = [n for n in paragraph.get("children", []) if n.get("kind") == "note"]
    i_notes = [n for n in item.get("children", []) if n.get("kind") == "note"]

    assert len(p_notes) == 1
    assert "This is a note." in (p_notes[0].get("text") or "")
    assert len(i_notes) == 1
    assert "備考：これは備考。" in (i_notes[0].get("text") or "")


def test_context_resolution_for_item_includes_its_note_only() -> None:
    input_path = Path("tests/fixtures/normal_note_sample.txt")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="normal_note_context",
        parser_profile=_profile(),
    )

    root = ir_doc.content
    item_node = None
    paragraph_node = None

    def _visit(node) -> None:
        nonlocal item_node, paragraph_node
        if node.kind == "item" and node.num == "a":
            item_node = node
        if node.kind == "paragraph" and node.num == "1.1":
            paragraph_node = node
        for child in node.children:
            _visit(child)

    _visit(root)
    assert item_node is not None
    assert paragraph_node is not None

    regdoc_profile = _build_regdoc_profile("normal_note_sample", context_root_kind="section")
    purpose = regdoc_profile["profiles"]["dq_gmp_checklist"]
    resolved = resolve_context_nodes(root, item_node.nid, purpose)
    resolved_nids = {n.nid for n in resolved}
    resolved_note_texts = [(n.text or "") for n in resolved if n.kind == "note"]

    assert item_node.nid in resolved_nids
    assert any("備考：これは備考。" in text for text in resolved_note_texts)
    assert not any("This is a note." in text for text in resolved_note_texts)
