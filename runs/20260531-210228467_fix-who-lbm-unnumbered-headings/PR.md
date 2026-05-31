# WHO LBM 3rd 項番なしheading修正

## まとめ

WHO LBM 3rd の正規化前チェックで見つかった、項番なし小見出しが章本文に混ざる問題を修正する。`Code of practice` や `Access` などを `section` として扱えるようにし、正式な正規化RUNへ進む前に、見出しと配下項目の関係をレビューしやすい構造へ整える。

## 変更内容

- `who_lbm_3rd_default_v4` で `section` を構造種別として許可。
- WHO LBM 3rd の既知の項番なし小見出しを `section.heading` として認識。
- `section` 配下に番号付き `item` が入ることをテストで確認。
- table/figureの正規化後処理を `section` 配下にも適用。
- Figure 1の固定幅表示をfigure nodeへ寄せ、Access本文から除去。
- 大文字小文字を区別して見出し検出し、表セル内の語句を誤ってheading化しないように調整。

## 検証結果

- `pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_general_tables.py tests/test_who_lbm_chap8_survey_parser.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py -q`: `24 passed`
- strict bundle再生成: success
- `goal_check --mode promotion`: PASS（tables 15, table_rows 210, figures 12, notes 14, unresolved errors none）
- `special_structure_audit --mode promotion`: pass（unresolved_special_blocks 0）
- `tools/check_ir_structure.py`: OK

## 注意

このPRでは正規化候補と `data/normalized/` は変更しない。反映後にWHO LBM 3rdの正規化RUNを作り直し、表・note・項番なしheading・不要改行/スペースを再確認する。代表箇所として、章3の `Access` / `Personal protection`、Figure 1、Annex 4の表セル誤heading化がないことは確認済み。

<!-- PR_BODY_FILE: runs/20260531-210228467_fix-who-lbm-unnumbered-headings/PR.md -->
