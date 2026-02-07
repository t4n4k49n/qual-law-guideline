## 概要

`336M50000100002_20260501_507M60000100117.xml` を IR v2 へ正規化しました。  
前回RUNで検出された `root` 直下 `ord` 並びの問題を解消して再実行しています。

## 入力

- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336M50000100002_20260501_507M60000100117\336M50000100002_20260501_507M60000100117.xml`

## 出力

- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/jp_egov_336M50000100002_20260501_507M60000100117.parser_profile.yaml`
- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/jp_egov_336M50000100002_20260501_507M60000100117.meta.yaml`
- `out/20260207-153733372_run-normalized-336M50000100002-v2-rerun/manifest.yaml`

## 検証

- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## 比較表（人間レビュー用）

| 観点 | 内容 |
| --- | --- |
| 対象ノード（最深） | `art8.p1.i1.ha.pt2` |
| 人間可読の経路 | `第二章 > 第一節 > 第八条 > 1 > 一 > ハ > （２）` |
| YAML上の経路（nid） | `root > ch2 > ch2.sec1 > art8 > art8.p1 > art8.p1.i1 > art8.p1.i1.ha > art8.p1.i1.ha.pt2` |
| ノード本文 | `流しを設置しないこと。` |
| ord | `000001.000000.000002.000000.000001.000000.000008.000000.000001.000000.000001.000000.000003.000000.000002.000000` |

## 判定

- 正規化チェックを満たしたため、PR承認後に `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/` へ昇格する。
