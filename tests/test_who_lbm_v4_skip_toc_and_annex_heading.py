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


def test_skip_toc_block_does_not_create_structural_nodes_from_toc() -> None:
    input_path = Path("tests/fixtures/who_lbm_excerpt_skip_toc.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_v4_skip_toc_fixture",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    root = ir_dict["content"]
    nodes = _flatten(root)

    preambles = [n for n in root["children"] if n["kind"] == "preamble"]
    assert preambles
    assert "Foreword body line" in (preambles[0].get("text") or "")
    assert all((n.get("heading") or "") != "General principles 1" for n in nodes)
    assert all("Chemicals: hazards and precautions 145" not in (n.get("heading") or "") for n in nodes)

    parts = [n for n in root["children"] if n["kind"] == "part" and (n.get("num") or "").upper() == "I"]
    assert len(parts) == 1
    chapter_1 = [n for n in parts[0].get("children", []) if n["kind"] == "chapter" and n.get("num") == "1"]
    assert len(chapter_1) == 1
    assert chapter_1[0].get("heading") == "General principles"
    assert "Actual chapter body" in (chapter_1[0].get("text") or "")


def test_annex_dot_only_heading_is_not_left_as_heading(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "Annex 4.",
            "Equipment safety",
            "• item",
        ]
    )
    input_path = tmp_path / "who_lbm_v4_annex_dot.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_v4_annex_dot_fixture",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    root = ir_dict["content"]
    annex_4 = [n for n in root["children"] if n["kind"] == "annex" and n.get("num") == "4"]
    assert len(annex_4) == 1
    assert annex_4[0].get("heading") == "Equipment safety"
