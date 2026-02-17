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


def test_chapter_heading_wrap_is_merged_into_heading() -> None:
    input_path = Path("tests/fixtures/who_heading_wrap_chapter.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_heading_wrap_chapter",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    nodes = _flatten(ir_dict["content"])
    chapter = next(n for n in nodes if n["kind"] == "chapter" and n.get("num") == "2")
    assert chapter.get("heading") == "Microbiological risk assessment"
    assert (chapter.get("text") or "").startswith(
        "The backbone of the practice of biosafety is risk assessment."
    )


def test_annex_heading_wrap_from_noisy_marker_line_is_merged_into_heading() -> None:
    input_path = Path("tests/fixtures/who_heading_wrap_annex.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_heading_wrap_annex",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    nodes = _flatten(ir_dict["content"])
    annex = next(n for n in nodes if n["kind"] == "annex" and n.get("num") == "4")
    assert annex.get("heading") == "Negative-pressure flexible-film isolators"
    assert (annex.get("text") or "").startswith("The negative-pressure, flexible-film isolator is")


def test_annex_marker_line_with_title_on_next_line_is_merged_into_heading(tmp_path: Path) -> None:
    text = "\n".join(
        [
            "ANNEX 2",
            "Immunization of staff",
            "The risks of working with particular agents...",
        ]
    )
    input_path = tmp_path / "who_heading_wrap_annex_marker_title.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_heading_wrap_annex_marker_title",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    nodes = _flatten(ir_dict["content"])
    annex = next(n for n in nodes if n["kind"] == "annex" and n.get("num") == "2")
    assert annex.get("heading") == "Immunization of staff"
    assert (annex.get("text") or "").startswith("The risks of working with particular agents...")


def test_mid_sentence_annex_reference_is_preserved_without_false_annex_split() -> None:
    input_path = Path("tests/fixtures/who_annex_mid_sentence_ref.txt")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml")
    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_annex_mid_sentence_ref",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    root = ir_dict["content"]
    nodes = _flatten(root)

    chapter_11 = next(n for n in nodes if n["kind"] == "chapter" and n.get("num") == "11")
    assert "presented in Annex 4." in (chapter_11.get("text") or "")
    assert "Negative-pressure flexible-film isolators" in (chapter_11.get("text") or "")

    annex_4 = [n for n in root.get("children", []) if n["kind"] == "annex" and n.get("num") == "4"]
    assert len(annex_4) == 1
    assert annex_4[0].get("heading") == "Equipment safety"
    assert "Certain items of equipment may create microbiological hazards" in (
        annex_4[0].get("text") or ""
    )
