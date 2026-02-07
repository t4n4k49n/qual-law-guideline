# RUN

- run_id: 20260208-023854899_run-normalized-335AC0000000145-v2
- branch: un/normalized-335AC0000000145-v2
- input: %USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\335AC0000000145_20260501_507AC0000000037\335AC0000000145_20260501_507AC0000000037.xml
- doc_id: jp_egov_335AC0000000145_20260501_507AC0000000037

## 実行コマンド

python -m qai_xml2ir.cli --input <xml> --out-dir out/20260208-023854899_run-normalized-335AC0000000145-v2 --doc-id jp_egov_335AC0000000145_20260501_507AC0000000037 --retrieved-at 2026-02-08 --source-url https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037 --emit-only all

## 出力

- out/20260208-023854899_run-normalized-335AC0000000145-v2/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_ir.yaml
- out/20260208-023854899_run-normalized-335AC0000000145-v2/jp_egov_335AC0000000145_20260501_507AC0000000037.parser_profile.yaml
- out/20260208-023854899_run-normalized-335AC0000000145-v2/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_profile.yaml
- out/20260208-023854899_run-normalized-335AC0000000145-v2/jp_egov_335AC0000000145_20260501_507AC0000000037.meta.yaml
- out/20260208-023854899_run-normalized-335AC0000000145-v2/manifest.yaml

## 検証結果（verify）

- schema: qai.regdoc_ir.v2
- doc_id: jp_egov_335AC0000000145_20260501_507AC0000000037
- ssert_unique_nids: OK
- check_annex_article_nids: OK
- check_appendix_scoped_indices: OK
- check_ord_format_and_order: NG（3件）
  - children ord not sorted under ch4
  - children ord not sorted under annex38.art1
  - children ord not sorted under annex40.art1

## 判定

- ord整列検証で3件NGのため、このままでは正式版昇格（data/normalized/<doc_id>/）を実施しない。
- 原因切り分け・修正方針はPR上で確認する。
