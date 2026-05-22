from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import yaml

from qai_mock_ui.candidate_visibility import build_candidate_visibility_map
from qai_mock_ui.ir_model import build_doc_index
from qai_text2ir.cli import _build_regdoc_profile
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


def test_table5_form_artifact_is_hidden_and_summarized(tmp_path: Path) -> None:
    checkbox = "\uEC1E"
    text = "\n".join(
        [
            "8. Safety checklist examples",
            "5. Proper procedures for general laboratory safety are required. Examples of such tools are provided in Table 5.",
            "",
            "Table 5. Basic Laboratory - Biosafety Level 1: laboratory safety survey",
            "Location ○ ○ ○ ○ ○",
            "Date ○ ○ ○ ○ ○",
            "CHECKED ITEM (ENTER DATE OF CHECK) YES NO N/A COMMENTS",
            f"Information on sign accurate and current .............................................. {checkbox} {checkbox} {checkbox}",
            f"Sign legible and not defaced ............. {checkbox} {checkbox} {checkbox}",
            "",
            "Laboratory biosecurity",
            "Normal prose continues here.",
        ]
    )
    input_path = tmp_path / "who_lbm_table5_fixture.txt"
    input_path.write_text(text, encoding="utf-8", newline="\n")
    parser_profile = _load_profile("src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml")

    ir_doc = parse_text_to_ir(
        input_path=input_path,
        doc_id="who_lbm_table5_fixture",
        parser_profile=parser_profile,
    )
    ir_dict = ir_doc.to_dict()
    verify_document(ir_dict)
    nodes = _flatten(ir_dict["content"])
    artifact_nodes = [
        n for n in nodes
        if n.get("kind_raw") == "form_artifact" or "form_artifact" in (n.get("tags") or [])
    ]
    visible_nodes = [
        n for n in nodes
        if not (n.get("kind_raw") == "form_artifact" or "not_selectable" in (n.get("tags") or []))
    ]
    visible_text = "\n".join((n.get("heading") or "") + "\n" + (n.get("text") or "") for n in visible_nodes)

    assert artifact_nodes
    assert "Proper procedures for general laboratory safety" in visible_text
    assert "Laboratory biosecurity" in visible_text
    assert "Information on sign accurate and current" not in visible_text
    assert "Sign legible and not defaced" not in visible_text
    assert "CHECKED ITEM" not in visible_text
    assert f"{checkbox}" not in yaml.safe_dump(ir_dict, allow_unicode=True)
    assert all(len(n.get("text") or "") <= 300 for n in artifact_nodes)
    assert all("[ ] [ ] [ ]" not in (n.get("text") or "") for n in artifact_nodes)

    index = build_doc_index(ir_dict)
    purpose = _build_regdoc_profile("who_lbm_table5_fixture")["profiles"]["dq_gmp_checklist"]
    visibility = build_candidate_visibility_map(index, purpose)
    for artifact in artifact_nodes:
        assert visibility[artifact["nid"]] is False
