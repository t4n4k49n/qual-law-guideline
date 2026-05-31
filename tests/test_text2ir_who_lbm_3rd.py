from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


def _flatten(node: Dict) -> List[Dict]:
    out = [node]
    for child in node.get("children", []):
        out.extend(_flatten(child))
    return out


def _load_profile(path: str) -> Dict:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8"))


def test_strip_inline_page_tokens_and_header(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "LABORATORY BIOSAFETY MANUAL",
            "1. General principles",
            "Introduction",
            "microorganisms, by risk group, taking into account:• 2 •",
            "LABORATORY BIOSAFETY MANUAL",
            "1. Pathogenicity of the organism.",
            "2. Mode of transmission and host range of organisms. These may be influenced",
            "• 2 •",
        ]
    )
    input_path = tmp_path / "who_lbm_fixture_1.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_fixture_1",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    verify_document(ir_dict)
    nodes = _flatten(ir_dict["content"])

    joined_text = "\n".join((n.get("text") or "") for n in nodes)
    joined_heading = "\n".join((n.get("heading") or "") for n in nodes)
    assert "LABORATORY BIOSAFETY MANUAL" not in joined_text
    assert "LABORATORY BIOSAFETY MANUAL" not in joined_heading
    assert "• 2 •" not in joined_text
    assert "• 2 •" not in joined_heading

    chapter = next(n for n in nodes if n["kind"] == "chapter" and n.get("num") == "1")
    item_1 = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "1")
    item_2 = next(n for n in nodes if n["kind"] == "item" and n.get("num") == "2")
    assert chapter.get("heading") == "General principles"
    assert item_1["nid"].startswith(chapter["nid"])
    assert item_2["nid"].startswith(chapter["nid"])


def test_qualitycheck_no_single_newline_in_prose_for_fixture(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "1. General principles",
            "1. Pathogenicity of the organism.",
            "2. Mode of transmission and host range of organisms. These may be influenced",
            "by environmental factors and by the stability of the organism in the environment.",
            "Awareness of potential hazards is key to the prevention of laboratory-",
            "",
            "acquired infections and accidents.",
            "• Operating procedures should be available for all activities.",
        ]
    )
    input_path = tmp_path / "who_lbm_fixture_2.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_fixture_2",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    nodes = _flatten(ir_dict["content"])
    joined = "\n".join((n.get("text") or "") for n in nodes)
    assert "laboratory-acquired" in joined
    warnings = qualitycheck_document(ir_doc.content)
    assert not any("single newline remains in prose" in w for w in warnings)
    assert not any("unresolved hyphen-space pattern remains" in w for w in warnings)


def test_profile_loader_defaults_to_who_lbm_v4() -> None:
    profile = load_parser_profile(family="WHO_LBM")
    assert profile["id"] == "who_lbm_3rd_default_v4"


def test_who_lbm_v4_unnumbered_headings_are_sections() -> None:
    ir_doc = parse_text_to_ir(
        input_path=Path("data/human-readable/who/WHO_LBM_3rd.txt"),
        doc_id="who_lbm_3rd_2004_9241546506",
        parser_profile=_load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml"),
    )
    ir_dict = ir_doc.to_dict()
    nodes = _flatten(ir_dict["content"])
    by_nid = {node["nid"]: node for node in nodes}

    chapter3 = by_nid["cha3"]
    sections = [child for child in chapter3["children"] if child["kind"] == "section"]
    headings = [section["heading"] for section in sections]

    assert "Code of practice" in headings
    assert "Access" in headings
    assert "Personal protection" in headings
    assert "Laboratory design and facilities" in headings

    access = next(section for section in sections if section["heading"] == "Access")
    access_items = [child for child in access["children"] if child["kind"] == "item"]
    assert access_items[0]["text"].startswith("The international biohazard warning symbol")
    assert access_items[-1]["text"] == "No animals should be admitted other than those involved in the work of the laboratory."
    assert "Access Personal protection Procedures" not in (chapter3.get("text") or "")


def test_who_lbm_v4_preserves_title_phrase_inside_prose() -> None:
    ir_doc = parse_text_to_ir(
        input_path=Path("data/human-readable/who/WHO_LBM_3rd.txt"),
        doc_id="who_lbm_3rd_2004_9241546506",
        parser_profile=_load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml"),
    )
    ir_dict = ir_doc.to_dict()
    nodes = _flatten(ir_dict["content"])
    chapter9 = next(node for node in nodes if node["kind"] == "chapter" and node.get("num") == "9")

    assert (chapter9.get("text") or "").startswith("The Laboratory biosafety manual has in the past focused")
    assert "The  has in the past focused" not in (chapter9.get("text") or "")


def test_drop_toc_entries_dont_create_chapters(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "Contents",
            "1. General principles                                             1",
            "2. Microbiological risk assessment                               7",
            "Annex 1 First aid                                                138",
            "Foreword vii",
            "Index 170",
            "1. General principles",
            "Introduction",
            "Throughout this manual, ...",
            "Annex 1",
            "First aid",
            "This annex describes ...",
        ]
    )
    input_path = tmp_path / "who_lbm_fixture_toc.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_fixture_toc",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    nodes = _flatten(ir_dict["content"])

    chapters_1 = [n for n in nodes if n["kind"] == "chapter" and n.get("num") == "1"]
    annexes_1 = [n for n in nodes if n["kind"] == "annex" and n.get("num") == "1"]
    assert len(chapters_1) == 1
    assert len(annexes_1) == 1
    assert chapters_1[0].get("heading") == "General principles"


def test_drop_repeated_running_headers_inside_chapter(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "10. BIOLOGICAL SAFETY CABINETS",
            "Some paragraph...",
            "Another paragraph...",
            "10. BIOLOGICAL SAFETY CABINETS",
            "More paragraph...",
        ]
    )
    input_path = tmp_path / "who_lbm_fixture_running_header.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_fixture_running_header",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    nodes = _flatten(ir_dict["content"])

    chapters_10 = [n for n in nodes if n["kind"] == "chapter" and n.get("num") == "10"]
    chapter_10_items = [n for n in nodes if n["kind"] == "item" and n.get("num") == "10"]
    assert len(chapters_10) == 1
    assert not chapter_10_items
