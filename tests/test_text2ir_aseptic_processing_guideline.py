from __future__ import annotations

from collections import Counter
from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


SOURCE = Path("data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_pmda_aseptic_processing_guideline_v1.yaml")


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def test_aseptic_profile_drops_front_matter_and_toc_duplicates() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_aseptic_processing_guideline_trial",
        parser_profile=profile,
    )
    verify_document(ir_doc.to_dict())

    root_chapters = [node for node in ir_doc.content.children if node.kind == "chapter"]
    root_nums = [node.num for node in root_chapters]
    counts = Counter(root_nums)

    assert root_nums[:3] == ["1", "2", "3"]
    assert counts["1"] == 1
    assert counts["20"] == 1
    assert not qualitycheck_document(ir_doc.content)


def test_aseptic_profile_keeps_main_and_reference_sections_separate() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_aseptic_processing_guideline_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    by_kind_num = {(node.kind, node.num): node for node in nodes}

    assert by_kind_num[("chapter", "3")].heading == "品質システム"
    assert by_kind_num[("section", "3.1")].heading == "品質システム一般要求事項"
    assert by_kind_num[("section", "3.1")].text.startswith("1） 全般")
    assert by_kind_num[("chapter", "A1")].heading == "細胞培養／発酵により製造する原薬"
    assert by_kind_num[("paragraph", "A1.1")].text.startswith("一般要件")


def test_aseptic_processing_table_adapter_separates_known_table_candidates() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_pmda_aseptic_processing_guideline_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    by_nid = {node.nid: node for node in nodes}

    table1 = by_nid["cha7.sec7_1.tbl1"]
    table2 = by_nid["cha11.sec11_3.tbl2"]
    table3 = by_nid["cha11.sec11_3.tbl3"]
    table1_rows = [child for child in table1.children[0].children if child.kind == "table_row"]
    table2_rows = [child for child in table2.children[0].children if child.kind == "table_row"]
    table3_rows = [child for child in table3.children[0].children if child.kind == "table_row"]

    assert "postprocess=aseptic_processing_tables" in ir_doc.content.tags
    assert by_nid["cha7.sec7_1"].heading == "清浄度レベルによる作業所の分類"
    assert by_nid["cha7.sec7_1.p7_1_1"].text.startswith("重要区域（グレード A）")
    assert by_nid["cha11.sec11_3"].heading == "環境モニタリング判定基準例"
    assert [child.nid for child in by_nid["cha7.sec7_1"].children][:2] == [
        "cha7.sec7_1.tbl1",
        "cha7.sec7_1.p7_1_1",
    ]
    assert "cha7.sec7_1.not1" not in by_nid
    assert table1.heading == "表１ 清浄区域の分類"
    assert table2.heading == "表２ 微生物管理に係る環境モニタリングの頻度"
    assert table3.heading == "表 3 環境微生物の許容基準(作業時) 注）1"
    assert table1.data["column_reconstruction"] == "visual_reviewed"
    assert table2.data["column_reconstruction"] == "visual_reviewed"
    assert table3.data["column_reconstruction"] == "visual_reviewed"
    assert table1.data["column_reconstruction_status"] == "complete_for_reviewed_tables"
    assert table2.data["column_reconstruction_status"] == "complete_for_reviewed_tables"
    assert table3.data["column_reconstruction_status"] == "complete_for_reviewed_tables"
    assert table1.data["record_review"]["candidate_granularity"] == "visual_reconstructed_table_row"
    assert table2.data["record_review"]["table_row_promotion"] == "promoted"
    assert table3.data["record_review"]["note_handling"] == "table notes kept as note nodes; note-to-cell links deferred"
    assert table1.data["columns"] == [
        "area_group",
        "area_name",
        "cleanliness_level",
        "non_operational_0_5um",
        "non_operational_5_0um",
        "operational_0_5um",
        "operational_5_0um",
    ]
    assert table1.data["column_labels"][3] == "最大許容微粒子数（個／m3） 非作業時 ≧0.5μm"
    assert table1.data["header_structure"]["spanning_headers"][0]["label"] == "名称"
    assert table1.data["header_structure"]["spanning_headers"][1]["label"] == "最大許容微粒子数（個／m3）"
    assert table2.data["columns"] == [
        "grade",
        "area_condition",
        "airborne_particles",
        "airborne_microorganisms",
        "surface_attached_equipment_walls",
        "surface_attached_gloves_garment",
    ]
    assert table2.data["header_structure"]["spanning_headers"][0]["label"] == "表面付着微生物"
    assert table3.data["columns"] == [
        "grade",
        "airborne_microorganisms_cfu_m3",
        "settle_plate_cfu_plate",
        "contact_plate_cfu_24_30cm2",
        "gloves_cfu_5_fingers",
    ]
    assert table3.data["header_structure"]["spanning_headers"][0]["label"] == "空中微生物"
    assert table3.data["header_structure"]["spanning_headers"][1]["label"] == "表面付着微生物"
    assert len(table1_rows) == 4
    assert len(table2_rows) == 4
    assert len(table3_rows) == 4
    assert table1.children[0].text.startswith("名称 区分 | 名称 区域")
    assert table2.children[0].text.startswith("グレード | 区域 | 空中浮遊微粒子")
    assert table3.children[0].text.startswith("グレード | 空中微生物 浮遊菌")
    assert table1_rows[0].data["record_id"] == "aseptic_table1.r1"
    assert table2_rows[2].data["record_id"] == "aseptic_table2.r3"
    assert table1_rows[0].data["cells"] == [
        "無菌操作区域",
        "重要区域",
        "グレード A (ISO 5)",
        "3,520",
        "20",
        "3,520",
        "20",
    ]
    assert table2_rows[2].data["cells"] == [
        "C，D",
        "製品や容器が環境に曝露される区域",
        "月1回",
        "週2回",
        "週2回",
        "----",
    ]
    assert table3_rows[-1].data["cells"] == ["D", "200", "100", "50", "----"]
    assert table1_rows[-1].text == "その他の支援区域 |  | グレード D | 3,520,000 | 29,000 | 作業形態による注2） | 作業形態による注2）"
    assert table2_rows[-1].text == "C，D | その他の区域 | 月1回 | 週1回 | 週1回 | ----"
    assert table3_rows[-1].text == "D | 200 | 100 | 50 | ----"
    assert "表１ 清浄区域の分類" not in (by_nid["cha7.sec7_1"].text or "")
    assert "表２ 微生物管理に係る環境モニタリングの頻度" not in (by_nid["cha11.sec11_3"].text or "")
    assert "cha11.sec11_3.pre1" not in by_nid
    assert not qualitycheck_document(ir_doc.content)
