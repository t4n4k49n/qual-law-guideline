## 概要

`jp_egov_335AC0000000145_20260501_507AC0000000037` の正規化RUN（v3）を実施しました。verify最小チェックは全てOKです。

## e-Gov法令リンク

- https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037

## 入力

- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\335AC0000000145_20260501_507AC0000000037\335AC0000000145_20260501_507AC0000000037.xml`

## 出力

- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_ir.yaml`
- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/jp_egov_335AC0000000145_20260501_507AC0000000037.parser_profile.yaml`
- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_profile.yaml`
- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/jp_egov_335AC0000000145_20260501_507AC0000000037.meta.yaml`
- `out/20260209-115003179_run-normalized-335AC0000000145-v3-rerun/manifest.yaml`

## 検証

- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## 比較表（人間レビュー用）

| 観点 | 内容 |
| --- | --- |
| 対象ノード（最深） | `art29_2.p1.i2.ro` |
| 人間可読の経路 | `第七章 > 第一節 > 第二十九条の二 > 1 > 二 > ロ` |
| YAML上の経路（nid） | `root > ch7 > ch7.sec1 > art29_2 > art29_2.p1 > art29_2.p1.i2 > art29_2.p1.i2.ro` |
| ノード本文 | `一般用医薬品` |
| ord | `989` |

## 正式版への昇格

- PR承認確認後、`data/normalized/jp_egov_335AC0000000145_20260501_507AC0000000037/` へ4ファイルを複写済み
