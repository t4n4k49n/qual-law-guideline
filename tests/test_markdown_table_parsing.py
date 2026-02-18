from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from qai_text2ir.cli import _build_regdoc_profile
from qai_text2ir.context_display import resolve_context_nodes
from qai_text2ir.text_parser import parse_text_to_ir
from qai_xml2ir.verify import verify_document


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _profile() -> Dict[str, object]:
    return {
        "schema": "qai.parser_profile.v1",
        "id": "markdown_table_test_profile",
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
            }
        ],
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


def test_markdown_table_block_is_structured() -> None:
    input_path = Path("tests/fixtures/markdown_table_sample.txt")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="markdown_table_sample",
        parser_profile=_profile(),
    )
    ir = ir_doc.to_dict()
    verify_document(ir)

    root = ir["content"]
    nodes = _flatten(root)
    table = next(n for n in nodes if n.get("kind") == "table")
    assert "Table 1: Example" in (table.get("heading") or "")

    header = next(n for n in table.get("children", []) if n.get("kind") == "table_header")
    header_text = header.get("text") or ""
    assert "| Item | Requirement |" in header_text
    assert "| --- | --- |" in header_text

    rows = [n for n in header.get("children", []) if n.get("kind") == "table_row"]
    assert len(rows) == 2
    assert rows[0].get("text") == "| A | Do A |"
    assert rows[1].get("text") == "| B | Do B |"

    notes = [n for n in table.get("children", []) if n.get("kind") == "note"]
    assert len(notes) == 1
    assert "Applies to all items." in (notes[0].get("text") or "")


def test_context_resolution_for_table_row_includes_header_and_note() -> None:
    input_path = Path("tests/fixtures/markdown_table_sample.txt")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="markdown_table_sample_context",
        parser_profile=_profile(),
    )

    root = ir_doc.content
    rows: List = []

    def _visit(node) -> None:
        if node.kind == "table_row":
            rows.append(node)
        for child in node.children:
            _visit(child)

    _visit(root)
    assert len(rows) == 2
    selected_row = rows[0]
    sibling_row = rows[1]

    regdoc_profile = _build_regdoc_profile("markdown_table_sample", context_root_kind="section")
    purpose = regdoc_profile["profiles"]["dq_gmp_checklist"]
    resolved = resolve_context_nodes(root, selected_row.nid, purpose)
    resolved_kinds = [n.kind for n in resolved]
    resolved_nids = {n.nid for n in resolved}

    assert "table" in resolved_kinds
    assert "table_header" in resolved_kinds
    assert "note" in resolved_kinds
    assert selected_row.nid in resolved_nids
    assert sibling_row.nid not in resolved_nids


def test_markdown_table_real_excerpt_with_japanese_notes() -> None:
    input_path = Path("tests/fixtures/markdown_table_real_excerpt.md")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="markdown_table_real_excerpt",
        parser_profile=_profile(),
    )
    ir = ir_doc.to_dict()
    verify_document(ir)

    root = ir["content"]
    nodes = _flatten(root)
    table = next(n for n in nodes if n.get("kind") == "table")
    assert "表１ 清浄区域の分類" in (table.get("heading") or "")

    header = next(n for n in table.get("children", []) if n.get("kind") == "table_header")
    rows = [n for n in header.get("children", []) if n.get("kind") == "table_row"]
    assert len(rows) >= 5

    notes = [n for n in table.get("children", []) if n.get("kind") == "note"]
    assert len(notes) == 1
    note_text = notes[0].get("text") or ""
    assert "注 1）" in note_text
    assert "注 2）" in note_text
