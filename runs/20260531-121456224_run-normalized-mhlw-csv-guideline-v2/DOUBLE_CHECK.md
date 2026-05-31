# CSVガイドライン ダブルチェック

- run_id: `20260531-121456224_run-normalized-mhlw-csv-guideline-v2`
- 対象: `jp_mhlw_csv_guideline_20101021`
- 正本候補: `runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/promotion_candidate/`

## 1回目チェック

| 観点 | 結果 | 確認内容 |
|---|---|---|
| heading | OK | 章 `1`-`10`、別紙 `別紙1`→`別紙2` が原文順。`1.1` / `1.3` / `4.1` などの小見出しを `heading` に分離し、本文先頭から除去。 |
| 表 | OK | 別紙2に `カテゴリ分類表`、`本ガイドラインの対象外` の2表を配置。表1は7 display rows、表2は1 display row。 |
| 結合セル | OK | カテゴリ3は display row `4` と `5` を `csv_annex2.category3` に対応付け、semantic record の `raw_row_nums` は `[4, 5]`。 |
| note / 表外 | OK | 別紙1は `html_image_reference` として画像参照のみ、別紙2は page2 HTML 表を別紙2配下に配置。表外テキストの先頭混入なし。 |
| 不要改行・スペース | OK | paragraph の `heading_prefix_left_in_text` は0件。表行 `text` の空セル区切りのみ確認対象外の表示用スペースとして残存。 |

## 2回目チェック

| 観点 | 結果 | 確認内容 |
|---|---|---|
| top-level order | OK | `top_chapters`: `1`-`10`、`annex_order`: `別紙1`, `別紙2`。 |
| heading split | OK | `cha1.p1_1.heading=目的`、`cha4.p4_1.heading=開発計画に関する文書の作成`。本文はいずれも見出し語で始まらない。 |
| table order | OK | `annex2.tbl1` → `annex2.tbl2`。 |
| merged cell semantics | OK | `annex2.tbl1.tblh.tblr4` と `annex2.tbl1.tblh.tblr5` はともに `csv_annex2.category3`。 |
| source artifact | OK | `manifest.yaml` のローカル絶対パスを相対表記へ修正済み。 |

## 検証コマンド

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_csv_guideline.py tests/test_mhlw_csv_annex2_tables.py tests/test_mhlw_csv_annexes.py tests/test_mhlw_csv_annex_source_recovery.py tests/test_candidate_visibility_profiles_6_9.py -q
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/promotion_candidate --doc-id jp_mhlw_csv_guideline_20101021 --mode promotion --out runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/GOAL_CHECK.md
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/promotion_candidate --doc-id jp_mhlw_csv_guideline_20101021 --mode promotion --format markdown --out runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/SPECIAL_STRUCTURE_AUDIT.md
.\.venv\Scripts\python.exe tools\check_ir_structure.py runs\20260531-121456224_run-normalized-mhlw-csv-guideline-v2\promotion_candidate
```

結果:

- focused tests: `17 passed`
- goal check: `PASS`
- special structure audit: `pass`
- IR structure: `[OK] no structure problems found`
