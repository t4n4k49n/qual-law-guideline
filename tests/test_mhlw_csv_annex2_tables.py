from __future__ import annotations

from pathlib import Path

from qai_text2ir.mhlw_csv_annex2_tables import extract_mhlw_csv_annex2_tables


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
