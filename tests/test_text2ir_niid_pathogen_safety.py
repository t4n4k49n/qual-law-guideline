from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

from qai_text2ir.profile_loader import load_parser_profile
from qai_text2ir.text_parser import parse_text_to_ir, qualitycheck_document
from qai_xml2ir.verify import verify_document


SOURCE = Path("data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt")
PROFILE = Path("src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_v1.yaml")
FULL_PROFILE = Path("src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_full_v1.yaml")


def _walk(node):
    yield node
    for child in node.children:
        yield from _walk(child)


def test_niid_profile_drops_front_matter_toc_and_annexes_for_body_phase() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_trial",
        parser_profile=profile,
    )
    verify_document(ir_doc.to_dict())

    root_chapters = [node for node in ir_doc.content.children if node.kind == "chapter"]
    root_nums = [node.num for node in root_chapters]
    counts = Counter(root_nums)
    headings_and_text = [str(part) for node in _walk(ir_doc.content) for part in (node.heading, node.text) if part]

    assert root_nums == ["1", "2", "3", "4", "5", "6"]
    assert all(counts[num] == 1 for num in root_nums)
    assert not any(part.strip() == "別表１" for part in headings_and_text)
    assert not qualitycheck_document(ir_doc.content)


def test_niid_profile_parses_articles_paragraphs_and_numbered_items() -> None:
    profile = load_parser_profile(path=PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_trial",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    chapter_1 = next(node for node in nodes if node.kind == "chapter" and node.num == "1")
    article_1 = next(node for node in chapter_1.children if node.kind == "paragraph" and node.num == "1")
    article_2 = next(node for node in chapter_1.children if node.kind == "paragraph" and node.num == "2")
    article_9_2 = next(node for node in nodes if node.kind == "paragraph" and node.num == "9_2")
    article_1_para_2 = next(node for node in article_1.children if node.kind == "item" and node.num == "2")
    article_2_item_1 = next(node for node in article_2.children if node.kind == "subitem" and node.num == "1")

    assert chapter_1.heading == "総     則"
    assert article_1.text.startswith("国立感染症研究所病原体等安全管理規程")
    assert article_9_2.text.startswith("ポリオウイルス取扱施設運営委員会")
    assert article_1_para_2.text.startswith("安全管理規程は、感染症法に基づく")
    assert article_2_item_1.text.startswith("「病原体等」とは")


def test_niid_full_profile_keeps_body_and_annexes_without_toc_duplicates() -> None:
    profile = load_parser_profile(path=FULL_PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_20240401",
        parser_profile=profile,
    )
    verify_document(ir_doc.to_dict())

    root_children = ir_doc.content.children
    chapters = [node for node in root_children if node.kind == "chapter"]
    annexes = [node for node in root_children if node.kind == "annex"]
    tables = [node for node in _walk(ir_doc.content) if node.kind == "table" and node.data.get("parser") == "niid_annex_table_adapter"]
    table_rows = [
        row
        for table in tables
        for header in table.children
        if header.kind == "table_header"
        for row in header.children
        if row.kind == "table_row"
    ]

    assert [node.num for node in chapters] == ["1", "2", "3", "4", "5", "6"]
    assert [node.num for node in annexes] == [
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
    assert len(table_rows) == 112
    assert not qualitycheck_document(ir_doc.content)


def test_niid_full_profile_normalizes_display_prose_spacing() -> None:
    profile = load_parser_profile(path=FULL_PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_20240401",
        parser_profile=profile,
    )
    pattern = re.compile(r"[一-龯ぁ-んァ-ヶー々〆〇Ａ-Ｚａ-ｚ０-９][ 　]+[一-龯ぁ-んァ-ヶー々〆〇Ａ-Ｚａ-ｚ０-９]")

    for node in _walk(ir_doc.content):
        if node.kind in {"table", "table_header", "table_row", "preformatted"}:
            continue
        for value in (node.heading, node.text):
            if not value:
                continue
            assert not pattern.search(value), f"{node.nid}: {value!r}"
            assert "\\r" not in value
            assert "\\n" not in value


def test_niid_full_profile_preserves_numbered_annex_items_as_nodes() -> None:
    profile = load_parser_profile(path=FULL_PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_20240401",
        parser_profile=profile,
    )
    nodes = list(_walk(ir_doc.content))
    annexes = {node.num: node for node in nodes if node.kind == "annex"}

    expected = {
        "付表1-2": [str(num) for num in range(1, 9)],
        "付表1-3": [str(num) for num in range(1, 5)],
        "別表6": [str(num) for num in range(1, 12)],
        "別表9": [str(num) for num in range(1, 6)],
    }
    for annex_num, item_nums in expected.items():
        annex = annexes[annex_num]
        assert [child.num for child in annex.children if child.kind == "item"] == item_nums
        assert "１．" not in (annex.text or "")
        assert "２．" not in (annex.text or "")
        assert "。。" not in (annex.text or "")

    assert annexes["別表1"].heading is None
    assert annexes["別表1"].text.startswith("病原体等の取扱いにおいては")
    assert any(node.kind == "note" and node.text.startswith("註：") for node in _walk(annexes["付表1-2"]))
    assert any(node.kind == "note" and node.text.startswith("註：") for node in _walk(annexes["付表1-3"]))


def test_niid_full_profile_reconstructs_wide_tables_without_decimal_item_artifacts() -> None:
    profile = load_parser_profile(path=FULL_PROFILE)
    ir_doc = parse_text_to_ir(
        input_path=SOURCE,
        doc_id="jp_niid_pathogen_safety_management_20240401",
        parser_profile=profile,
    )
    annexes = {node.num: node for node in _walk(ir_doc.content) if node.kind == "annex"}

    for annex_num in ["別表4", "別表5", "別表8"]:
        annex = annexes[annex_num]
        assert any(child.kind == "table" for child in annex.children)
        assert not any(child.kind in {"item", "subitem"} for child in annex.children)
    betsu5_table = next(child for child in annexes["別表5"].children if child.kind == "table")
    betsu5_text = " ".join(row.text or "" for header in betsu5_table.children if header.kind == "table_header" for row in header.children)
    assert "0.01％以上の次亜" in betsu5_text
    betsu4_table = next(child for child in annexes["別表4"].children if child.kind == "table")
    betsu4_records = [
        row.data["record"]
        for header in betsu4_table.children
        if header.kind == "table_header"
        for row in header.children
    ]
    assert betsu4_table.children[0].data["columns"][:2] == ["section", "criterion"]
    assert any(record["section"] == "実験室" and record["criterion"] == "－" for record in betsu4_records)
    assert any(record["section"] == "実験室内" and record["criterion"] == "－" for record in betsu4_records)
    for merged_row in [record for record in betsu4_records if record["section"] in {"実験室", "実験室内"} and record["criterion"] == "－"]:
        assert all(merged_row[column] == "実験室" for column in betsu4_table.children[0].data["columns"][2:])
    assert any(record["section"] == "感染動物の飼育設備" and record["criterion"] == "－" for record in betsu4_records)
    assert any(record["section"] == "滅菌設備" and record["criterion"] == "－" for record in betsu4_records)
    betsu5_records = [
        row.data["record"]
        for header in betsu5_table.children
        if header.kind == "table_header"
        for row in header.children
    ]
    assert next(record for record in betsu5_records if record["criterion"] == "複数名での作業")["section"] == "使用の基準"
    assert next(record for record in betsu5_records if record["criterion"] == "安全キャビネット内での適切な使用")["section"] == "使用の基準"
    assert not any(record["section"] == "運搬の基準" for record in betsu5_records)
    assert any(node.kind == "note" and "運搬する場合には容器に封入すること" in (node.text or "") for node in annexes["別表5"].children)

    for table in [child for node in annexes.values() for child in node.children if child.kind == "table"]:
        for header in [child for child in table.children if child.kind == "table_header"]:
            columns = header.data["columns"]
            for row in header.children:
                assert len(row.data["cells"]) == len(columns), f"{row.nid}: {row.text}"
                assert row.text.count(" | ") == len(columns) - 1, f"{row.nid}: {row.text}"
