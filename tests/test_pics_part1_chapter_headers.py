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


def test_chapter1_heading_is_merged_from_next_line() -> None:
    input_path = Path("tests/fixtures/pics_part1_chapter1_heading_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_part1_default_v2.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_part1_chapter1_heading_fixture",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    root = ir_dict["content"]
    chapters = [n for n in root.get("children", []) if n["kind"] == "chapter" and n.get("num") == "1"]
    assert len(chapters) == 1
    chapter = chapters[0]
    assert chapter.get("heading") == "PHARMACEUTICAL QUALITY SYSTEM"
    nodes = _flatten(root)
    paragraph_11 = next(n for n in nodes if n["kind"] == "paragraph" and n.get("num") == "1.1")
    assert "Manufacturing Authorisation" in (paragraph_11.get("text") or "")


def test_running_header_chapter1_is_dropped_without_duplicate_chapter() -> None:
    input_path = Path("tests/fixtures/pics_part1_chapter1_running_header_fixture.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/pics_part1_default_v2.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="pics_part1_chapter1_running_header_fixture",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    root = ir_dict["content"]
    chapters = [n for n in root.get("children", []) if n["kind"] == "chapter" and n.get("num") == "1"]
    assert len(chapters) == 1
    chapter = chapters[0]
    chapter_text = chapter.get("text") or ""
    assert "Chapter 1 Pharmaceutical Quality System" not in chapter_text

    nodes = _flatten(root)
    paragraph_nums = [n.get("num") for n in nodes if n["kind"] == "paragraph"]
    assert "1.1" in paragraph_nums
    assert "1.2" in paragraph_nums
