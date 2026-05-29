from __future__ import annotations

from collections import Counter
from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


SOURCE = Path("data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_pmda_api_gmp_guideline_v1.yaml")


def _flatten(node):
    yield node
    for child in node.children:
        yield from _flatten(child)


def test_api_gmp_profile_drops_notice_and_toc_duplicates() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_api_gmp_guideline_20011102",
        parser_profile=profile,
    )
    ir = ir_doc.to_dict()
    verify_document(ir)

    root_children = ir_doc.content.children
    root_chapter_nums = [node.num for node in root_children if node.kind == "chapter"]
    counts = Counter(root_chapter_nums)

    assert root_chapter_nums[:3] == ["1", "2", "3"]
    assert counts["1"] == 1
    assert counts["2"] == 1
    assert counts["19"] == 1
    assert not qualitycheck_document(ir_doc.content)


def test_api_gmp_profile_keeps_deep_sections_under_chapters() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_api_gmp_guideline_20011102",
        parser_profile=profile,
    )
    nodes = list(_flatten(ir_doc.content))
    by_num = {(node.kind, node.num): node for node in nodes}

    assert by_num[("chapter", "3")].heading == "従業員"
    assert by_num[("section", "3.1")].heading == "従業員の適格性"
    assert by_num[("section", "3.1")].text is None
    assert by_num[("paragraph", "3.10")].text.startswith("中間体・原薬の生産を実施し監督するため")
    assert by_num[("paragraph", "3.10")].nid.startswith(by_num[("section", "3.1")].nid)
    assert by_num[("section", "3.2")].heading == "従業員の衛生"


def test_api_gmp_section_heading_with_chapeau_keeps_text_and_table_context() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_api_gmp_guideline_20011102",
        parser_profile=profile,
    )
    nodes = list(_flatten(ir_doc.content))
    by_num = {(node.kind, node.num): node for node in nodes}

    section_1_3 = by_num[("section", "1.3")]
    assert section_1_3.heading == "適用範囲"
    assert section_1_3.text.startswith("本ガイドラインは、ヒト用医薬品に使用する原薬に適用する。")

    table_1 = next(child for child in section_1_3.children if child.kind == "table" and child.num == "1")
    assert table_1.heading == "表１：原薬生産に対する本ガイドラインの適用"


def test_api_gmp_table1_adapter_keeps_raw_rows_without_manual_input_rewrite() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_api_gmp_guideline_20011102",
        parser_profile=profile,
    )
    nodes = list(_flatten(ir_doc.content))
    section_1_3 = next(node for node in nodes if node.kind == "section" and node.num == "1.3")
    table_1 = next(child for child in section_1_3.children if child.kind == "table" and child.num == "1")
    header = next(child for child in table_1.children if child.kind == "table_header")
    rows = [child for child in header.children if child.kind == "table_row"]

    assert "postprocess=api_gmp_table1" in ir_doc.content.tags
    assert table_1.heading == "表１：原薬生産に対する本ガイドラインの適用"
    assert table_1.data["parser"] == "api_gmp_table1_adapter"
    assert table_1.data["column_reconstruction"] == "prototype"
    assert table_1.data["column_reconstruction_status"] == "partial"
    assert table_1.data["reconstructed_columns"] == [
        "production_type",
        "early_stage_1",
        "early_stage_2",
        "middle_stage",
        "late_stage",
        "final_stage",
    ]
    assert len(table_1.data["reconstructed_records"]) == 7
    assert table_1.data["record_review"]["candidate_granularity"] == "reconstructed_record"
    assert table_1.data["record_review"]["table_row_promotion"] == "deferred"
    assert table_1.data["record_review"]["deferred_raw_rows"] == [1, 2, 26]
    assert table_1.data["reconstructed_records"][0]["review_status"] == "reviewed_candidate"
    assert table_1.data["reconstructed_records"][0]["promotion_status"] == "deferred"
    assert table_1.data["reconstructed_records"][0]["cells"] == [
        "化学的合成による原薬",
        "原薬出発物質の製造",
        "原薬出発物質の工程への導入",
        "中間体の製造",
        "分離及び精製",
        "物理的加工処理及び包装",
    ]
    assert header.text == "raw_line"
    assert header.data["columns"] == ["raw_line"]
    assert len(rows) == 26
    assert rows[0].text == "生産形態                  形態ごとの生産工程の事例"
    assert rows[2].data["column_reconstruction_record_id"] == "api_gmp_table1.r1"
    assert rows[25].data["column_reconstruction_warning"] == "non_data_row_not_cell_reconstructed"
    assert rows[-1].text == "ＧＭＰ要求事項の増大"
    assert "表１：原薬生産に対する本ガイドラインの適用" not in (section_1_3.text or "")
    assert not qualitycheck_document(ir_doc.content)
