# RUN 20260206-111530177_run-xml2ir-336M50000100002

## Summary
- xml2ir 実行（入力: 336M50000100002_20260501_507M60000100117.xml）
- 4ファイル（IR / parser_profile / regdoc_profile / meta）を出力
- manifest.yaml を正式版向けに更新（検証/レビュー結果を追記）

## Command
python -m qai_xml2ir.cli --input "C:\Users\ryoki\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336M50000100002_20260501_507M60000100117\336M50000100002_20260501_507M60000100117.xml" --out-dir "out\20260206-111530177_run-xml2ir-336M50000100002" --doc-id "jp_test_336M50000100002_20260501" --emit-only all

## Outputs
- out\20260206-111530177_run-xml2ir-336M50000100002\jp_test_336M50000100002_20260501.regdoc_ir.yaml
- out\20260206-111530177_run-xml2ir-336M50000100002\jp_test_336M50000100002_20260501.parser_profile.yaml
- out\20260206-111530177_run-xml2ir-336M50000100002\jp_test_336M50000100002_20260501.regdoc_profile.yaml
- out\20260206-111530177_run-xml2ir-336M50000100002\jp_test_336M50000100002_20260501.meta.yaml
- out\20260206-111530177_run-xml2ir-336M50000100002\manifest.yaml

## Checks
- verify.py: assert_unique_nids / check_annex_article_nids / check_appendix_scoped_indices => PASS
- 目視レビュー: 第六条・第四号・イロハの階層と本文の対応を確認。欠落や順序の逆転は無し。

## Notes
- 実行日時: 2026-02-06 11:15 頃
