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


def test_refine_subtrees_fallback_applies_to_unmapped_annex() -> None:
    input_path = Path("tests/fixtures/pics_annexes_refine_fallback_excerpt.txt")
    profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/pics_annexes_default_v3.yaml"))

    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annexes_refine_fallback_excerpt",
        parser_profile=profile,
    ).to_dict()

    annex_3 = next(
        n
        for n in ir["content"].get("children", [])
        if n.get("kind") == "annex" and n.get("num") == "3"
    )
    nodes_3 = _flatten(annex_3)

    sec_1 = next(n for n in nodes_3 if n.get("kind") == "section" and n.get("num") == "1")
    p_11 = next(n for n in nodes_3 if n.get("kind") == "paragraph" and n.get("num") == "1.1")

    assert "PRINCIPLE" in ((sec_1.get("heading") or "") + " " + (sec_1.get("text") or "")).upper()
    assert "First paragraph in annex 3." in (p_11.get("text") or "")
    assert _first_line_locator(p_11) == "line:4"


def test_refine_subtrees_dispatch_still_wins_over_fallback() -> None:
    input_path = Path("tests/fixtures/pics_annexes_refine_fallback_excerpt.txt")
    profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/pics_annexes_default_v3.yaml"))

    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annexes_refine_dispatch_precedence",
        parser_profile=profile,
    ).to_dict()

    annex_15 = next(
        n
        for n in ir["content"].get("children", [])
        if n.get("kind") == "annex" and n.get("num") == "15"
    )
    nodes_15 = _flatten(annex_15)

    sec_2 = next(n for n in nodes_15 if n.get("kind") == "section" and n.get("num") == "2")
    p_21 = next(n for n in nodes_15 if n.get("kind") == "paragraph" and n.get("num") == "2.1")

    assert sec_2.get("heading") == "DOCUMENTATION, INCLUDING VMP"
    assert "Good documentation should be maintained." in (p_21.get("text") or "")
