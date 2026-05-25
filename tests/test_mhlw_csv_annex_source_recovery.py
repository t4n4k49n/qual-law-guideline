from __future__ import annotations

from pathlib import Path

from qai_text2ir.mhlw_csv_annex_source_recovery import build_mhlw_csv_annex_source_recovery


SOURCE_HTML = Path("data/human-readable/mhlw/csv_guideline/00tb6573.html")


def test_csv_annex_source_recovery_classifies_annex1_as_ocr_candidate() -> None:
    items = build_mhlw_csv_annex_source_recovery(SOURCE_HTML, image_http_status=200)
    by_num = {item.num: item for item in items}

    assert by_num["別紙1"].source_candidate == "mhlw_image_endpoint"
    assert by_num["別紙1"].candidate_url == "https://www.mhlw.go.jp/web/t_img?img=6676058"
    assert by_num["別紙1"].source_status == "reachable_http_200"
    assert by_num["別紙1"].ocr_required is True
    assert by_num["別紙1"].table_body_available is False


def test_csv_annex_source_recovery_marks_page2_table_as_no_ocr_path() -> None:
    page2_html = """
    <html><body>
      <p>別紙2</p>
      <p>カテゴリ分類表と対応例</p>
      <table><tr><td>カテゴリ</td><td>対応例</td></tr></table>
    </body></html>
    """
    items = build_mhlw_csv_annex_source_recovery(SOURCE_HTML, page2_html_text=page2_html)
    by_num = {item.num: item for item in items}

    assert by_num["別紙2"].source_candidate == "mhlw_official_page2_html"
    assert by_num["別紙2"].candidate_url.endswith("pageNo=2")
    assert by_num["別紙2"].source_status == "official_page2_contains_table_body"
    assert by_num["別紙2"].ocr_required is False
    assert by_num["別紙2"].table_body_available is True
