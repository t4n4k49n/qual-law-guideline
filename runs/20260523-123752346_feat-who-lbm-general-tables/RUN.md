# RUN: 20260523-123752346_feat-who-lbm-general-tables

## Task

WHO Laboratory Biosafety Manual 3rd edition (`who_lbm_3rd_2004_9241546506`) について、Chapter 8 の専用サーベイ表以外に残っていた一般表・図を構造化する。

## Scope

- 対象プロンプト: `out/administrators-memos/20260523.........問題発展型特殊パーサー/106.WHO_LBM_一般表・図/codex_who_lbm_general_tables_prompt.md`
- 入力: `data/human-readable/who/WHO_LBM_3rd.txt`
- プロファイル: `src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml`
- 実出力: `out/20260523-123752346_feat-who-lbm-general-tables/after_who_lbm_v3/`

## Implementation

- `who_lbm_general_tables` 後処理パーサーを追加し、WHO LBM v4 プロファイルでのみ有効化した。
- Table 1-4, 8-15 を `table` / `table_header` / `table_row` / `note` に正規化した。
- Figure 1-12 を `figure` に正規化し、本文側に残っていた図キャプション・図面テキスト層を除去した。
- Chapter 8 の Table 5-7 は既存の `who_lbm_chap8_survey` 専用パーサーのまま維持した。
- 特殊構造監査で、既に Chapter 8 サーベイ表として構造化済みの CHECKED ITEM ヘッダを未解決扱いしないよう補正した。

## Verification

- `python -m pytest tests\test_who_lbm_general_tables.py tests\test_who_lbm_chap8_survey_parser.py tests\test_special_structure_audit.py -q`
  - `18 passed`
- `python -m pytest tests\test_who_lbm_general_tables.py tests\test_special_structure_audit.py -q`
  - `16 passed`
- `python -m qai_text2ir.goal_check --bundle-dir out\20260523-123752346_feat-who-lbm-general-tables\after_who_lbm_v3 --doc-id who_lbm_3rd_2004_9241546506 --mode promotion`
  - `PASS`

## Outputs

- `runs/20260523-123752346_feat-who-lbm-general-tables/WHO_LBM_GENERAL_TABLES_REPORT.md`
- `runs/20260523-123752346_feat-who-lbm-general-tables/WHO_LBM_GENERAL_TABLES_REPORT.json`

