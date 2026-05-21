from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def test_annex2a_part_a_b_and_b1_are_structured() -> None:
    parser_profile = yaml.safe_load(
        Path("src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml").read_text(encoding="utf-8")
    )
    ir_doc = parse_text_to_ir(
        input_path=Path("tests/fixtures/pics_annex2a_part_hierarchy_fixture.txt"),
        doc_id="pics_annex2a_part_hierarchy_fixture",
        parser_profile=parser_profile,
    )
    nodes = _flatten(ir_doc.to_dict()["content"])

    part_a = next(n for n in nodes if n["kind"] == "chapter" and n.get("num") == "A")
    part_b = next(n for n in nodes if n["kind"] == "chapter" and n.get("num") == "B")
    section_b1 = next(n for n in nodes if n["kind"] == "section" and n.get("num") == "B1")

    assert part_a.get("heading") == "GENERAL GUIDANCE"
    assert part_b.get("heading") == "SPECIFIC GUIDANCE ON SELECTED PRODUCT TYPES"
    assert section_b1.get("heading") == "ANIMAL SOURCED PRODUCTS"
