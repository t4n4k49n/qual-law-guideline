# RUN

- run_id: `20260208-055930008_run-normalized-335AC0000000145-v3-int`
- branch: `run/normalized-335AC0000000145-v3-int`
- input: `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\335AC0000000145_20260501_507AC0000000037\335AC0000000145_20260501_507AC0000000037.xml`
- doc_id: `jp_egov_335AC0000000145_20260501_507AC0000000037`

## 対象e-Gov法令URL

- https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037

## 実行コマンド

`python -m qai_xml2ir.cli --input <xml> --out-dir out/20260208-055930008_run-normalized-335AC0000000145-v3-int --doc-id jp_egov_335AC0000000145_20260501_507AC0000000037 --retrieved-at 2026-02-08 --source-url https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037 --emit-only all`

## 出力

- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_ir.yaml`
- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/jp_egov_335AC0000000145_20260501_507AC0000000037.parser_profile.yaml`
- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_profile.yaml`
- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/jp_egov_335AC0000000145_20260501_507AC0000000037.meta.yaml`
- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/manifest.yaml`

## 検証結果（verify）

- `schema`: `qai.regdoc_ir.v3`
- `doc_id`: `jp_egov_335AC0000000145_20260501_507AC0000000037`
- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## 問題解消確認（15:16 / 1:2）

- `ch4`: `art1516`（ord=`351`） < `art17`（ord=`352`）
- `annex38.art1`: `annex38.art1.i12`（ord=`2279`） < `annex38.art1.i3`（ord=`2280`）
- `annex40.art1`: `annex40.art1.i12`（ord=`2290`） < `annex40.art1.i3`（ord=`2291`）

## 判定

- 正規化チェックを満たす。
- PR承認後に `data/normalized/jp_egov_335AC0000000145_20260501_507AC0000000037/` へ昇格を実施する。
