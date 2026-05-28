from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

from qai_text2ir.goal_check import check_bundle
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


SOURCE = Path("data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt")
PROFILE = Path("src/qai_text2ir/profiles/pics_part2_default_v1.yaml")


def _flatten(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = [node]
    for child in node.get("children", []) or []:
        out.extend(_flatten(child))
    return out


def _ir(profile: Dict[str, Any] | None = None) -> Dict[str, Any]:
    parser_profile = profile or load_parser_profile(path=PROFILE)
    return parse_text_to_ir(
        input_path=SOURCE,
        doc_id="pics_part2_table1_test",
        parser_profile=parser_profile,
    ).to_dict()


def _table1(ir: Dict[str, Any]) -> Dict[str, Any]:
    return next(
        node
        for node in _flatten(ir["content"])
        if node.get("kind") == "table" and (node.get("data") or {}).get("parser") == "pics_part2_api_table1"
    )


def _rows(table: Dict[str, Any]) -> List[Dict[str, Any]]:
    header = next(child for child in table.get("children", []) if child.get("kind") == "table_header")
    return [child for child in header.get("children", []) if child.get("kind") == "table_row"]


def test_part2_table1_header_preserves_spanning_parent_header() -> None:
    table = _table1(_ir())
    header = next(child for child in table.get("children", []) if child.get("kind") == "table_header")
    columns = header["data"]["columns"]

    assert columns == [
        "Type of Manufacturing",
        "Application of this Guide to steps (shown in grey) used in this type of manufacturing step 1",
        "Application of this Guide to steps (shown in grey) used in this type of manufacturing step 2",
        "Application of this Guide to steps (shown in grey) used in this type of manufacturing step 3",
        "Application of this Guide to steps (shown in grey) used in this type of manufacturing step 4",
        "Application of this Guide to steps (shown in grey) used in this type of manufacturing step 5",
    ]
    assert header["text"] == " | ".join(columns)
    assert len(columns) == len(set(columns))


def test_part2_table1_rows_are_structured() -> None:
    table = _table1(_ir())
    rows = _rows(table)
    manufacturing_types = [row["data"]["manufacturing_type"] for row in rows]

    assert manufacturing_types == [
        "Chemical Manufacturing",
        "API derived from animal sources",
        "API extracted from plant sources",
        "Herbal extracts used as API",
        "API consisting of comminuted or powdered herbs",
        "Biotechnology: fermentation / cell culture",
        "“Classical” Fermentation to produce an API",
    ]
    assert table["data"]["shading_reconstructed"] is False


def test_part2_table1_preserves_multiline_cells_and_annotation() -> None:
    table = _table1(_ir())
    rows = _rows(table)
    note_text = "\n".join(child.get("text") or "" for child in table.get("children", []) if child.get("kind") == "note")

    assert rows[0]["data"]["cells"][1] == "Production of the API Starting Material"
    assert rows[0]["data"]["cells"][2] == "Introduction of the API Starting Material into process"
    assert rows[-1]["data"]["cells"][3] == "Introduction of the cells into fermentation"
    assert "Increasing GMP requirements" in note_text


def test_part2_table1_caption_not_embedded_in_ordinary_text() -> None:
    nodes = _flatten(_ir()["content"])

    for node in nodes:
        if node.get("kind") in {"chapter", "section", "paragraph", "item", "subitem"}:
            text = node.get("text") or ""
            assert "Table 1:    Application of this Guide to API Manufacturing" not in text
            assert "Chemical           Production of" not in text
            assert "Increasing GMP requirements" not in text


def test_part2_table1_promotion_gate_passes(tmp_path: Path) -> None:
    from qai_text2ir import cli

    out_dir = tmp_path / "pics_part2_table1_bundle"
    cli.bundle(
        input=SOURCE,
        out_dir=out_dir,
        doc_id="pics_part2_table1_bundle",
        title="PIC/S Part II",
        short_title="PIC/S Part II",
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

    result = check_bundle(out_dir, "pics_part2_table1_bundle", mode="promotion")

    assert result.passed


def test_part2_table1_promotion_gate_fails_when_unstructured(tmp_path: Path) -> None:
    from qai_text2ir import cli

    profile = load_parser_profile(path=PROFILE)
    profile["id"] = "pics_part2_table1_disabled_test"
    profile["preprocess"]["pics_part2_table1"]["enabled"] = False
    disabled_profile = tmp_path / "pics_part2_table1_disabled.yaml"
    disabled_profile.write_text(yaml.safe_dump(profile, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n")

    out_dir = tmp_path / "pics_part2_table1_unstructured_bundle"
    cli.bundle(
        input=SOURCE,
        out_dir=out_dir,
        doc_id="pics_part2_table1_unstructured_bundle",
        title="PIC/S Part II",
        short_title="PIC/S Part II",
        jurisdiction="PIC/S",
        language="en",
        family="PIC/S",
        parser_profile_path=disabled_profile,
        source_url="https://picscheme.org",
        retrieved_at="2026-05-23",
        emit_only="all",
        qualitycheck=True,
        strict=False,
        write_manifest=True,
        overwrite_manifest=False,
    )

    result = check_bundle(out_dir, "pics_part2_table1_unstructured_bundle", mode="promotion")

    assert not result.passed
    assert any(error.code == "special_structure_unresolved" for error in result.errors)
