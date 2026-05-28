# PIC/S Part II 正規化RUN v1

## まとめ

PIC/S PE 009-17 Part II を正式版昇格候補として生成しました。前段PRでTable 1の結合見出しを目検修正済みであり、今回の候補でもその構造が維持されていること、Warningが残っていないこと、DQチェックシート向けのtable_row選択性が成立していることを確認しています。

## 対象

| 項目 | 内容 |
|---|---|
| doc_id | `pics_pe00917_part2_20230825` |
| source URL | `https://picscheme.org/docview/6607` |
| 入力 | `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt` |
| parser profile | `src/qai_text2ir/profiles/pics_part2_default_v1.yaml` |
| 正本候補 | `runs/20260529-022734132_run-normalized-pics-part2-v1/promotion_candidate/` |

## 検証結果

| 確認 | 結果 |
|---|---|
| strict bundle generation | pass |
| promotion goal check | pass |
| schema | `qai.regdoc_ir.v4` |
| nodes | 601 |
| source span coverage | 1.0 |
| goal check errors | none |
| goal check warnings | none |
| manifest quality warnings | none |
| IR warning metadata scan | none |
| special structure audit | pass |
| focused tests | `8 passed` |

## Table / Warning 目検確認

- Table count: 1.
- Table 1: 7 rows、table note 1件。
- Source table-like blocks: 2、unresolved special blocks: 0。
- 前段レビューでPDF page 8を確認済み。
- 今回候補でも Table 1 の5つの application step columns は、結合親見出し `Application of this Guide to steps (shown in grey) used in this type of manufacturing` を列名に保持。
- Warning系は strict / promotion goal / IR metadata scan で該当なし。

## 深い階層サンプル

`runs/20260529-022734132_run-normalized-pics-part2-v1/SAMPLE_EXTRACT.md` より。section/table本文は表の可読性を優先して空欄化し、祖先ノード自体は省略していません。

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha1` | `chapter` | `1.` | `INTRODUCTION` |
| 3 | `cha1.sec1_2` | `section` | `1.2` |  |
| 4 | `cha1.sec1_2.tbl1` | `table` | `table` |  |
| 5 | `cha1.sec1_2.tbl1.tblh` | `table_header` | `table_header` | `Type of Manufacturing | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 1 | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 2 | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 3 | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 4 | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 5` |
| 6 | `cha1.sec1_2.tbl1.tblh.tblr7` | `table_row` | `table_row` | `“Classical” Fermentation to produce an API | Establishment of cell bank | Maintenance of the cell bank | Introduction of the cells into fermentation | Isolation and purification | Physical processing, and packaging` |

## 昇格境界

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/pics_pe00917_part2_20230825/` に複写します。

<!-- PR_BODY_FILE: runs/20260529-022734132_run-normalized-pics-part2-v1/PR.md -->
