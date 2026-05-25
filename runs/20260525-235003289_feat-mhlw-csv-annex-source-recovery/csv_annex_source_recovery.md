# CSVガイドライン 別紙ソース回収inventory

| 別紙 | 現状 | 回収候補 | 候補URL | 状態 | OCR | 次アクション |
| --- | --- | --- | --- | --- | --- | --- |
| 別紙1 | html_image_reference | mhlw_image_endpoint | https://www.mhlw.go.jp/web/t_img?img=6676058 | reachable_http_200 | 要 | download_image_then_ocr_or_manual_transcription |
| 別紙2 | html_table_title_only | mhlw_official_page2_html | https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=2 | official_page2_contains_table_body | 不要 | fetch_official_page2_and_parse_html_table |

## 判定メモ

### 別紙1

- 見出し: コンピュータ化システムのライフサイクルモデル
- 現状メモ: HTML本文には画像リンク表示のみが残るため、内容テキスト化には画像取得/OCRが必要
- 表本体利用可否: 不可
- 根拠: `local_page1_html_points_to_image_only; textual content is not available in HTML`

### 別紙2

- 見出し: カテゴリ分類表と対応例
- 現状メモ: HTML本文抽出範囲には表題行のみが残り、表本体行が確認できない
- 表本体利用可否: 可
- 根拠: `local_page1_html_has_annex2_title_only; official page2 is the candidate for the table body`
