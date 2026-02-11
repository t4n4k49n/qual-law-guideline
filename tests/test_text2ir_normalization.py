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


def test_prose_unwrap_and_paragraph_break(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "§ 11.1 Scope.",
            "(a) This is a",
            "wrapped line.",
            "",
            "New paragraph starts here.",
        ]
    )
    input_path = tmp_path / "wrap_paragraph.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")

    profile = load_parser_profile(family="US_CFR")
    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="wrap_paragraph_check",
        parser_profile=profile,
    ).to_dict()
    nodes = _flatten(ir["content"])
    pa = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "a")
    assert pa.get("text") == "This is a wrapped line.\n\nNew paragraph starts here."


def test_hyphenation_repair_drop_and_keep(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "§ 11.10 Controls for closed systems.",
            "(a) elec-",
            "tronic records and compo-",
            "nents are reviewed with time-",
            "stamped audit trails.",
            "(b) electronic components remain available.",
            "(c) time-stamped logs are retained.",
        ]
    )
    input_path = tmp_path / "hyphen_repair.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")

    profile = load_parser_profile(family="US_CFR")
    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="hyphen_repair_check",
        parser_profile=profile,
    ).to_dict()
    nodes = _flatten(ir["content"])
    pa = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "a")
    text_a = pa.get("text") or ""
    assert "electronic" in text_a
    assert "components" in text_a
    assert "time-stamped" in text_a
    assert "elec- tronic" not in text_a
    assert "compo- nents" not in text_a


def test_preformatted_block_keeps_newlines_and_indent(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "§ 11.11 Sample.",
            "(a) Intro text.",
            "    col1   col2",
            "    1      2",
            "Continuation after table.",
        ]
    )
    input_path = tmp_path / "preformatted_keep.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")

    profile = load_parser_profile(family="US_CFR")
    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="preformatted_keep_check",
        parser_profile=profile,
    ).to_dict()
    nodes = _flatten(ir["content"])
    pa = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "a")
    text_a = pa.get("text") or ""
    assert "    col1   col2\n    1      2" in text_a


def test_integration_cfr_style_wrap_hyphen_fix(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "§ 11.10 Controls for closed systems.",
            "(e) Use of secure, computer-gen-",
            "erated, time-stamped audit trails to independently record actions.",
            "§ 11.70 Signature/record linking.",
            "(a) Electronic signatures and hand-",
            "written signatures executed to elec-",
            "tronic records shall be linked.",
        ]
    )
    input_path = tmp_path / "cfr_wrap_hyphen_integration.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")

    profile = load_parser_profile(family="US_CFR")
    ir = parse_text_to_ir(
        input_path=input_path,
        doc_id="cfr_wrap_hyphen_integration",
        parser_profile=profile,
    ).to_dict()
    nodes = _flatten(ir["content"])
    all_text = "\n".join((n.get("text") or "") for n in nodes)
    assert "computer-generated" in all_text
    assert "time-stamped" in all_text
    assert "handwritten" in all_text
    assert "electronic" in all_text
    assert "gen- erated" not in all_text
    assert "hand- written" not in all_text
    assert "elec- tronic" not in all_text
