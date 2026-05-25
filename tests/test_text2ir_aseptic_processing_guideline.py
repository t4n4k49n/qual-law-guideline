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
    assert by_kind_num[("paragraph", "3.1")].text.startswith("品質システム一般要求事項")
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

    table1 = by_nid["cha7.p7_1.tbl1"]
    table2 = by_nid["cha11.p11_3.tbl2"]
    table3 = by_nid["cha11.p11_3.tbl3"]
    table1_rows = [child for child in table1.children[0].children if child.kind == "table_row"]
    table2_rows = [child for child in table2.children[0].children if child.kind == "table_row"]
    table3_rows = [child for child in table3.children[0].children if child.kind == "table_row"]

    assert "postprocess=aseptic_processing_tables" in ir_doc.content.tags
    assert table1.heading == "表１ 清浄区域の分類"
    assert table2.heading == "表２ 微生物管理に係る環境モニタリングの頻度"
    assert table3.heading == "表 3 環境微生物の許容基準(作業時) 注）1"
    assert table1.data["column_reconstruction"] is False
    assert table2.data["column_reconstruction"] is False
    assert table3.data["column_reconstruction"] is False
    assert len(table1_rows) == 14
    assert len(table2_rows) == 9
    assert len(table3_rows) == 7
    assert table1_rows[0].text == "最大許容微粒子数（個／m3）"
    assert table2_rows[-1].text == "その他の区域        月1回      週1回         週1回            ----"
    assert table3_rows[-1].text == "D        200                100              50       ----"
    assert "表１ 清浄区域の分類" not in (by_nid["cha7.p7_1"].text or "")
    assert "表２ 微生物管理に係る環境モニタリングの頻度" not in (by_nid["cha11.p11_3"].text or "")
    assert "cha11.p11_3.pre1" not in by_nid
    assert not qualitycheck_document(ir_doc.content)
