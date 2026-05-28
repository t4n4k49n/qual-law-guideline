# PIC/S Part I 正規化RUN v1

## まとめ

PIC/S PE 009-17 Part I を正式版昇格候補として生成しました。前段PRでTable/Warning/Note周りを確認し、Chapter 7冒頭Noteの帰属修正を反映済みです。今回の候補では表・図の未解決構造がなく、Warningも残っていないことを確認しています。

## 対象

| 項目 | 内容 |
|---|---|
| doc_id | `pics_pe00917_part1_20230825` |
| source URL | `https://picscheme.org/docview/6606` |
| 入力 | `data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt` |
| parser profile | `src/qai_text2ir/profiles/pics_part1_default_v3.yaml` |
| 正本候補 | `runs/20260529-034208684_run-normalized-pics-part1-v1/promotion_candidate/` |

## 検証結果

| 確認 | 結果 |
|---|---|
| strict bundle generation | pass |
| promotion goal check | pass |
| schema | `qai.regdoc_ir.v4` |
| nodes | 344 |
| source span coverage | 1.0 |
| goal check errors | none |
| goal check warnings | none |
| manifest quality warnings | none |
| IR warning metadata scan | none |
| special structure audit | pass |
| focused tests | `9 passed` |
| full test suite | `251 passed, 1 skipped` |

## Table / Warning 目検確認

- Table count: 0.
- Table row count: 0.
- Figure count: 0.
- Unresolved special blocks: 0.
- Warning系は strict / promotion goal / IR metadata scan で該当なし。
- 前段レビューで、本文に構造化すべきTable/Figureがないことを確認済み。
- 前段レビューで修正した Chapter 7 note は、今回候補でも `cha7.not1` としてChapter 7配下に配置。

## 深い階層サンプル

`runs/20260529-034208684_run-normalized-pics-part1-v1/SAMPLE_EXTRACT.md` より。chapter本文は可読性を優先して空欄化し、祖先ノード自体は省略していません。

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha7` | `chapter` | `CHAPTER` |  |
| 3 | `cha7.not1` | `note` | `note` | `Note: This Chapter deals with the responsibilities of manufacturers towards the Competent Regulatory Authorities with respect to the granting of marketing and manufacturing authorisations. It is not intended in any way to affect the respective liability of Contract Acceptors and Contract Givers to consumers; this is governed by other provisions of national law.` |

## 昇格境界

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/pics_pe00917_part1_20230825/` に複写します。

<!-- PR_BODY_FILE: runs/20260529-034208684_run-normalized-pics-part1-v1/PR.md -->
