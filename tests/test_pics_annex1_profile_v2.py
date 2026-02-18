from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _load_profile(path: str) -> Dict:
    return load_parser_profile(path=Path(path))


def test_annex1_document_map_skipped_without_duplicate_sections() -> None:
    input_path = Path("tests/fixtures/pics_annex1_document_map_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_annex1_default_v2.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annex1_v2_document_map",
        parser_profile=parser_profile,
    )

    root = ir_doc.to_dict()["content"]
    annexes = [n for n in root.get("children", []) if n["kind"] == "annex" and n.get("num") == "1"]
    assert len(annexes) == 1
    annex = annexes[0]
    assert annex.get("heading") == "MANUFACTURE OF STERILE MEDICINAL PRODUCTS"

    sections = [n for n in annex.get("children", []) if n["kind"] == "section"]
    assert sum(1 for s in sections if s.get("num") == "1") == 1
    assert sum(1 for s in sections if s.get("num") == "2") == 1

    nodes = _flatten(annex)
    paragraph_11 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "1.1")
    assert "The manufacture" in (paragraph_11.get("text") or "")


def test_annex1_footer_and_inline_running_header_removed() -> None:
    input_path = Path("tests/fixtures/pics_annex1_noise_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_annex1_default_v2.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annex1_v2_noise",
        parser_profile=parser_profile,
    )

    annex = ir_doc.to_dict()["content"]["children"][0]
    nodes = _flatten(annex)
    all_text = "\n".join((n.get("text") or "") for n in nodes)

    assert "Annex 1 Manufacture of sterile medicinal products" not in all_text
    assert "PE 009-17 (Annexes) -2- 25 August 2023" not in all_text

    paragraph_12 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "1.2")
    assert "Next paragraph" in (paragraph_12.get("text") or "")
    assert any(n.get("kind") == "subitem" for n in nodes)
