from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from qai_text2ir.goal_check import check_bundle
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


SOURCE = Path("data/human-readable/who/WHO_LBM_3rd.txt")
PROFILE = Path("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml")
DOC_ID = "who_lbm_3rd_2004_9241546506"
TARGET_CAPTIONS = [
    "Table 1. Classification of infective microorganisms by risk group",
    "Table 2. Relation of risk groups to biosafety levels, practices and equipment",
    "Table 3. Summary of biosafety level requirements",
    "Table 4. Animal facility containment levels: summary of practices and safety equipment",
    "Table 8. Selection of a biological safety cabinet (BSC), by type of protection needed",
    "Table 9. Differences between Class I, II and III biological safety cabinets (BSCs)",
    "Table 10. Biosafety equipment",
    "Table 11. Personal protective equipment",
    "Table 12. Recommended dilutions of chlorine-releasing compounds",
    "Table 13. General rules for chemical incompatibilities",
    "Table 14. Storage of compressed and liquefied gases",
    "Table 15. Types and uses of fire extinguishers",
    "Table A4-1. Equipment and operations that may create hazards",
    "Table A4-2. Common causes of equipment-related accidents",
    "Table A5-1. Chemicals: hazards and precautions",
]


def _flatten(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = [node]
    for child in node.get("children", []) or []:
        out.extend(_flatten(child))
    return out


def _ir() -> Dict[str, Any]:
    return parse_text_to_ir(
        input_path=SOURCE,
        doc_id=DOC_ID,
        parser_profile=load_parser_profile(path=PROFILE),
    ).to_dict()


def _table(ir: Dict[str, Any], no: str) -> Dict[str, Any]:
    return next(
        node
        for node in _flatten(ir["content"])
        if node.get("kind") == "table"
        and (node.get("data") or {}).get("parser") == "who_lbm_general_tables"
        and (node.get("data") or {}).get("table_no") == no
    )


def _rows(table: Dict[str, Any]) -> List[Dict[str, Any]]:
    header = next(child for child in table.get("children", []) if child.get("kind") == "table_header")
    return [child for child in header.get("children", []) if child.get("kind") == "table_row"]


def test_who_lbm_general_table_1_risk_groups_are_structured() -> None:
    rows = _rows(_table(_ir(), "1"))
    assert [row["data"]["row_key"] for row in rows] == [
        "Risk Group 1",
        "Risk Group 2",
        "Risk Group 3",
        "Risk Group 4",
    ]
    assert "unlikely to cause human or animal disease" in rows[0]["data"]["cells"][2]


def test_who_lbm_general_table_2_biosafety_level_rows_are_structured() -> None:
    rows = _rows(_table(_ir(), "2"))
    assert rows[0]["data"]["cells"][:2] == ["1", "Basic - Biosafety Level 1"]
    assert rows[-1]["data"]["cells"][1] == "Maximum containment - Biosafety Level 4"
    assert "double-ended autoclave" in rows[-1]["data"]["cells"][-1]


def test_who_lbm_general_table_3_isolation_row_has_bsl_columns() -> None:
    row = next(row for row in _rows(_table(_ir(), "3")) if row["data"]["row_key"] == "Isolation of laboratory")
    assert row["data"]["cells"] == ["Isolation of laboratory", "No", "No", "Yes", "Yes"]


def test_who_lbm_general_table_8_bsc_selection_rows_are_structured() -> None:
    rows = _rows(_table(_ir(), "8"))
    assert rows[0]["data"]["cells"][1] == "Class I, Class II, Class III"
    assert rows[-1]["data"]["cells"] == [
        "Volatile radionuclide/chemical protection",
        "Class I, Class IIB2, Class III",
    ]


def test_who_lbm_general_table_10_preserves_bullet_features_in_cells() -> None:
    rows = _rows(_table(_ir(), "10"))
    pipetting = next(row for row in rows if row["data"]["row_key"] == "Pipetting aids")
    assert "• Ease of use" in pipetting["data"]["cells"][2]
    assert "• Controls leakage from pipette tip" in pipetting["data"]["cells"][2]


def test_who_lbm_general_table_12_preserves_dilutions_and_footnotes() -> None:
    table = _table(_ir(), "12")
    rows = _rows(table)
    assert rows[0]["data"]["cells"] == ["Available chlorine required", "0.1% (1 g/l)", "0.5% (5 g/l)"]
    assert rows[-1]["data"]["cells"] == ["Chloramine (25% available chlorine) (c)", "20 g/l", "20 g/l"]
    notes = "\n".join(child.get("text") or "" for child in table.get("children", []) if child.get("kind") == "note")
    assert "After removal of bulk material" in notes
    assert "For flooding" in notes


def test_who_lbm_general_table_15_fire_extinguisher_rows_are_structured() -> None:
    rows = _rows(_table(_ir(), "15"))
    assert [row["data"]["row_key"] for row in rows] == [
        "Water",
        "Carbon dioxide (CO2) extinguisher gases",
        "Dry powder",
        "Foam",
    ]
    assert "burning metals" in rows[0]["data"]["cells"][2]


def test_who_lbm_annex_fixed_width_tables_are_line_preserving() -> None:
    ir = _ir()
    table_a4_1 = _table(ir, "A4-1")
    table_a4_2 = _table(ir, "A4-2")
    table_a5_1 = _table(ir, "A5-1")

    assert table_a4_1["data"]["source_format"] == "fixed_width_line_preserving_table"
    assert table_a4_2["data"]["source_format"] == "fixed_width_line_preserving_table"
    assert table_a5_1["data"]["source_format"] == "fixed_width_line_preserving_table"

    a4_1_rows = _rows(table_a4_1)
    a4_2_rows = _rows(table_a4_2)
    a5_1_rows = _rows(table_a5_1)

    assert not a4_1_rows[0]["data"]["raw_line"].startswith("Table A4-1")
    assert any(row["data"]["cells"][0] == "Hypodermic" for row in a4_1_rows)
    assert any("Electrical fires" in row["data"]["cells"][0] for row in a4_2_rows)
    assert any(row["data"]["cells"][0] == "Acetaldehyde" for row in a5_1_rows)
    assert any(row["data"]["cells"][0].startswith("Acetic acid") for row in a5_1_rows)

    acetaldehyde = next(row for row in a5_1_rows if row["data"]["cells"][0] == "Acetaldehyde")
    assert acetaldehyde["data"]["cells"][4] == "No open flames, no"
    assert acetaldehyde["data"]["cells"][5] == "Can form explosive"


def test_who_lbm_general_target_captions_not_embedded_in_ordinary_text() -> None:
    ordinary = {"preamble", "part", "chapter", "annex", "section", "item", "subitem"}
    for node in _flatten(_ir()["content"]):
        if node.get("kind") not in ordinary:
            continue
        text = " ".join(value for value in [node.get("heading"), node.get("text")] if value)
        for caption in TARGET_CAPTIONS:
            assert caption not in text


def test_who_lbm_general_figures_are_structured() -> None:
    figures = [
        node
        for node in _flatten(_ir()["content"])
        if node.get("kind") == "figure" and (node.get("data") or {}).get("parser") == "who_lbm_general_tables"
    ]
    figure_nos = {(node.get("data") or {}).get("figure_no") for node in figures}
    assert {"1", "4", "5", "6", "7", "8", "9", "10", "11", "12"}.issubset(figure_nos)


def test_who_lbm_general_promotion_has_no_target_plaintext_table_warning(tmp_path: Path) -> None:
    from qai_text2ir import cli

    out_dir = tmp_path / "who_lbm_general_bundle"
    cli.bundle(
        input=SOURCE,
        out_dir=out_dir,
        doc_id=DOC_ID,
        title="WHO Laboratory Biosafety Manual, 3rd ed.",
        short_title="WHO LBM 3rd",
        jurisdiction="WHO",
        language="en",
        family="WHO_LBM",
        parser_profile_path=PROFILE,
        source_url="https://www.who.int/publications/i/item/9241546506",
        retrieved_at="2026-05-23",
        emit_only="all",
        qualitycheck=True,
        strict=False,
        write_manifest=True,
        overwrite_manifest=False,
    )

    result = check_bundle(out_dir, DOC_ID, mode="promotion")
    target_text = "\n".join(TARGET_CAPTIONS)
    messages = "\n".join(error.message for error in result.errors + result.warnings)

    assert "possible_plaintext_table_not_structured" not in messages or not any(
        caption in messages for caption in TARGET_CAPTIONS
    )
    assert target_text
