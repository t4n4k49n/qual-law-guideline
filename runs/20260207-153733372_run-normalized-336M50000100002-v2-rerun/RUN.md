# RUN

- run_id: `20260207-153733372_run-normalized-336M50000100002-v2-rerun`
- branch: `run/normalized-336M50000100002-v2`
- input: `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336M50000100002_20260501_507M60000100117\336M50000100002_20260501_507M60000100117.xml`
- doc_id: `jp_egov_336M50000100002_20260501_507M60000100117`
- note: `20260207-153154910_run-normalized-336M50000100002-v2` の検証NG（root ord順）を解消して再実行

## 実行コマンド

`python -m qai_xml2ir.cli --input <xml> --out-dir out/20260207-153733372_run-normalized-336M50000100002-v2-rerun --doc-id jp_egov_336M50000100002_20260501_507M60000100117 --retrieved-at 2026-02-07 --source-url https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117 --emit-only all`

## 出力

- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/jp_egov_336M50000100002_20260501_507M60000100117.parser_profile.yaml`
- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/jp_egov_336M50000100002_20260501_507M60000100117.meta.yaml`
- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/manifest.yaml`

## 検証結果（verify）

- `schema`: `qai.regdoc_ir.v2`
- `doc_id`: `jp_egov_336M50000100002_20260501_507M60000100117`
- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## 判定

- 正規化チェックを満たしたため、PR承認後に `data/normalized/<doc_id>/` へ昇格可能。
