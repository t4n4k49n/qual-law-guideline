# WHO LBM Table A4-2の固定幅列境界修正

## まとめ

WHO LBM正規化候補の表再結合確認で残っていた Table A4-2 の列境界ずれを修正します。固定幅表を人が原表に近い形で確認できるようにし、正規化RUNのレビュー品質を保つための個別パーサ修正です。

## 変更内容

- Table A4-2 専用の固定幅 slice を1桁調整
- `Explosion in domestic-` 行の原因列と対策列の分割を修正
- `Fire in flame` 行の原因列と対策列の分割を修正
- 回帰テストに上記2行の再結合確認を追加

## 検証

- `python -m pytest tests/test_who_lbm_general_tables.py -q`
  - `12 passed`
- `python -m pytest tests/test_who_lbm_general_tables.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_v3_skip_blocks.py tests/test_who_lbm_v2_drop_toc_and_annex_dedupe.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_chap8_survey_parser.py tests/test_text2ir_who_lbm_3rd.py -q`
  - `31 passed`

## 対象外

- `data/normalized/` への昇格は含めない
- 正規化候補の再生成は含めない
- 共通パーサの変更は含めない

<!-- PR_BODY_FILE: runs/20260531-233058086_fix-who-lbm-a4-2-column-boundary/PR.md -->
