from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _load_profile(path: str) -> Dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_skip_toc_and_parse_chapters() -> None:
    input_path = Path("tests/fixtures/pics_part1_full_v3_toc_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_part1_default_v3.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_part1_full_v3_toc_fixture",
        parser_profile=parser_profile,
    )
    root = ir_doc.to_dict()["content"]
    nodes = _flatten(root)

    chapters = [n for n in root.get("children", []) if n["kind"] == "chapter"]
    assert [c.get("num") for c in chapters] == ["1", "2"]
    assert chapters[0].get("heading") == "PHARMACEUTICAL QUALITY SYSTEM"
    assert chapters[1].get("heading") == "PERSONNEL"

    chapter1_text = chapters[0].get("text") or ""
    assert "CHAPTER 1 - PHARMACEUTICAL QUALITY SYSTEM" not in chapter1_text
    assert "PE 009-17 (Part I) - 8 - 25 August 2023" not in chapter1_text
    assert "Chapter 1 Pharmaceutical Quality System" not in chapter1_text

    paragraph_nums = [n.get("num") for n in nodes if n["kind"] == "paragraph"]
    assert "1.1" in paragraph_nums
    assert "2.5" in paragraph_nums


def test_bullet_char_detected() -> None:
    input_path = Path("tests/fixtures/pics_part1_full_v3_bullet_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_part1_default_v3.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_part1_full_v3_bullet_fixture",
        parser_profile=parser_profile,
    )
    nodes = _flatten(ir_doc.to_dict()["content"])
    subitems = [n for n in nodes if n["kind"] == "subitem"]
    assert len(subitems) >= 2


def test_profile_loader_defaults_to_pics_v3() -> None:
    profile = load_parser_profile(family="PICS")
    assert profile["id"] == "pics_part1_default_v3"


def test_chapter_transition_note_attaches_to_new_chapter(tmp_path: Path) -> None:
    input_path = tmp_path / "part1_chapter_transition_note.txt"
    input_path.write_text(
        "\n".join(
            [
                "CHAPTER 6",
                "QUALITY CONTROL",
                "",
                "6.41   Where appropriate, specific requirements described in other guidelines should be",
                "       addressed for the transfer of particular testing methods.",
                "",
                " PE 009-17 (Part I)                         - 44 -                          25 August 2023",
                "                                                       Chapter 7     Outsourced activities",
                "",
                "CHAPTER 7",
                "",
                "                      OUTSOURCED ACTIVITIES",
                "",
                "PRINCIPLE",
                "       Any activity covered by the GMP Guide that is outsourced should be appropriately",
                "       defined, agreed and controlled.",
                "",
                "       Note: This Chapter deals with the responsibilities of manufacturers towards the",
                "       Competent Regulatory Authorities.",
                "",
                "GENERAL",
                "7.1    There should be a written contract covering the outsourced activities.",
            ]
        ),
        encoding="utf-8",
        newline="\n",
    )
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_part1_default_v3.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_part1_chapter_transition_note",
        parser_profile=parser_profile,
    )
    root = ir_doc.to_dict()["content"]
    nodes = _flatten(root)
    by_nid = {node["nid"]: node for node in nodes}

    assert "Chapter 7     Outsourced activities" not in (by_nid["cha6.p6_41"].get("text") or "")
    assert not by_nid["cha6.p6_41"].get("children")
    assert by_nid["cha7"]["children"][0]["kind"] == "note"
    assert by_nid["cha7"]["children"][0]["nid"] == "cha7.not1"
