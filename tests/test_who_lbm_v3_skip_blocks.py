from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _load_profile(path: str) -> Dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_skip_blocks_contents_to_foreword() -> None:
    input_path = Path("tests/fixtures/who_lbm_contents_block_excerpt.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v3.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_contents_block_excerpt",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    nodes = _flatten(ir_dict["content"])
    root_children = ir_dict["content"]["children"]

    parts = [n for n in root_children if n["kind"] == "part"]
    assert any((n.get("num") or "").upper() == "I" for n in parts)
    part_i = next(n for n in parts if (n.get("num") or "").upper() == "I")
    assert any(ch["kind"] == "chapter" and ch.get("num") == "1" for ch in part_i.get("children", []))

    chapters_1 = [n for n in nodes if n["kind"] == "chapter" and n.get("num") == "1"]
    assert chapters_1
    assert chapters_1[0].get("heading") == "General principles"

    joined = "\n".join((n.get("heading") or "") for n in nodes if n["kind"] in {"chapter", "part", "annex"})
    assert "General principles 1" not in joined
    assert "Chemicals: hazards and precautions 145" not in joined


def test_annex_punctuation_not_in_heading() -> None:
    input_path = Path("tests/fixtures/who_lbm_annex_repeated_excerpt.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v3.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_annex_repeated_excerpt",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    root_children = ir_dict["content"]["children"]

    annex_4 = [n for n in root_children if n["kind"] == "annex" and n.get("num") == "4"]
    assert len(annex_4) == 1
    assert annex_4[0].get("heading") == "Equipment safety"

    warnings = qualitycheck_document(ir_doc.content)
    assert not any("duplicate structural siblings" in msg for msg in warnings)
