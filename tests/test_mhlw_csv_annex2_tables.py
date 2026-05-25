from __future__ import annotations

from pathlib import Path

from qai_text2ir.mhlw_csv_annex2_tables import (
    build_excluded_table_semantic_records,
    build_main_table_semantic_records,
    extract_mhlw_csv_annex2_tables,
)


PAGE2_HTML = Path("data/human-readable/mhlw/csv_guideline/00tb6573_page2.html")


def test_extract_csv_annex2_page2_tables_expands_html_cells() -> None:
    tables = extract_mhlw_csv_annex2_tables(PAGE2_HTML)
    by_no = {table.table_no: table for table in tables}

    assert list(by_no) == ["1", "2"]
    assert by_no["1"].heading == "カテゴリ分類表"
    assert by_no["1"].columns[:4] == ["category_no", "category_name", "content", "content_detail"]
    assert len(by_no["1"].columns) == 20
    assert len(by_no["1"].rows) == 7
    assert by_no["1"].rows[0][:4] == ["カテゴリ", "カテゴリ", "内容", "内容"]
    assert by_no["1"].rows[1][0] == "1"
    assert by_no["1"].rows[1][1] == "基盤ソフト"
    assert "プラットフォーム" in by_no["1"].rows[1][2]
    assert by_no["1"].rows[4][0] == "3"
    assert by_no["1"].rows[3][1] == "構成設定していないソフトウェア"
    assert by_no["1"].rows[4][3] == "単独のコンピュータシステム"

    assert by_no["2"].heading == "本ガイドラインの対象外"
    assert by_no["2"].columns == ["excluded_item", "description"]
    assert len(by_no["2"].rows) == 1
    assert by_no["2"].rows[0][0] == "本ガイドラインの対象外"


def test_csv_annex2_semantic_records_group_category_rows_and_split_symbols() -> None:
    tables = extract_mhlw_csv_annex2_tables(PAGE2_HTML)
    main = next(table for table in tables if table.table_no == "1")
    excluded = next(table for table in tables if table.table_no == "2")

    records = build_main_table_semantic_records(main)
    by_category = {record["category_no"]: record for record in records}

    assert len(records) == 5
    assert by_category["1"]["record_id"] == "csv_annex2.category1"
    assert by_category["1"]["variants"][0]["semantic_values"]["development_plan"] == {
        "raw": "○1",
        "symbol": "○",
        "status": "conditional_required",
        "meaning": "システムアセスメントの結果による(基本的には必要)",
        "footnote_refs": ["1"],
    }
    assert by_category["1"]["variants"][0]["semantic_values"]["iq"]["footnote_refs"] == ["2"]
    assert by_category["2"]["semantic_warnings"][0]["warning"] == "blank_semantic_value"
    assert by_category["2"]["semantic_warnings"][-1]["warning"] == "blank_category_name_preserved"
    assert by_category["3"]["raw_row_nums"] == [4, 5]
    assert [variant["content_detail"] for variant in by_category["3"]["variants"]] == [
        "製造設備、分析機器、製造支援設備等に搭載されるシステム",
        "単独のコンピュータシステム",
    ]
    assert by_category["5"]["variants"][0]["semantic_values"]["fs"]["footnote_refs"] == ["4"]

    excluded_records = build_excluded_table_semantic_records(excluded)
    assert len(excluded_records) == 1
    assert excluded_records[0]["record_id"] == "csv_annex2.excluded.r1"
    assert "市販のワープロソフト" in excluded_records[0]["description"]
