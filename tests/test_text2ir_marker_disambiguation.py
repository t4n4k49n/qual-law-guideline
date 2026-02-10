from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _parse(tmp_path: Path, text: str) -> Dict:
    input_path = tmp_path / "input.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    profile = load_parser_profile(profile_id="us_cfr_default_v1")
    return parse_text_to_ir(
        input_path=input_path,
        doc_id="doc",
        parser_profile=profile,
    ).to_dict()


def test_alpha_gap_is_adopted_with_warning(tmp_path: Path, caplog) -> None:
    caplog.set_level(logging.WARNING)
    ir = _parse(
        tmp_path,
        "\n".join(
            [
                "§ 1.0 Title",
                "(a) A",
                "(1) A-1",
                "(c) C",
            ]
        ),
    )
    nodes = _flatten(ir["content"])
    c_node = next(n for n in nodes if n["kind"] == "paragraph" and n["num"] == "c")
    assert c_node["nid"].startswith("sec1_0.")
    assert any("marker gap adopted" in rec.message for rec in caplog.records)


def test_roman_under_item_stays_roman(tmp_path: Path) -> None:
    ir = _parse(
        tmp_path,
        "\n".join(
            [
                "§ 1.0 Title",
                "(a) A",
                "(1) One",
                "(i) Roman child",
            ]
        ),
    )
    nodes = _flatten(ir["content"])
    roman = next(n for n in nodes if n["num"] == "i")
    assert roman["kind"] == "subitem"
    assert ".i1.si" in roman["nid"]


def test_alpha_beats_roman_when_alpha_continuity_is_strong(tmp_path: Path) -> None:
    ir = _parse(
        tmp_path,
        "\n".join(
            [
                "§ 1.0 Title",
                "(a) A",
                "(b) B",
                "(1) B-1",
                "(xcvi) deep roman",
                "(c) C",
            ]
        ),
    )
    nodes = _flatten(ir["content"])
    c_node = next(n for n in nodes if n["num"] == "c")
    assert c_node["kind"] == "paragraph"
    assert c_node["nid"].startswith("sec1_0.pc")


def test_roman_c_is_selected_when_roman_sequence_is_clear(tmp_path: Path) -> None:
    ir = _parse(
        tmp_path,
        "\n".join(
            [
                "§ 1.0 Title",
                "(a) A",
                "(1) One",
                "(xcix) ninety-nine",
                "(c) hundred",
            ]
        ),
    )
    nodes = _flatten(ir["content"])
    c_node = next(n for n in nodes if n["num"] == "c")
    assert c_node["kind"] == "subitem"
    assert ".i1.sic" in c_node["nid"]

