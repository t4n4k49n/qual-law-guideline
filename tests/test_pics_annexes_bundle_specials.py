from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from qai_text2ir.goal_check import check_bundle
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


SOURCE = Path("data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt")
PROFILE = Path("src/qai_text2ir/profiles/pics_annexes_default_v3.yaml")
DOC_ID = "pics_pe00917_annexes_20230825_refined_v3_extends_trace"


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


def _nodes(ir: Dict[str, Any]) -> List[Dict[str, Any]]:
    return _flatten(ir["content"])


def _table_rows(table: Dict[str, Any]) -> List[Dict[str, Any]]:
    header = next(child for child in table.get("children", []) if child.get("kind") == "table_header")
    return [child for child in header.get("children", []) if child.get("kind") == "table_row"]


def test_combined_annexes_reuses_annex1_table_parser_results() -> None:
    nodes = _nodes(_ir())
    annex1_tables = [
        node
        for node in nodes
        if node.get("kind") == "table" and (node.get("data") or {}).get("parser") == "pics_annex1_tables"
    ]

    assert len(annex1_tables) >= 6
    assert {str((node.get("data") or {}).get("table_no")) for node in annex1_tables}.issuperset(
        {"1", "2", "3", "4", "5", "6"}
    )


def test_combined_annexes_reuses_annex2a_table_and_figure_parser_results() -> None:
    nodes = _nodes(_ir())
    annex2a_table = next(
        node
        for node in nodes
        if node.get("kind") == "table" and (node.get("data") or {}).get("parser") == "pics_annex2a_table1"
    )
    annex2a_figures = [
        node
        for node in nodes
        if node.get("kind") == "figure" and (node.get("data") or {}).get("parser") == "pics_annex2a_flow_figures"
    ]

    assert len(_table_rows(annex2a_table)) == 6
    assert {str(node.get("num")) for node in annex2a_figures} == {"1", "2", "3"}


def test_annex2b_table1_rows_notes_and_shading_are_structured() -> None:
    table = next(
        node
        for node in _nodes(_ir())
        if node.get("kind") == "table"
        and (node.get("data") or {}).get("parser") == "pics_annexes_bundle_specials"
        and (node.get("data") or {}).get("annex") == "2B"
    )
    rows = _table_rows(table)
    notes = [child for child in table.get("children", []) if child.get("kind") == "note"]

    assert [row["data"]["row_key"] for row in rows] == [
        "Animal or plant sources: non-transgenic",
        "Virus or bacteria / fermentation / cell culture",
        "Biotechnology fermentation / cell culture",
        "Animal sources: transgenic",
        "Plant sources: transgenic",
        "Human sources",
        "Human sources: products from cells and tissues not classified as ATMPs",
    ]
    assert len(notes) == 7
    assert table["data"]["shading_reconstructed"] is False
    assert "not preserve grey shading reliably" in table["data"]["shading_note"]


def test_annex20_qrm_process_is_informative_figure_node() -> None:
    figure = next(
        node
        for node in _nodes(_ir())
        if node.get("kind") == "figure"
        and (node.get("data") or {}).get("parser") == "pics_annexes_bundle_specials"
        and (node.get("data") or {}).get("annex") == "20"
    )
    steps = figure["data"]["steps"]

    assert figure["role"] == "informative"
    assert steps[:5] == [
        "Initiate Quality Risk Management Process",
        "Risk Assessment",
        "Risk Identification",
        "Risk Analysis",
        "Risk Evaluation",
    ]
    assert steps[-2:] == ["Risk Communication", "Risk Management tools"]


def test_combined_annexes_target_captions_not_embedded_in_ordinary_text() -> None:
    ordinary = {"annex", "section", "paragraph", "item", "subitem"}
    forbidden = [
        "Table 1. Illustrative guide to manufacturing activities within the scope of Annex 2B",
        "Figure 1: Overview of a typical quality risk management process",
    ]

    for node in _nodes(_ir()):
        if node.get("kind") not in ordinary:
            continue
        text = " ".join(value for value in [node.get("heading"), node.get("text")] if value)
        for caption in forbidden:
            assert caption not in text


def test_combined_annexes_promotion_gate_passes_for_targets(tmp_path: Path) -> None:
    from qai_text2ir import cli

    out_dir = tmp_path / "pics_annexes_bundle"
    cli.bundle(
        input=SOURCE,
        out_dir=out_dir,
        doc_id=DOC_ID,
        title="PIC/S PE 009-17 Annexes",
        short_title="PIC/S Annexes",
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

    result = check_bundle(out_dir, DOC_ID, mode="promotion")
    messages = "\n".join(error.message for error in result.errors + result.warnings)

    assert "Annex 2B" not in messages
    assert "quality risk management process" not in messages
    assert not any(
        "possible_plaintext_table_not_structured" in (node.get("tags") or [])
        for node in _nodes(parse_text_to_ir(input_path=SOURCE, doc_id=DOC_ID, parser_profile=load_parser_profile(path=PROFILE)).to_dict())
        if "Annex 2B" in str(node.get("heading") or node.get("text") or "")
    )
