# PIC/S Annex 15 正規化RUN v1

## まとめ

PIC/S PE 009-17 Annex 15 を正式版昇格候補として生成しました。前段PRで見出し誤結合を校正済みであり、今回の候補でも `PROCESS VALIDATION` と `General` が分離されていること、Table/Warning由来の未解決構造が残っていないこと、DQチェックシート向けの候補設定が成立していることを確認しています。

## 対象

| 項目 | 内容 |
|---|---|
| doc_id | `pics_pe00917_annex15_20230825` |
| source URL | `https://picscheme.org/docview/8881` |
| 入力 | `data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt` |
| parser profile | `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml` |
| 正本候補 | `runs/20260529-054601644_run-normalized-pics-annex15-v1/promotion_candidate/` |

## 検証結果

| 確認 | 結果 |
|---|---|
| strict bundle generation | pass |
| promotion goal check | pass |
| schema | `qai.regdoc_ir.v4` |
| nodes | 142 |
| source span coverage | 1.0 |
| goal check errors | none |
| goal check warnings | none |
| manifest quality warnings | none |
| IR warning metadata scan | none |
| special structure audit | pass |
| focused tests | `4 passed` |
| full tests | `252 passed, 1 skipped` |

## Table / Warning 目検確認

- Table count: 0。
- Table row count: 0。
- Note count: 0。
- Source table-like blocks: 0、unresolved special blocks: 0。
- Warning系は strict / promotion goal / IR metadata scan で該当なし。
- 前段レビューPR `#210` の校正結果として、今回候補でも `ann15.sec5` は `heading: PROCESS VALIDATION`、`text: General` に分離。

## 深い階層サンプル

`runs/20260529-054601644_run-normalized-pics-annex15-v1/SAMPLE_EXTRACT.md` より。最大深度5のitemを抽出し、祖先ノード自体は省略していません。

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann15` | `annex` | `ANNEX` | `QUALIFICATION AND VALIDATION` |
| 3 | `ann15.sec5` | `section` | `5.` | `PROCESS VALIDATION` |
| 4 | `ann15.sec5.p5_22` | `paragraph` | `5.22` | `Process validation protocols should include, but are not limited to the following:` |
| 5 | `ann15.sec5.p5_22.ivi` | `item` | `vi.` | `List of the equipment/facilities to be used (including measuring/monitoring/recording equipment) together with the calibration status;` |

## 昇格境界

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/pics_pe00917_annex15_20230825/` に複写します。

<!-- PR_BODY_FILE: runs/20260529-054601644_run-normalized-pics-annex15-v1/PR.md -->
