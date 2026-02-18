from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _first_line_locator(node: Dict) -> Optional[str]:
    spans = node.get("source_spans") or []
    if not spans:
        return None
    locator = spans[0].get("locator")
    return locator if isinstance(locator, str) else None


def test_refine_subtrees_dispatch_applies() -> None:
    input_path = Path("tests/fixtures/pics_annexes_refine_excerpt.txt")
    profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/pics_annexes_default_v2.yaml"))

    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annexes_refine_excerpt",
        parser_profile=profile,
    ).to_dict()

    root = ir["content"]
    annexes = [n for n in root.get("children", []) if n.get("kind") == "annex"]
    annex_1 = next(n for n in annexes if n.get("num") == "1")
    annex_15 = next(n for n in annexes if n.get("num") == "15")
    annex_2b = next(n for n in annexes if n.get("num") == "2B")

    nodes_1 = _flatten(annex_1)
    nodes_15 = _flatten(annex_15)
    nodes_2b = _flatten(annex_2b)

    assert any(n.get("kind") == "section" for n in nodes_1)
    assert any(n.get("kind") == "paragraph" and n.get("num") == "1.1" for n in nodes_1)
    assert any(n.get("kind") == "section" and n.get("num") == "2" for n in nodes_15)
    assert any(n.get("kind") == "paragraph" and n.get("num") == "2.1" for n in nodes_15)
    assert any(n.get("kind") == "item" and n.get("num") == "ii" for n in nodes_15)
    assert not any(n.get("kind") in {"section", "paragraph"} for n in nodes_2b[1:])


def test_source_spans_keep_original_line_numbers() -> None:
    input_path = Path("tests/fixtures/pics_annexes_refine_excerpt.txt")
    profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/pics_annexes_default_v2.yaml"))

    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annexes_refine_line_locator",
        parser_profile=profile,
    ).to_dict()

    annex_15 = next(
        n
        for n in ir["content"].get("children", [])
        if n.get("kind") == "annex" and n.get("num") == "15"
    )
    nodes_15 = _flatten(annex_15)
    p_24 = next(n for n in nodes_15 if n.get("kind") == "paragraph" and n.get("num") == "2.4")
    item_ii = next(n for n in nodes_15 if n.get("kind") == "item" and n.get("num") == "ii")

    assert _first_line_locator(p_24) == "line:30"
    assert _first_line_locator(item_ii) == "line:32"
