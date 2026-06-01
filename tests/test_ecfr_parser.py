from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from qai_xml2ir.ecfr_parser import parse_ecfr_xml


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def test_ecfr_part11_xml_structure_notes_and_markers() -> None:
    parsed = parse_ecfr_xml(Path("data/human-readable/cfr/source_xml/title21_part11_2025-10-27.xml"))
    ir = parsed.root.to_dict()
    nodes = _flatten(ir)

    part = next(node for node in nodes if node["kind"] == "part")
    assert part["num"] == "11"
    assert part["heading"] == "ELECTRONIC RECORDS; ELECTRONIC SIGNATURES"

    subparts = [node for node in nodes if node["kind"] == "subpart"]
    assert [node["num"] for node in subparts] == ["A", "B", "C"]

    section = next(node for node in nodes if node["kind"] == "section" and node["num"] == "11.200")
    assert section["heading"] == "Electronic signature components and controls."

    paragraph_a = next(node for node in nodes if node["nid"].endswith(".sec11_200.pa"))
    item_1 = next(node for node in nodes if node["nid"].endswith(".sec11_200.pa.i1"))
    subitem_i = next(node for node in nodes if node["nid"].endswith(".sec11_200.pa.i1.sii"))
    assert paragraph_a["kind_raw"] == "(a)"
    assert item_1["kind_raw"] == "(1)"
    assert subitem_i["kind_raw"] == "(i)"
    assert "first signing shall be executed" in subitem_i["text"]

    section_111 = next(node for node in nodes if node["kind"] == "section" and node["num"] == "11.1")
    paragraph_i = next(node for node in nodes if node["nid"].endswith(".sec11_1.pi"))
    assert paragraph_i["kind"] == "paragraph"
    assert paragraph_i["kind_raw"] == "(i)"
    assert paragraph_i["nid"].startswith(section_111["nid"])

    notes = [node for node in nodes if node["kind"] == "note"]
    assert any((node.get("text") or "").startswith("Authority:") for node in notes)
    assert any((node.get("text") or "").startswith("Source:") for node in notes)
    assert any((node.get("text") or "").startswith("[62 FR") for node in notes)


def test_ecfr_part11_parser_metadata_from_filename() -> None:
    parsed = parse_ecfr_xml(Path("data/human-readable/cfr/source_xml/title21_part11_2025-10-27.xml"))
    assert parsed.cfr_title == "21"
    assert parsed.cfr_part == "11"
    assert parsed.as_of == "2025-10-27"


def test_ecfr_part211_alpha_after_items_returns_to_section_paragraph() -> None:
    parsed = parse_ecfr_xml(Path("data/human-readable/cfr/source_xml/title21_part211_2025-10-27.xml"))
    nodes = _flatten(parsed.root.to_dict())

    paragraph_c = next(node for node in nodes if node["nid"].endswith(".sec211_67.pc"))
    assert paragraph_c["kind"] == "paragraph"
    assert paragraph_c["kind_raw"] == "(c)"
    assert "Records shall be kept" in paragraph_c["text"]

    misplaced = [node for node in nodes if node["nid"].endswith(".sec211_67.pb.i6.sic")]
    assert misplaced == []


def test_ecfr_part211_roman_subitems_stay_under_item() -> None:
    parsed = parse_ecfr_xml(Path("data/human-readable/cfr/source_xml/title21_part211_2025-10-27.xml"))
    nodes = _flatten(parsed.root.to_dict())

    subitem_i = next(node for node in nodes if node["nid"].endswith(".sec211_42.pc.i10.sii"))
    subitem_vi = next(node for node in nodes if node["nid"].endswith(".sec211_42.pc.i10.sivi"))
    assert subitem_i["kind"] == "subitem"
    assert subitem_i["kind_raw"] == "(i)"
    assert subitem_vi["kind"] == "subitem"
    assert subitem_vi["kind_raw"] == "(vi)"


def test_ecfr_part211_section_xref_is_informative_note() -> None:
    parsed = parse_ecfr_xml(Path("data/human-readable/cfr/source_xml/title21_part211_2025-10-27.xml"))
    nodes = _flatten(parsed.root.to_dict())

    note = next(
        node
        for node in nodes
        if node["kind"] == "note" and node.get("kind_raw") == "XREF" and "89 FR 51769" in (node.get("text") or "")
    )
    assert note["role"] == "informative"
    assert note["normativity"] is None
    assert ".sec211_1." in note["nid"]
