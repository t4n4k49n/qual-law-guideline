## 概要

`jp_egov_336M50000100002_20260501_507M60000100117` の正規化RUN（v3）を実施し、検証OKのため `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/` へ昇格しました。

## e-Gov法令リンク

- https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117

## 入力

- `%USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\336M50000100002_20260501_507M60000100117\\336M50000100002_20260501_507M60000100117.xml`

## 出力

- `out/20260209-113403073_run-normalized-336M50000100002-v3/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260209-113403073_run-normalized-336M50000100002-v3/jp_egov_336M50000100002_20260501_507M60000100117.parser_profile.yaml`
- `out/20260209-113403073_run-normalized-336M50000100002-v3/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260209-113403073_run-normalized-336M50000100002-v3/jp_egov_336M50000100002_20260501_507M60000100117.meta.yaml`
- `out/20260209-113403073_run-normalized-336M50000100002-v3/manifest.yaml`

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
| ord | `195` |

## 正式版への昇格

- `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/` へ4ファイルをコピー済み
