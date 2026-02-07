## 概要

指定XMLから `jp_egov_336M50000100002_20260501_507M60000100117` を正規化変換しました（IR v2）。

## 入力

- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336M50000100002_20260501_507M60000100117\336M50000100002_20260501_507M60000100117.xml`

## 出力

- `out/20260207-153154910_run-normalized-336M50000100002-v2/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260207-153154910_run-normalized-336M50000100002-v2/jp_egov_336M50000100002_20260501_507M60000100117.parser_profile.yaml`
- `out/20260207-153154910_run-normalized-336M50000100002-v2/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260207-153154910_run-normalized-336M50000100002-v2/jp_egov_336M50000100002_20260501_507M60000100117.meta.yaml`
- `out/20260207-153154910_run-normalized-336M50000100002-v2/manifest.yaml`

## 検証

- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: NG（`children ord not sorted under root`）

## 補足

- 現時点では `data/normalized` への昇格は行っていません。
- 上記検証NGを解消後に昇格PRへ進める想定です。
