# PIC/S Annex 2A 正規化RUN v1

## まとめ

PIC/S PE 009-17 Annex 2A を正式版昇格候補として生成しました。前段PRでTable 1の結合見出しを目検修正済みであり、今回の候補でもその構造が維持されていること、Warningが残っていないこと、DQチェックシート向けのtable_row選択性が成立していることを確認しています。

## 対象

| 項目 | 内容 |
|---|---|
| doc_id | `pics_pe00917_annex2a_20230825` |
| source URL | `https://picscheme.org/docview/8881` |
| 入力 | `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt` |
| parser profile | `src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml` |
| 正本候補 | `runs/20260528-194731940_run-normalized-pics-annex2a-v1/promotion_candidate/` |

## 検証結果

| 確認 | 結果 |
|---|---|
| strict bundle generation | pass |
| promotion goal check | pass |
| schema | `qai.regdoc_ir.v4` |
| nodes | 215 |
| source span coverage | 1.0 |
| goal check errors | none |
| goal check warnings | none |
| manifest quality warnings | none |
| IR warning metadata scan | none |
| focused tests | `13 passed` |

## Table / Warning 目検確認

- Table count: 1.
- Table 1: 6 rows、table note 3件。
- Figure count: 3.
- 前段レビューでPDF page 77-79を確認済み。
- 今回候補でも Table 1 の4つの application columns は、結合親見出し `Application of this Annex (see note 1)` を列名に保持。
- Warning系は strict / promotion goal / IR metadata scan で該当なし。

## 深い階層サンプル

- `runs/20260528-194731940_run-normalized-pics-annex2a-v1/SAMPLE_EXTRACT.md`
- target nid: `ann2a.sec2.ib.tbl1.tblh.tblr4`
- table row が `section -> item -> table -> table_header -> table_row` の祖先経路で保持されていることを確認。

## 昇格境界

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/pics_pe00917_annex2a_20230825/` に複写します。

<!-- PR_BODY_FILE: runs/20260528-194731940_run-normalized-pics-annex2a-v1/PR.md -->
