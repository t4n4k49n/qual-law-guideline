## 概要

`416M60000100179_20260501_507M60000100117.xml` を IR v2 へ正規化しました。

## 入力

- `C:\Users\ryoki\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\416M60000100179_20260501_507M60000100117\416M60000100179_20260501_507M60000100117.xml`

## 出力

- `out/20260208-020202287_run-normalized-416M60000100179-v2/jp_egov_416M60000100179_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260208-020202287_run-normalized-416M60000100179-v2/jp_egov_416M60000100179_20260501_507M60000100117.parser_profile.yaml`
- `out/20260208-020202287_run-normalized-416M60000100179-v2/jp_egov_416M60000100179_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260208-020202287_run-normalized-416M60000100179-v2/jp_egov_416M60000100179_20260501_507M60000100117.meta.yaml`
- `out/20260208-020202287_run-normalized-416M60000100179-v2/manifest.yaml`

## 検証

- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## 比較表（人間レビュー用）

| 観点 | 内容 |
| --- | --- |
| 対象ノード（最深） | `art27.p1.i9.ni` |
| 人間可読の経路 | `第二章 > 第四節 > 第二十七条 > 1 > 九 > ニ` |
| YAML上の経路（nid） | `root > ch2 > ch2.sec4 > art27 > art27.p1 > art27.p1.i9 > art27.p1.i9.ni` |
| ノード本文 | `継代培養の状況` |
| ord | `000001.000000.000002.000000.000004.000000.000027.000000.000001.000000.000009.000000.000004.000000` |

## 判定

- 正規化チェックを満たしたため、PR承認後に `data/normalized/jp_egov_416M60000100179_20260501_507M60000100117/` へ昇格する。
