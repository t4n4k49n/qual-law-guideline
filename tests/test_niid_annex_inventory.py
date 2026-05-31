from __future__ import annotations

from pathlib import Path

from qai_text2ir.niid_annex_inventory import build_niid_annex_inventory
from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


SOURCE = Path("data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_annex_v1.yaml")


def _inventory():
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_annex_inventory_trial",
        parser_profile=profile,
    )
    return build_niid_annex_inventory(ir_doc.content)


def test_niid_annex_inventory_classifies_all_annexes() -> None:
    inventory = _inventory()
    by_num = {item.num: item for item in inventory}

    assert list(by_num) == [
        "別表1",
        "付表1-1",
        "付表1-2",
        "付表1-3",
        "付表2",
        "付表3",
        "付表4",
        "別表2",
        "別表3",
        "別表4",
        "別表5",
        "別表6",
        "別表7",
        "別表8",
        "別表9",
        "別表10",
    ]
    assert len(inventory) == 16


def test_niid_annex_inventory_marks_column_restoration_candidates() -> None:
    by_num = {item.num: item for item in _inventory()}

    assert by_num["付表2"].column_restoration == "candidate"
    assert by_num["付表3"].column_restoration == "candidate"
    assert by_num["付表4"].column_restoration == "candidate"
    assert by_num["別表4"].column_restoration == "candidate_complex"
    assert by_num["別表5"].column_restoration == "candidate_complex"
    assert by_num["別表7"].column_restoration == "candidate"
    assert by_num["別表8"].column_restoration == "candidate_complex"
    assert by_num["別表10"].column_restoration == "candidate"

    assert by_num["別表6"].column_restoration == "not_applicable"
    assert by_num["別表9"].structure_type == "numbered_requirements"
    assert by_num["別表8"].subitem_count == 0
