## 概要

`335AC0000000145_20260501_507AC0000000037.xml` を IR v3（ord=int絶対順序）で正規化しました。

## e-Gov法令リンク

- https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037

## 入力

- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\335AC0000000145_20260501_507AC0000000037\335AC0000000145_20260501_507AC0000000037.xml`

## 出力

- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_ir.yaml`
- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/jp_egov_335AC0000000145_20260501_507AC0000000037.parser_profile.yaml`
- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/jp_egov_335AC0000000145_20260501_507AC0000000037.regdoc_profile.yaml`
- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/jp_egov_335AC0000000145_20260501_507AC0000000037.meta.yaml`
- `out/20260208-055930008_run-normalized-335AC0000000145-v3-int/manifest.yaml`

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

## 15:16 / 1:2 の順序確認

- `ch4`: `art1516`（ord=`351`） < `art17`（ord=`352`）
- `annex38.art1`: `annex38.art1.i12`（ord=`2279`） < `annex38.art1.i3`（ord=`2280`）
- `annex40.art1`: `annex40.art1.i12`（ord=`2290`） < `annex40.art1.i3`（ord=`2291`）

## 判定

- 正規化チェックを満たしたため、PR承認後に `data/normalized/jp_egov_335AC0000000145_20260501_507AC0000000037/` へ昇格する。
