from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _span_pairs(node: Dict) -> List[Tuple[str, str]]:
    pairs: List[Tuple[str, str]] = []
    for span in node.get("source_spans", []):
        pairs.append((str(span.get("source_label")), str(span.get("locator"))))
    return pairs


def test_cfr_v2_structure_kind_raw_spans_and_section_split(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "PART 11 ELECTRONIC RECORDS; ELECTRONIC SIGNATURES",
            "Subpart A—General Provisions",
            "§ 11.1 Scope.",
            "(a) Intro paragraph.",
            "Subpart B—Electronic Records",
            "§ 11.10 Controls for closed systems.",
            "(b)(2)(ii) Example body text.",
            "Subpart C—Electronic Signatures",
            "§ 11.300 Controls for identification codes/passwords. Persons who use identification codes/passwords shall employ controls.",
        ]
    )
    input_path = tmp_path / "CFR_PART11_quality_v2.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")

    profile = load_parser_profile(family="US_CFR")
    assert profile["id"] == "us_cfr_default_v2"

    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="us_cfr_part11_quality_v2",
        parser_profile=profile,
    ).to_dict()

    nodes = _flatten(ir["content"])

    subparts = [n for n in nodes if n["kind"] == "subpart"]
    assert len(subparts) >= 3
    assert any(n.get("num") == "A" and n.get("heading") == "General Provisions" for n in subparts)
    assert any(n.get("num") == "B" and n.get("heading") == "Electronic Records" for n in subparts)
    assert any(n.get("num") == "C" and n.get("heading") == "Electronic Signatures" for n in subparts)

    text_values = [n.get("text") or "" for n in nodes]
    assert all("Subpart B—Electronic Records" not in t for t in text_values)
    assert all("Subpart C—Electronic Signatures" not in t for t in text_values)

    paragraph_b = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "b")
    item_2 = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "2")
    subitem_ii = next(n for n in nodes if n["kind"] == "subitem" and n.get("num") == "ii")
    assert paragraph_b.get("kind_raw") == "(b)"
    assert item_2.get("kind_raw") == "(2)"
    assert subitem_ii.get("kind_raw") == "(ii)"

    for node in nodes:
        pairs = _span_pairs(node)
        assert len(pairs) == len(set(pairs))
        assert all(p[0] == "CFR" for p in pairs)

    sec_11300 = next(n for n in nodes if n["kind"] == "section" and n.get("num") == "11.300")
    assert sec_11300.get("heading") == "Controls for identification codes/passwords."
    assert "Persons who use identification codes/passwords shall employ controls." in (
        sec_11300.get("text") or ""
    )
