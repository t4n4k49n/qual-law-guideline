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


def _profile(*, detect_plaintext_tables: bool = False) -> Dict[str, object]:
    preprocess: Dict[str, object] = {
        "extract_notes": {
            "enabled": True,
            "start_regexes": [r"^Note\s+\d+:"],
            "max_lines": 5,
        }
    }
    if detect_plaintext_tables:
        preprocess["detect_plaintext_tables"] = {
            "enabled": True,
            "min_rows": 3,
            "max_rows": 12,
        }
    return {
        "schema": "qai.parser_profile.v1",
        "id": "pics_annex1_real_table_test_profile",
        "language": "en",
        "source_label": "pics_annex1_excerpt",
        "context_root_kind": "section",
        "structural_kinds": ["section"],
        "preprocess": preprocess,
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
            "section": {"children": ["paragraph", "item", "subitem", "note", "history", "table", "preformatted"]},
            "paragraph": {"children": ["item", "subitem", "note", "history"]},
            "item": {"children": ["subitem", "note", "history"]},
            "subitem": {"children": ["note", "history"]},
            "table": {"children": ["table_header", "note"]},
            "table_header": {"children": ["table_row"]},
            "table_row": {"children": []},
            "note": {"children": []},
            "preformatted": {"children": []},
            "history": {"children": []},
        },
    }


def test_pics_annex1_markdown_table_excerpt_structures_table_note_and_payload() -> None:
    ir_doc = parse_text_to_ir(
        input_path=Path("tests/fixtures/text2ir/pics_annex1_table2_markdown_excerpt.txt"),
        doc_id="pics_annex1_table2_markdown_excerpt",
        parser_profile=_profile(),
    )
    ir = ir_doc.to_dict()
    verify_document(ir)

    nodes = _flatten(ir["content"])
    table = next(n for n in nodes if n.get("kind") == "table")
    assert "Table 2" in (table.get("heading") or "")
    assert table.get("data", {}).get("format") == "markdown"

    header = next(n for n in table.get("children", []) if n.get("kind") == "table_header")
    assert header.get("data", {}).get("columns") == [
        "Grade",
        "Air sample cfu/m3",
        "Settle plates cfu/4 hours",
        "Contact plates cfu/plate",
    ]
    rows = [n for n in header.get("children", []) if n.get("kind") == "table_row"]
    assert len(rows) == 4
    assert rows[0].get("data", {}).get("cells") == ["A", "< 1", "< 1", "< 1"]
    assert rows[0].get("source_spans")

    notes = [n for n in table.get("children", []) if n.get("kind") == "note"]
    assert len(notes) == 1
    assert notes[0].get("data", {}).get("note_type") == "table_note"
    assert "Note 1:" in (notes[0].get("text") or "")
    assert "Note 2:" in (notes[0].get("text") or "")


def test_pics_annex1_table_row_context_includes_header_and_table_note() -> None:
    ir_doc = parse_text_to_ir(
        input_path=Path("tests/fixtures/text2ir/pics_annex1_table2_markdown_excerpt.txt"),
        doc_id="pics_annex1_table2_markdown_context",
        parser_profile=_profile(),
    )
    rows = []

    def visit(node) -> None:
        if node.kind == "table_row":
            rows.append(node)
        for child in node.children:
            visit(child)

    visit(ir_doc.content)
    assert rows

    regdoc_profile = _build_regdoc_profile("pics_annex1_table2_markdown_context", context_root_kind="section")
    purpose = regdoc_profile["profiles"]["dq_gmp_checklist"]
    resolved = resolve_context_nodes(ir_doc.content, rows[0].nid, purpose)
    resolved_kinds = {node.kind for node in resolved}
    assert "table" in resolved_kinds
    assert "table_header" in resolved_kinds
    assert "note" in resolved_kinds


def test_pics_annex1_plaintext_table_excerpt_is_not_silently_flattened() -> None:
    ir_doc = parse_text_to_ir(
        input_path=Path("tests/fixtures/text2ir/pics_annex1_table2_plaintext_excerpt.txt"),
        doc_id="pics_annex1_table2_plaintext_excerpt",
        parser_profile=_profile(detect_plaintext_tables=True),
    )
    ir = ir_doc.to_dict()
    verify_document(ir)

    nodes = _flatten(ir["content"])
    possible_table = next(n for n in nodes if "possible_plaintext_table_not_structured" in (n.get("tags") or []))
    assert possible_table.get("kind") == "preformatted"
    assert possible_table.get("kind_raw") == "possible_table"
    assert "Table 2" in (possible_table.get("heading") or "")
    assert possible_table.get("source_spans")
    assert possible_table.get("data", {}).get("warning") == "possible_plaintext_table_not_structured"
