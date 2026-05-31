# WHO LBM Table A4-2 column boundary fix

- run_id: `20260531-233058086_fix-who-lbm-a4-2-column-boundary`
- branch: `fix/who-lbm-a4-2-column-boundary`
- target: WHO Laboratory Biosafety Manual, 3rd ed.

## 背景

正規化RUN `20260531-232632935_run-normalized-who-lbm-3rd-v7` の表再結合確認で、Table A4-2 に残存する固定幅列境界ずれを確認した。

- `Fire in flame            Incorrect reassembly of ...` が `Fire in flame            I | ncorrect reassembly of | ...` に分割されていた。
- `Explosion in domestic-    Dangerous chemical not        • Store...` が `Dangerous chemical not        • | Store...` に分割されていた。

このため正規化RUNは停止し、WHO LBM個別パーサの修正RUNとして切り出した。

## 変更内容

- Table A4-2 専用の固定幅 slice を `(0, 26), (26, 57), (57, None)` から `(0, 25), (25, 56), (56, None)` に調整した。
- Table A4-2 のカテゴリ行保持、A5-1 の終端検出など既存のWHO LBM個別処理は維持した。
- 共通パーサには触れていない。

## 検証

- `python -m pytest tests/test_who_lbm_general_tables.py -q`
  - `12 passed`
- `python -m pytest tests/test_who_lbm_general_tables.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_v3_skip_blocks.py tests/test_who_lbm_v2_drop_toc_and_annex_dedupe.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_chap8_survey_parser.py tests/test_text2ir_who_lbm_3rd.py -q`
  - `31 passed`

## 確認観点

- Table A4-2 `Explosion in domestic-` 行が `Dangerous chemical not` / `• Store low-flashpoint solvents` に分かれること。
- Table A4-2 `Fire in flame` 行が `Incorrect reassembly of` / `• Train and supervise staff.` に分かれること。
- Table A4-2 のカテゴリ行 `Faulty design or construction` / `Lack of proper maintenance` が単一セル行として維持されること。
