from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def test_toc_is_skipped_and_annex_boundaries_keep_2a() -> None:
    input_path = Path("tests/fixtures/pics_annexes_full_excerpt.txt")
    profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/pics_annexes_default_v1.yaml"))

    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annexes_full_excerpt",
        parser_profile=profile,
    ).to_dict()

    root = ir["content"]
    annexes = [n for n in root.get("children", []) if n.get("kind") == "annex"]
    assert [n.get("num") for n in annexes] == ["1", "2A", "15"]

    annex_2a = next(n for n in annexes if n.get("num") == "2A")
    assert "MANUFACTURE OF ADVANCED THERAPY MEDICINAL PRODUCTS FOR HUMAN USE" in (
        annex_2a.get("heading") or ""
    )

    nodes = _flatten(root)
    all_text = "\n".join((n.get("heading") or "") + "\n" + (n.get("text") or "") for n in nodes)
    assert "ANNEX 1 ... 1" not in all_text
    assert "ANNEX 2A ... 68" not in all_text
    assert not re.search(
        r"PE\s*009-17\s*\(Annexes\)\s*-\s*\d{1,3}\s*-\s*25\s+August\s+2023",
        all_text,
        flags=re.IGNORECASE,
    )


def test_inline_running_header_tail_is_stripped() -> None:
    input_path = Path("tests/fixtures/pics_annexes_full_excerpt.txt")
    profile = load_parser_profile(path=Path("src/qai_text2ir/profiles/pics_annexes_default_v1.yaml"))

    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_annexes_inline_header_strip",
        parser_profile=profile,
    ).to_dict()

    annex_15 = next(
        n for n in ir["content"].get("children", []) if n.get("kind") == "annex" and n.get("num") == "15"
    )
    text_15 = annex_15.get("text") or ""
    assert "acceptance criteria." in text_15
    assert "Annex 15 Qualification and validation" not in text_15
