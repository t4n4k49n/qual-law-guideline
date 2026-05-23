# まとめ

text2ir の出力に表・図・チェックリスト・フォーム相当の特殊構造が未解決のまま残っている場合に、promotion/release を通過できない全体ゲートを追加しました。個別パーサーで直す前段として、問題が通常段落や `preformatted` に隠れたまま見落とされるリスクを可視化し、正式化判断の品質を安定させます。

## 変更内容

- `qai_text2ir.special_structure_audit` を追加し、source/IR 双方から特殊構造を監査
  - source 側: `Table N`、`Figure N`、`CHECKED ITEM`、`YES NO N/A COMMENTS`、固定幅表候補を検出
  - IR 側: `table`、`table_header`、`table_row`、`figure`、`preformatted`、`note` を集計
  - 未解決ブロックを `SPECIAL_STRUCTURE_AUDIT.json` / `SPECIAL_STRUCTURE_AUDIT.md` として出力
- `goal_check` に監査を接続
  - 通常モードでは warning
  - `promotion` / `release` では `special_structure_unresolved` error として fail
- WHO LBM 3rd、PIC/S Annex 1、PIC/S Annex 2A、PIC/S Part II 相当の回帰テストを追加
- 実文書に対する監査レポートを run 成果物として追加

## 実文書監査結果

現行 text2ir 出力では以下の未解決特殊構造が残っており、promotion/release ではブロック対象になります。

| doc_id | source_tables | source_figures | generated_tables | generated_rows | generated_figures | unresolved_special_blocks | status |
|---|---:|---:|---:|---:|---:|---:|---|
| pics_annex1 | 6 | 0 | 0 | 0 | 0 | 14 | warn |
| pics_annex2a | 1 | 2 | 0 | 0 | 0 | 8 | warn |
| pics_part2 | 2 | 0 | 0 | 0 | 0 | 3 | warn |
| who_lbm_3rd | 18 | 12 | 0 | 0 | 0 | 43 | warn |

## 確認

- `python -m pytest tests/test_special_structure_audit.py -q`
- `python -m pytest tests/test_text2ir_audit_report.py tests/test_text2ir_goal_check.py tests/test_table_note_inventory.py tests/test_special_structure_audit.py -q`
- `python -m pytest -q`

最終結果: `175 passed, 1 skipped`

<!-- PR_BODY_FILE: runs/20260523-093052469_feat-special-structure-global-gate/PR.md -->
