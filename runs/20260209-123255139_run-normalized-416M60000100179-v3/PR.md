# PR: 正規化RUN 20260209-123255139_run-normalized-416M60000100179-v3

## 概要

`jp_egov_416M60000100179_20260501_507M60000100117` の正規化RUN（v3）を実施しました。verify最小チェックは全てOKです。

## e-Gov法令リンク

- https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117

## 入力

- `%USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\416M60000100179_20260501_507M60000100117\\416M60000100179_20260501_507M60000100117.xml`

## 出力

- `out/20260209-123255139_run-normalized-416M60000100179-v3/jp_egov_416M60000100179_20260501_507M60000100117.regdoc_ir.yaml`
- `out/20260209-123255139_run-normalized-416M60000100179-v3/jp_egov_416M60000100179_20260501_507M60000100117.parser_profile.yaml`
- `out/20260209-123255139_run-normalized-416M60000100179-v3/jp_egov_416M60000100179_20260501_507M60000100117.regdoc_profile.yaml`
- `out/20260209-123255139_run-normalized-416M60000100179-v3/jp_egov_416M60000100179_20260501_507M60000100117.meta.yaml`
- `out/20260209-123255139_run-normalized-416M60000100179-v3/manifest.yaml`

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
| ord | `321` |
