# WHO LBM 3rd Annex固定幅表の再結合修正

## まとめ

WHO LBM 3rd の正規化前確認で見つかった、Annex 4/5 の大きな固定幅表が本文に残る問題を修正する。共通パーサーには触れず、WHO LBM専用後処理だけで `Table A4-1`、`Table A4-2`、`Table A5-1` をtableとして扱えるようにし、正規化候補のレビューで表構造を確認できる状態にする。

## 変更内容

- WHO LBM専用後処理にAnnex固定幅表3件の定義を追加。
- 固定幅表の視覚行を `table_row` として保持し、`raw_line` と分割済み `cells` を併記。
- caption行やページヘッダをtable rowから除外。
- 本文側から固定幅表本体を除去し、参照文だけを残す。
- Annex固定幅表の回帰テストを追加。

## 検証結果

- `pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_general_tables.py tests/test_who_lbm_chap8_survey_parser.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py -q`: `25 passed`
- strict bundle再生成: success
- `goal_check --mode promotion`: PASS（tables 18, table_rows 1054, figures 12, notes 14）
- `special_structure_audit --mode promotion`: pass（source_tables 18, generated_tables 18, unresolved_special_blocks 0）
- `tools/check_ir_structure.py`: OK

## 注意

このPRでは正規化候補と `data/normalized/` は変更しない。反映後にWHO LBM 3rdの正規化RUNを作り直す。

<!-- PR_BODY_FILE: runs/20260531-221603696_fix-who-lbm-annex-fixed-width-tables/PR.md -->
