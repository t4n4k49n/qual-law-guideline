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


def test_api_gmp_table1_adapter_promotes_visual_reviewed_cells() -> None:
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
    assert table_1.data["column_reconstruction"] == "visual_reviewed"
    assert table_1.data["column_reconstruction_status"] == "complete_for_table1"
    assert table_1.data["columns"] == [
        "production_type",
        "api_starting_material_manufacture",
        "api_starting_material_introduction_or_preliminary_processing",
        "intermediate_manufacture_or_equivalent",
        "isolation_and_purification_or_further_extraction",
        "physical_processing_and_packaging",
    ]
    assert len(table_1.data["reconstructed_records"]) == 7
    assert table_1.data["record_review"]["candidate_granularity"] == "visual_reconstructed_table_row"
    assert table_1.data["record_review"]["table_row_promotion"] == "promoted"
    assert table_1.data["record_review"]["deferred_raw_rows"] == []
    assert table_1.data["reconstructed_records"][0]["cells"] == [
        "化学的合成による原薬",
        "原薬出発物質の製造",
        "原薬出発物質の工程への導入",
        "中間体の製造",
        "分離及び精製",
        "物理的加工処理及び包装",
    ]
    assert table_1.data["reconstructed_records"][0]["guideline_applicable"] == [False, True, True, True, True]
    assert table_1.data["visual_notes"][0]["meaning"] == "guideline_applicable=true"
    assert header.text.startswith("生産形態 | 原薬出発物質の製造")
    assert header.data["columns"] == table_1.data["columns"]
    assert len(rows) == 7
    assert rows[0].data["record_id"] == "api_gmp_table1.r1"
    assert rows[0].data["cells"] == table_1.data["reconstructed_records"][0]["cells"]
    assert rows[0].data["guideline_applicable"] == [False, True, True, True, True]
    assert rows[0].data["visual_fill"] == ["not_applicable", "white", "gray", "gray", "gray", "gray"]
    assert rows[3].data["cells"] == [
        "原薬として使用する生薬抽出物",
        "植物の収集",
        "細断及び初期抽出",
        "",
        "再抽出",
        "物理的加工処理及び包装",
    ]
    assert rows[3].data["guideline_applicable"] == [False, False, False, True, True]
    assert rows[4].data["guideline_applicable"] == [False, False, False, False, True]
    assert rows[-1].data["record_id"] == "api_gmp_table1.r7"
    assert rows[-1].data["guideline_applicable"] == [False, True, True, True, True]
    assert "表１：原薬生産に対する本ガイドラインの適用" not in (section_1_3.text or "")
    assert not qualitycheck_document(ir_doc.content)
