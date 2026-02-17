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


def test_annex11_profile_header_footer_strip_and_structure() -> None:
    input_path = Path("tests/fixtures/pics_annex11_profile_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_annex11_default_v1.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annex11_fixture",
        parser_profile=parser_profile,
    )
    root = ir_doc.to_dict()["content"]
    nodes = _flatten(root)

    annexes = [n for n in root.get("children", []) if n["kind"] == "annex" and n.get("num") == "11"]
    assert len(annexes) == 1
    annex = annexes[0]
    assert annex.get("heading") == "COMPUTERISED SYSTEMS"
    annex_text = annex.get("text") or ""
    assert "PE 009-17 (Annexes) -170- 25 August 2023" not in annex_text
    assert "Annex 11 Computerised systems" not in annex_text

    section_4 = next(n for n in nodes if n["kind"] == "section" and n.get("num") == "4")
    assert "Validation" in (section_4.get("text") or "")
    paragraph_41 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "4.1")
    assert "validation documentation" in (paragraph_41.get("text") or "")
    items = [n for n in nodes if n["kind"] == "item"]
    assert any(i.get("num") == "a" for i in items)
    assert any(i.get("num") == "b" for i in items)
