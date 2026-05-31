from __future__ import annotations

from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir


SOURCE = Path("data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_annex_v1.yaml")


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def test_niid_annex_cell_reconstruction_v1_keeps_raw_rows_and_splits_safe_rows() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_annex_trial",
        parser_profile=profile,
    )
    tables = {
        table.data["annex_num"]: table
        for table in _walk(ir_doc.content)
        if table.kind == "table" and table.data.get("parser") == "niid_annex_table_adapter"
    }

    assert tables["付表2"].data["cell_reconstructed_rows"] == 4
    assert tables["付表2"].data["cell_deferred_rows"] == 0
    assert tables["付表4"].data["cell_reconstructed_rows"] == 4
    assert tables["別表7"].data["cell_reconstructed_rows"] == 18
    assert tables["別表10"].data["cell_reconstructed_rows"] == 13

    fuhyo4_rows = tables["付表4"].children[0].children
    assert fuhyo4_rows[0].data["record"]["absl"] == "1"
    assert "通常の動物実験の条件" in fuhyo4_rows[0].data["record"]["laboratory_practice"]
    assert fuhyo4_rows[0].data["cell_reconstruction"] == "visual_reviewed_cells"
    assert tables["付表4"].data["raw_table_audit"]["fixed_width_cell_deferred_rows"] == 19


def test_niid_annex_readiness_decisions_cover_all_annexes() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_annex_trial",
        parser_profile=profile,
    )
    annexes = [node for node in ir_doc.content.children if node.kind == "annex"]
    decisions = {annex.num: annex.data.get("normalization_readiness", {}) for annex in annexes}

    assert len(decisions) == 16
    assert all(decision.get("status") == "ready_for_readiness_review" for decision in decisions.values())
    assert decisions["付表2"]["decision"] == "promotion_candidate_as_visual_reviewed_table"
    assert decisions["付表3"]["decision"] == "promotion_candidate_as_visual_reviewed_table"
    assert decisions["別表4"]["decision"] == "promotion_candidate_as_visual_reviewed_table"
    assert decisions["別表5"]["decision"] == "promotion_candidate_as_visual_reviewed_table"
    assert decisions["別表8"]["decision"] == "promotion_candidate_as_visual_reviewed_table"
    assert decisions["別表2"]["promotion_mode"] == "annex_text"
