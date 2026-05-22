from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir
from qai_text2ir.who_lbm_chap8_survey import parse_chap8_survey_tables, summarize_tables
from qai_xml2ir.verify import verify_document


FIXTURE = Path("tests/fixtures/who_lbm_chap8_text_layer.txt")


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _table_rows(table: Dict) -> List[Dict]:
    rows: List[Dict] = []
    for section in table.get("children", []):
        if section.get("kind") == "table_header":
            rows.extend([row for row in section.get("children", []) if row.get("kind") == "table_row"])
    return rows


def test_chap8_survey_fixture_counts_and_golden_rows() -> None:
    lines = FIXTURE.read_text(encoding="utf-8").splitlines()
    result = parse_chap8_survey_tables(lines)
    summary = summarize_tables(result.tables)

    assert summary["5"]["row_count"] == 81
    assert summary["6"]["row_count"] == 37
    assert summary["7"]["row_count"] == 15
    assert sum(info["row_count"] for info in summary.values()) == 133

    by_table_section = {
        (table.table_no, section.heading): [row.text for row in section.rows]
        for table in result.tables
        for section in table.sections
    }

    assert "Proper signage: ultraviolet light, laser, radioactive material, etc." in by_table_section[("5", "Laboratory")]
    assert "Appropriate biosafety guidelines available and followed" in by_table_section[("5", "Laboratory")]
    assert "Laboratory equipment properly labelled (biohazardous, radioactive, toxic, etc.)" in by_table_section[("5", "Laboratory")]
    assert "Microwave oven(s) clearly labelled “No Food Preparation, Laboratory Use Only”" in by_table_section[("5", "General practices and procedures")]
    assert "No trash on floor" in by_table_section[("5", "Waste management")]
    assert "BSC surface wiped down with appropriate disinfectant at beginning and end of each procedure" in by_table_section[("6", "Biological safety cabinet (BSC)")]
    assert "Information on sign accurate and current" in by_table_section[("6", "Laboratory")]
    assert "Sign legible and not defaced" in by_table_section[("6", "Laboratory")]
    assert "Double gloves worn when handling infectious material, potentially contaminated equipment and work surfaces" in by_table_section[("7", "Hand protection")]


def test_full_who_lbm_chap8_tables_are_structured_rows() -> None:
    profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml"))
    ir_doc = parse_text_to_ir(
        input_path=Path("data/human-readable/who/WHO_LBM_3rd.txt"),
        doc_id="who_lbm_3rd_2004_9241546506",
        parser_profile=profile,
    )
    ir = ir_doc.to_dict()
    verify_document(ir)
    nodes = _flatten(ir["content"])
    chapter8 = next(node for node in nodes if node["kind"] == "chapter" and node.get("num") == "8")
    tables = [child for child in chapter8["children"] if child["kind"] == "table"]
    by_no = {table["num"]: table for table in tables}

    assert set(by_no) >= {"5", "6", "7"}
    assert len(_table_rows(by_no["5"])) == 81
    assert len(_table_rows(by_no["6"])) == 37
    assert len(_table_rows(by_no["7"])) == 15

    rows = _table_rows(by_no["5"]) + _table_rows(by_no["6"]) + _table_rows(by_no["7"])
    row_texts = [row["text"] for row in rows]
    assert "Information on sign accurate and current" in row_texts
    assert "Sign legible and not defaced" in row_texts
    assert "No trash on floor" in row_texts
    assert "Microwave oven(s) clearly labelled “No Food Preparation, Laboratory Use Only”" in row_texts

    visible = "\n".join([node.get("heading") or "" for node in nodes] + [node.get("text") or "" for node in nodes])
    forbidden = [
        "\x01",
        "\uec1e",
        "........................",
        "CHECKED ITEM (ENTER DATE OF CHECK)",
        "YES NO N/A COMMENTS",
        "Location Date",
        "Person in charge of laboratory",
        "Safety surveyor",
        "Date survey completed",
        "Brand:",
        "Type:",
        "Serial no.:",
    ]
    assert not any(token in visible for token in forbidden)
    assert not any(node["nid"].startswith("cha8.i5.si") for node in nodes)
