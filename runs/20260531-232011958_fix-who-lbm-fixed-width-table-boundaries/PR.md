# WHO LBM固定幅表のカテゴリ行・終端検出修正

## まとめ

WHO LBM正規化候補の目検・表再結合確認で見つかった固定幅表の復元不具合を修正します。Table A4-2 のカテゴリ行が列境界で分割される問題と、Table A5-1 が索引行を表データとして巻き込む問題を解消し、レビュー時に原表へ戻して確認できる状態を改善します。

## 変更内容

- WHO LBM個別の固定幅表処理で、Table A4-2 のインデントなしカテゴリ行を1列目へ保持する指定を追加
- 固定幅表の終端検出を正規化済み prefix 判定に変更し、`Index` を終端として検出できるよう修正
- 回帰テストに Table A4-2 のカテゴリ行復元と Table A5-1 の索引巻き込み防止を追加

## 検証

- `python -m pytest tests/test_who_lbm_general_tables.py -q`
  - `12 passed`
- `python -m pytest tests/test_who_lbm_general_tables.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_v3_skip_blocks.py tests/test_who_lbm_v2_drop_toc_and_annex_dedupe.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_chap8_survey_parser.py tests/test_text2ir_who_lbm_3rd.py -q`
  - `31 passed`

## 対象外

- `data/normalized/` への昇格は含めない
- 正規化候補の再生成は含めない
- 共通パーサの変更は含めない

<!-- PR_BODY_FILE: runs/20260531-232011958_fix-who-lbm-fixed-width-table-boundaries/PR.md -->
