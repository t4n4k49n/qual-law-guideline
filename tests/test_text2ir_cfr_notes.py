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


def test_cfr_note_lines_are_split_under_section(tmp_path: Path) -> None:
    fixture = Path("tests/fixtures/CFR_PART11_with_notes.txt")
    input_path = tmp_path / fixture.name
    input_path.write_text(fixture.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")

    profile = load_parser_profile(profile_id="us_cfr_default_v1")
    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="us_cfr_note_check",
        parser_profile=profile,
    ).to_dict()

    nodes = _flatten(ir["content"])
    notes = [n for n in nodes if n["kind"] == "note"]
    assert len(notes) == 3

    note_texts = [n.get("text") for n in notes]
    assert any(text and text.startswith("[62 FR") for text in note_texts)
    assert any(text and text.startswith("Authority:") for text in note_texts)
    assert any(text and text.startswith("Source:") for text in note_texts)

    for note in notes:
        assert note["role"] == "informative"
        assert note["normativity"] is None
        assert ".sec11_10." in note["nid"]

    subitem = next(n for n in nodes if n["kind"] == "subitem")
    assert "[62 FR" not in (subitem.get("text") or "")
    assert "Authority:" not in (subitem.get("text") or "")
    assert "Source:" not in (subitem.get("text") or "")
