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


def _load_profile(path: str) -> Dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_annex15_inline_header_stripped_and_footer_dropped() -> None:
    input_path = Path("tests/fixtures/pics_annex15_header_footer_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_annex15_default_v1.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annex15_fixture_header_footer",
        parser_profile=parser_profile,
    )

    root = ir_doc.to_dict()["content"]
    annexes = [n for n in root.get("children", []) if n["kind"] == "annex" and n.get("num") == "15"]
    assert len(annexes) == 1
    annex = annexes[0]
    assert annex.get("heading") == "QUALIFICATION AND VALIDATION"

    section_2 = next(n for n in _flatten(root) if n["kind"] == "section" and n.get("num") == "2")
    assert section_2.get("heading") == "DOCUMENTATION, INCLUDING VMP"
    section_text = section_2.get("text") or ""
    assert "Annex 15 Qualification and validation" not in section_text
    assert "PE 009-17 (Annexes) -214- 25 August 2023" not in section_text


def test_annex15_roman_items_parsed() -> None:
    input_path = Path("tests/fixtures/pics_annex15_roman_items_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_annex15_default_v1.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annex15_fixture_roman_items",
        parser_profile=parser_profile,
    )

    root = ir_doc.to_dict()["content"]
    nodes = _flatten(root)
    paragraph_15 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "1.5")
    assert "include" in (paragraph_15.get("text") or "")

    items = [n for n in nodes if n["kind"] == "item"]
    assert any(i.get("num") == "i" for i in items)
    assert any(i.get("num") == "ii" for i in items)
