## 概要

`jp_egov_336M50000100001_20260501_507M60000100117` の正規化RUN（v3）を実施しました。verify最小チェックは全てOKです。

## e-Gov法令リンク

- https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117

## 入力

- `%USERPROFILE%\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\336M50000100001_20260501_507M60000100117\\336M50000100001_20260501_507M60000100117.xml`

## 出力

- `out/20260209-141050252_run-normalized-336M50000100001-v3/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260209-141050252_run-normalized-336M50000100001-v3/jp_egov_336M50000100001_20260501_507M60000100117.parser_profile.yaml`
- `out/20260209-141050252_run-normalized-336M50000100001-v3/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260209-141050252_run-normalized-336M50000100001-v3/jp_egov_336M50000100001_20260501_507M60000100117.meta.yaml`
- `out/20260209-141050252_run-normalized-336M50000100001-v3/manifest.yaml`

## 検証

- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## 比較表（人間レビュー用）

| 観点 | 内容 |
| --- | --- |
| 対象ノード（最深） | `art228_20.p1.i1.ha.pt1` |
| 人間可読の経路 | `第九章 > 第二百二十八条の二十 > 1 > 一 > ハ > （１）` |
| YAML上の経路（nid） | `root > ch9 > art228_20 > art228_20.p1 > art228_20.p1.i1 > art228_20.p1.i1.ha > art228_20.p1.i1.ha.pt1` |
| ノード本文 | `障害` |
| ord | `4244` |
