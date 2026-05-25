from __future__ import annotations

from pathlib import Path

from qai_text2ir.html_extract import extract_mhlw_t_doc_lines
from qai_text2ir.mhlw_csv_annexes import extract_mhlw_csv_annexes_from_html, extract_mhlw_csv_annexes_from_lines


SOURCE_HTML = Path("data/human-readable/mhlw/csv_guideline/00tb6573.html")


def test_csv_annex_inventory_reads_image_link_and_title_only_table() -> None:
    annexes = extract_mhlw_csv_annexes_from_html(SOURCE_HTML)
    by_num = {annex.num: annex for annex in annexes}

    assert set(by_num) == {"別紙1", "別紙2"}
    assert by_num["別紙1"].heading == "コンピュータ化システムのライフサイクルモデル"
    assert by_num["別紙1"].source_format == "html_image_reference"
    assert by_num["別紙1"].label == "画像1 (36KB)"
    assert by_num["別紙1"].href == "t_img?img=6676058"
    assert by_num["別紙1"].resolved_url == "https://www.mhlw.go.jp/web/t_img?img=6676058"
    assert by_num["別紙1"].extractable_text is False
    assert "OCR" in (by_num["別紙1"].deferred_reason or "")

    assert by_num["別紙2"].heading == "カテゴリ分類表と対応例"
    assert by_num["別紙2"].source_format == "html_table_title_only"
    assert by_num["別紙2"].table_rows_found == 0
    assert by_num["別紙2"].extractable_text is False


def test_csv_annex_inventory_from_extracted_lines_tracks_visible_annexes() -> None:
    lines = extract_mhlw_t_doc_lines(SOURCE_HTML)
    annexes = extract_mhlw_csv_annexes_from_lines(lines)
    by_num = {annex.num: annex for annex in annexes}

    assert by_num["別紙1"].label == "画像1 (36KB)"
    assert by_num["別紙2"].heading == "カテゴリ分類表と対応例"
