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


def test_drop_toc_entries_no_structural_nodes() -> None:
    input_path = Path("tests/fixtures/WHO_LBM_3rd_toc_excerpt_v2.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_toc_fixture_v2",
        parser_profile=parser_profile,
    )
    nodes = _flatten(ir_doc.to_dict()["content"])

    chapters_1 = [n for n in nodes if n["kind"] == "chapter" and n.get("num") == "1"]
    assert len(chapters_1) == 1
    assert chapters_1[0].get("heading") == "General principles"
    assert not any((n.get("heading") or "").rstrip().endswith((" 1", " 7", " 145", " 170", " 172")) for n in nodes)


def test_drop_repeated_annex_headers_no_duplicate_annex_siblings() -> None:
    input_path = Path("tests/fixtures/WHO_LBM_3rd_annex5_repeated_header_excerpt_v2.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_annex5_fixture_v2",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    root_children = ir_dict["content"]["children"]
    annex_5 = [n for n in root_children if n["kind"] == "annex" and n.get("num") == "5"]
    assert len(annex_5) == 1

    warnings = qualitycheck_document(ir_doc.content)
    assert not any("duplicate structural siblings" in msg for msg in warnings)
