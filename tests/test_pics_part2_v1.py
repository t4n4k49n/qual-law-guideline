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


def test_skip_toc_and_parse_intro() -> None:
    input_path = Path("tests/fixtures/pics_part2_toc_intro_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_part2_default_v1.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_part2_toc_intro_fixture",
        parser_profile=parser_profile,
    )
    root = ir_doc.to_dict()["content"]
    nodes = _flatten(root)

    chapters = [n for n in root.get("children", []) if n["kind"] == "chapter"]
    assert len(chapters) == 1
    assert chapters[0].get("num") == "1"
    assert chapters[0].get("heading") == "INTRODUCTION"
    assert "PE 009-17 (Part II) - 1 - 25 August 2023" not in (chapters[0].get("text") or "")

    section_11 = next(n for n in nodes if n["kind"] == "section" and n.get("num") == "1.1")
    assert "Objective" in (section_11.get("text") or "")
    assert not any(
        "19.9 Documentation" in (n.get("heading") or "") for n in nodes if n.get("kind") == "chapter"
    )


def test_bullet_dingbat_detected() -> None:
    input_path = Path("tests/fixtures/pics_part2_bullet_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_part2_default_v1.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_part2_bullet_fixture",
        parser_profile=parser_profile,
    )
    nodes = _flatten(ir_doc.to_dict()["content"])

    assert any(n["kind"] == "item" and n.get("num") == "1" for n in nodes)
    assert any(n["kind"] == "subitem" for n in nodes)
