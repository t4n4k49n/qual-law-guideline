# 正規化RUN: NIID病原体等安全管理規程 v8

## 概要

- run_id: `20260531-023248221_run-normalized-niid-pathogen-safety-v8`
- 対象: `jp_niid_pathogen_safety_management_20240401`
- 目的: `promotion_candidate/` に正規化候補を作成し、表4/表5の目検修正を反映する。

## 主な修正

- 別表4の結合セル行（`実験室`、`実験室内`）は、Markdown/IRデータとして欠落しないよう全BSL列へ値を複製した。
- 別表5の `○ 運搬の基準（1種～4種病原体等）` 以降は表外の箇条書きとして扱い、表5のtable_rowから除外した。
- 運搬基準本文は `ann5.not3` のnoteとして保持した。
- 表4/表5の再結合Markdownを `TABLE4_5_RECONSTRUCTION_CHECK.md` に出力した。

## 検証

- focused tests: `13 passed`
- full tests: `257 passed, 1 skipped`
- goal check: PASS
- special structure audit: PASS
- IR structure check: PASS
- absolute local path check: PASS

## 昇格

- この親PRでは `data/normalized/` は変更しない。
- PR承認後、子PRで `promotion_candidate/` から `data/normalized/` へ複写する。
