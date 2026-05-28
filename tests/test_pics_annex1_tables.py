from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from qai_text2ir.goal_check import check_bundle
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


SOURCE = Path("data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt")
PROFILE = Path("src/qai_text2ir/profiles/pics_annex1_default_v2.yaml")


def _flatten(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = [node]
    for child in node.get("children", []) or []:
        out.extend(_flatten(child))
    return out


def _ir() -> Dict[str, Any]:
    profile = load_parser_profile(path=PROFILE)
    return parse_text_to_ir(
        input_path=SOURCE,
        doc_id="pics_annex1_tables_test",
        parser_profile=profile,
    ).to_dict()


def _tables(ir: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    tables = [node for node in _flatten(ir["content"]) if node.get("kind") == "table"]
    return {str((node.get("data") or {}).get("table_no")): node for node in tables if (node.get("data") or {}).get("parser") == "pics_annex1_tables"}


def _rows(table: Dict[str, Any]) -> List[Dict[str, Any]]:
    header = next(child for child in table.get("children", []) if child.get("kind") == "table_header")
    return [child for child in header.get("children", []) if child.get("kind") == "table_row"]


def test_annex1_table_1_grade_a_to_d_are_structured() -> None:
    table = _tables(_ir())["1"]
    rows = _rows(table)
    header = table["children"][0]
    columns = header["data"]["columns"]

    assert table["data"]["cell_reconstruction_status"] == "complete"
    assert table["data"]["header_groups"][0]["columns"] == [1, 2]
    assert columns == [
        "Grade",
        "Maximum limits for total particle >= 0.5 µm/m3 at rest",
        "Maximum limits for total particle >= 0.5 µm/m3 in operation",
        "Maximum limits for total particle >= 5 µm/m3 at rest",
        "Maximum limits for total particle >= 5 µm/m3 in operation",
    ]
    assert header["text"] == " | ".join(columns)
    assert [row["data"]["grade"] for row in rows] == ["A", "B", "C", "D"]
    assert rows[0]["data"]["cells"] == ["A", "3 520", "3 520", "Not specified (a)", "Not specified (a)"]
    assert rows[3]["data"]["cells"][2] == "Not predetermined (b)"
    assert rows[3]["data"]["wrapped_cells"] == [2, 4]
    assert len(set(columns)) == len(columns)


def test_annex1_table_2_grade_a_to_d_and_notes_are_structured() -> None:
    table = _tables(_ir())["2"]
    rows = _rows(table)
    notes = [child for child in table.get("children", []) if child.get("kind") == "note"]
    note_text = "\n".join(note.get("text") or "" for note in notes)

    assert [row["data"]["grade"] for row in rows] == ["A", "B", "C", "D"]
    assert rows[0]["data"]["cells"] == ["A", "No growth", "No growth", "No growth"]
    assert rows[0]["data"]["expanded_merged_cells"] == [1, 2, 3]
    assert table["data"]["merged_cells"][0]["type"] == "column_span"
    assert "Note 1:" in note_text
    assert "Note 2:" in note_text
    assert "Note 3:" in note_text
    assert "Note 4:" in note_text


def test_annex1_table_3_grade_operations_are_structured() -> None:
    table = _tables(_ir())["3"]
    rows = _rows(table)

    assert [row["data"]["grade"] for row in rows] == ["A", "C", "C", "D"]
    assert "Filling of products" in rows[0]["data"]["operations"][0]
    assert rows[1]["data"]["rowspan_group"] == "Grade C"
    assert rows[2]["data"]["rowspan_group"] == "Grade C"
    assert "subsequent filling" in rows[-1]["data"]["operations"][0]


def test_annex1_table_4_grade_operations_are_structured() -> None:
    table = _tables(_ir())["4"]
    rows = _rows(table)
    grades = [row["data"]["grade"] for row in rows]

    assert grades == ["A"] * 8 + ["B"] * 2 + ["C"] + ["D"] * 4
    assert rows[8]["data"]["operations"][0] == "Background support for grade A (when not in an isolator)."
    assert rows[8]["data"]["rowspan_group"] == "Grade B"
    assert rows[11]["data"]["operations"][0] == "Cleaning of equipment."
    assert rows[11]["data"]["rowspan_group"] == "Grade D"
    assert any("lyophilizer" in row["data"]["operations"][0] for row in rows)


def test_annex1_table_5_grade_a_to_d_are_structured() -> None:
    table = _tables(_ir())["5"]
    rows = _rows(table)
    header = table["children"][0]
    columns = header["data"]["columns"]

    assert columns == [
        "Grade",
        "Maximum limits for total particle >= 0.5 μm/m3 at rest",
        "Maximum limits for total particle >= 0.5 μm/m3 in operation",
        "Maximum limits for total particle >= 5 μm/m3 at rest",
        "Maximum limits for total particle >= 5 μm/m3 in operation",
    ]
    assert header["text"] == " | ".join(columns)
    assert [row["data"]["grade"] for row in rows] == ["A", "B", "C", "D"]
    assert rows[0]["data"]["cells"] == ["A", "3 520", "3 520", "29", "29"]
    assert rows[3]["data"]["cells"][2] == "Not predetermined (a)"
    assert rows[3]["data"]["wrapped_cells"] == [2, 4]
    assert len(set(columns)) == len(columns)


def test_annex1_table_6_grade_a_to_d_and_notes_are_structured() -> None:
    table = _tables(_ir())["6"]
    rows = _rows(table)
    notes = [child for child in table.get("children", []) if child.get("kind") == "note"]
    note_text = "\n".join(note.get("text") or "" for note in notes)

    assert [row["data"]["grade"] for row in rows] == ["A", "B", "C", "D"]
    assert rows[0]["data"]["cells"][1:] == ["No growth (c)", "No growth (c)", "No growth (c)", "No growth (c)"]
    assert rows[0]["data"]["expanded_merged_cells"] == [1, 2, 3, 4]
    assert table["data"]["merged_cells"][0]["type"] == "column_span"
    assert "(a)" in note_text
    assert "(b)" in note_text
    assert "(c)" in note_text
    assert "Note 1:" in note_text
    assert "Note 2:" in note_text


def test_annex1_tables_do_not_leave_forbidden_plaintext_or_embedded_captions() -> None:
    ir = _ir()
    nodes = _flatten(ir["content"])

    assert not any("possible_plaintext_table_not_structured" in (node.get("tags") or []) for node in nodes)
    for node in nodes:
        if node.get("kind") in {"chapter", "section", "paragraph", "item", "subitem"}:
            text = node.get("text") or ""
            assert "Table 3:" not in text
            assert "Table 4:" not in text


def test_annex1_tables_do_not_embed_running_footers() -> None:
    ir = _ir()
    nodes = _flatten(ir["content"])

    for node in nodes:
        if node.get("kind") in {"table", "table_row", "note"}:
            assert "PE 009-17" not in (node.get("text") or "")
            data = node.get("data") or {}
            assert "PE 009-17" not in "\n".join(str(line) for line in data.get("raw_lines") or [])
            assert "PE 009-17" not in "\n".join(str(cell) for cell in data.get("cells") or [])
            assert "PE 009-17" not in "\n".join(str(op) for op in data.get("operations") or [])


def test_annex1_tables_promotion_gate_passes(tmp_path: Path) -> None:
    from qai_text2ir import cli

    out_dir = tmp_path / "pics_annex1_tables_bundle"
    cli.bundle(
        input=SOURCE,
        out_dir=out_dir,
        doc_id="pics_annex1_tables_bundle",
        title="PIC/S Annex 1",
        short_title="PIC/S Annex 1",
        jurisdiction="PIC/S",
        language="en",
        family="PIC/S",
        parser_profile_path=PROFILE,
        source_url="https://picscheme.org",
        retrieved_at="2026-05-23",
        emit_only="all",
        qualitycheck=True,
        strict=False,
        write_manifest=True,
        overwrite_manifest=False,
    )

    result = check_bundle(out_dir, "pics_annex1_tables_bundle", mode="promotion")

    assert result.passed
