# PR: 正規化RUN 20260209-125137789_run-normalized-336CO0000000011-v3

## 概要

`jp_egov_336CO0000000011_20260501_507CO0000000362` の正規化RUN（v3）を実施しました。verify最小チェックは全てOKです。

## e-Gov法令リンク

- https://laws.e-gov.go.jp/law/336CO0000000011/20260501_507CO0000000362

## 入力

- `%USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\336CO0000000011_20260501_507CO0000000362\\336CO0000000011_20260501_507CO0000000362.xml`

## 出力

- `out/20260209-125137789_run-normalized-336CO0000000011-v3/jp_egov_336CO0000000011_20260501_507CO0000000362.regdoc_ir.yaml`
- `out/20260209-125137789_run-normalized-336CO0000000011-v3/jp_egov_336CO0000000011_20260501_507CO0000000362.parser_profile.yaml`
- `out/20260209-125137789_run-normalized-336CO0000000011-v3/jp_egov_336CO0000000011_20260501_507CO0000000362.regdoc_profile.yaml`
- `out/20260209-125137789_run-normalized-336CO0000000011-v3/jp_egov_336CO0000000011_20260501_507CO0000000362.meta.yaml`
- `out/20260209-125137789_run-normalized-336CO0000000011-v3/manifest.yaml`

## 検証

- `assert_unique_nids`: OK
- `check_annex_article_nids`: OK
- `check_appendix_scoped_indices`: OK
- `check_ord_format_and_order`: OK

## 比較表（人間レビュー用）

| 観点 | 内容 |
| --- | --- |
| 対象ノード（最深） | `art80.p2.i3.i` |
| 人間可読の経路 | `第十五章 > 第八十条 > ２ > 三 > イ` |
| YAML上の経路（nid） | `root > ch15 > art80 > art80.p2 > art80.p2.i3 > art80.p2.i3.i` |
| ノード本文 | `生物学的製剤` |
| ord | `657` |
