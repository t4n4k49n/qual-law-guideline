<!-- PR_BODY_FILE: runs/20260523-123752346_feat-who-lbm-general-tables/PR_BODY.md -->

## まとめ

WHO LBM 3rd の一般表・図を構造化し、Chapter 8 の専用サーベイ表とあわせて、実文書内の主要な特殊構造が promotion ゲートで未解決扱いにならない状態にしました。これにより、表行をチェックリスト候補として安定して扱える範囲が広がり、本文に混ざっていた表・図キャプション由来のノイズも低減します。

## 変更内容

- `who_lbm_general_tables` パーサーを追加し、Table 1-4, 8-15 を `table` / `table_header` / `table_row` / `note` に正規化
- Figure 1-12 を `figure` ノードとして構造化し、図キャプションやFigure 10の図面テキスト層が通常本文に残らないよう補正
- WHO LBM v4 プロファイルで一般表・図パーサーを有効化し、`figure` を許可構造に追加
- Chapter 8 の Table 5-7 は既存の `who_lbm_chap8_survey` パーサーで維持
- 特殊構造監査で、構造化済みのChapter 8サーベイ表を元CHECKED ITEM行だけで未解決扱いしないよう補正
- RUN記録とWHO LBM一般表・図レポートを追加

## 確認

- `python -m pytest -q`
  - `202 passed, 1 skipped`
- `python -m qai_text2ir.goal_check --bundle-dir out\20260523-123752346_feat-who-lbm-general-tables\after_who_lbm_v3 --doc-id who_lbm_3rd_2004_9241546506 --mode promotion`
  - `PASS`

## 出力

- `runs/20260523-123752346_feat-who-lbm-general-tables/RUN.md`
- `runs/20260523-123752346_feat-who-lbm-general-tables/WHO_LBM_GENERAL_TABLES_REPORT.md`
- `runs/20260523-123752346_feat-who-lbm-general-tables/WHO_LBM_GENERAL_TABLES_REPORT.json`
