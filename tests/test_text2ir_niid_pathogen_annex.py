from __future__ import annotations

from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


SOURCE = Path("data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_annex_v1.yaml")


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def test_niid_annex_profile_keeps_all_betsuhyo_and_fuhyo_markers() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_annex_trial",
        parser_profile=profile,
    )
    verify_document(ir_doc.to_dict())

    annexes = [node for node in ir_doc.content.children if node.kind == "annex"]
    annex_nums = [node.num for node in annexes]

    assert annex_nums == [
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
    assert not qualitycheck_document(ir_doc.content)


def test_niid_annex_profile_preserves_annex_text_without_body_chapters() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_annex_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    annex_by_num = {node.num: node for node in ir_doc.content.children if node.kind == "annex"}
    all_text = "\n".join(str(part) for node in nodes for part in (node.heading, node.text) if part)

    assert [node.kind for node in ir_doc.content.children] == ["annex"] * 16
    assert "第１章" not in all_text
    assert annex_by_num["別表1"].heading is None
    assert annex_by_num["別表1"].text.startswith("病原体等の取扱いにおいては")
    assert "における該当部分" in all_text
    assert "特定病原体等の取扱いに必要な教育訓練" in all_text


def test_niid_annex_table_adapter_creates_raw_row_tables_for_selected_annexes() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_annex_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    by_num = {node.num: node for node in ir_doc.content.children if node.kind == "annex"}
    tables = [node for node in nodes if node.kind == "table" and node.data.get("parser") == "niid_annex_table_adapter"]

    assert "postprocess=niid_annex_tables" in ir_doc.content.tags
    assert [table.data["annex_num"] for table in tables] == [
        "付表2",
        "付表3",
        "付表4",
        "別表4",
        "別表5",
        "別表7",
        "別表8",
        "別表10",
    ]
    assert len(tables) == 8
    assert by_num["付表2"].heading == "病原体等のリスク群分類と、実験室のＢＳＬ分類、実験室使用目的、実験手技及び安全機器との関連性"
    assert by_num["付表2"].text.startswith("病原体等の取り扱う実験室は")
    assert by_num["付表3"].text is None
    assert by_num["付表2"].data["normalization_readiness"]["decision"] == "promotion_candidate_as_visual_reviewed_table"
    assert by_num["別表4"].data["normalization_readiness"]["decision"] == "promotion_candidate_as_visual_reviewed_table"

    fuhyo3_table = next(table for table in tables if table.data["annex_num"] == "付表3")
    betsu7_table = next(table for table in tables if table.data["annex_num"] == "別表7")
    betsu10_table = next(table for table in tables if table.data["annex_num"] == "別表10")
    fuhyo3_rows = [row for row in fuhyo3_table.children[0].children if row.kind == "table_row"]
    betsu7_rows = [row for row in betsu7_table.children[0].children if row.kind == "table_row"]
    betsu10_rows = [row for row in betsu10_table.children[0].children if row.kind == "table_row"]

    assert fuhyo3_table.data["column_reconstruction"] == "visual_reviewed_cells"
    assert fuhyo3_table.data["normalization_readiness"]["decision"] == "promotion_candidate_as_visual_reviewed_table"
    assert fuhyo3_table.data["reconstructed_columns"] == ["criterion", "parent_criterion", "bsl1", "bsl2", "bsl3", "bsl4"]
    assert fuhyo3_rows[0].data["record"]["criterion"] == "実験室の独立性*1"
    assert fuhyo3_rows[-1].data["record"]["criterion"] == "作業従事者の安全監視機能*8"
    assert betsu7_table.data["reconstructed_columns"] == [
        "category",
        "ordinance_item",
        "record_content",
        "pathogen_type_1",
        "pathogen_type_2",
        "pathogen_type_3",
    ]
    assert len(betsu7_rows) == 18
    assert len(betsu10_rows) == 13
    assert fuhyo3_table.data["cell_reconstruction"] == "visual_reviewed_cells"
    assert fuhyo3_table.data["cell_reconstruction_status"] == "complete"
    assert fuhyo3_table.data["cell_reconstructed_rows"] == 15
    assert fuhyo3_table.data["cell_deferred_rows"] == 0
    assert fuhyo3_rows[0].data["cells"] == ["実験室の独立性*1", "", "不要", "不要", "必要", "必要"]
    assert fuhyo3_rows[0].data["cell_reconstruction"] == "visual_reviewed_cells"
    assert fuhyo3_table.data["raw_table_audit"]["fixed_width_cell_deferred_rows"] == 6
    assert betsu7_table.data["cell_reconstructed_rows"] == 18
    assert betsu7_rows[1].data["cells"] == [
        "病原体等",
        "病原体等の受入れ又は払出しの日時",
        "事業所ごとに記帳（同上）",
        "年月日・時刻",
        "年月日",
        "年月日",
    ]
    assert betsu10_table.data["cell_reconstructed_rows"] == 13
    assert not qualitycheck_document(ir_doc.content)
