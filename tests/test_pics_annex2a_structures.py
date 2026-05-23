from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from qai_text2ir.goal_check import check_bundle
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


SOURCE = Path("data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt")
PROFILE = Path("src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml")


def _flatten(node: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = [node]
    for child in node.get("children", []) or []:
        out.extend(_flatten(child))
    return out


def _ir() -> Dict[str, Any]:
    profile = load_parser_profile(path=PROFILE)
    return parse_text_to_ir(
        input_path=SOURCE,
        doc_id="pics_annex2a_structures_test",
        parser_profile=profile,
    ).to_dict()


def _table1(ir: Dict[str, Any]) -> Dict[str, Any]:
    return next(
        node
        for node in _flatten(ir["content"])
        if node.get("kind") == "table" and (node.get("data") or {}).get("parser") == "pics_annex2a_table1"
    )


def _rows(table: Dict[str, Any]) -> List[Dict[str, Any]]:
    header = next(child for child in table.get("children", []) if child.get("kind") == "table_header")
    return [child for child in header.get("children", []) if child.get("kind") == "table_row"]


def test_annex2a_table1_product_classes_and_notes_are_structured() -> None:
    table = _table1(_ir())
    rows = _rows(table)
    product_classes = [row["data"]["product_class"] for row in rows]
    notes = [child for child in table.get("children", []) if child.get("kind") == "note"]

    assert product_classes == [
        "Gene therapy: mRNA",
        "Gene therapy: in vivo viral vectors",
        "Gene therapy: in vivo non-viral vectors (naked DNA, lipoplexes, polyplexes, etc.)",
        "Gene therapy: ex-vivo genetically modified cells",
        "Somatic cell therapy",
        "Tissue engineered products",
    ]
    assert len(notes) == 3
    assert table["data"]["shading_reconstructed"] is False


def test_annex2a_figures_are_informative_figure_nodes() -> None:
    figures = {
        str(node.get("num")): node
        for node in _flatten(_ir()["content"])
        if node.get("kind") == "figure"
    }

    assert set(figures) == {"1", "2", "3"}
    assert figures["1"]["role"] == "informative"
    assert "gene therapy mRNA" in figures["1"]["heading"]
    assert "in vivo viral vector gene therapy" in figures["2"]["heading"]
    assert "autologous CAR-T therapy" in figures["3"]["heading"]
    assert len(figures["3"]["data"]["columns"]) == 3
    assert "Transduction" in figures["3"]["data"]["columns"][2]["steps"]


def test_annex2a_special_structures_do_not_remain_in_ordinary_text() -> None:
    nodes = _flatten(_ir()["content"])

    assert not any("possible_plaintext_table_not_structured" in (node.get("tags") or []) for node in nodes)
    assert not any("possible_form_or_table" in (node.get("tags") or []) for node in nodes)
    for node in nodes:
        if node.get("kind") in {"paragraph", "item", "subitem"}:
            text = node.get("text") or ""
            assert "Table 1. Illustrative guide" not in text
            assert "Figure 1:" not in text
            assert "Figure 2:" not in text
            assert "Figure 3:" not in text


def test_annex2a_structures_promotion_gate_passes(tmp_path: Path) -> None:
    from qai_text2ir import cli

    out_dir = tmp_path / "pics_annex2a_structures_bundle"
    cli.bundle(
        input=SOURCE,
        out_dir=out_dir,
        doc_id="pics_annex2a_structures_bundle",
        title="PIC/S Annex 2A",
        short_title="PIC/S Annex 2A",
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

    result = check_bundle(out_dir, "pics_annex2a_structures_bundle", mode="promotion")

    assert result.passed
