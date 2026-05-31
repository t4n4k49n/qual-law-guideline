# WHO LBM fixed-width table boundary fix

- run_id: `20260531-232011958_fix-who-lbm-fixed-width-table-boundaries`
- branch: `fix/who-lbm-fixed-width-table-boundaries`
- target: WHO Laboratory Biosafety Manual, 3rd ed.

## 背景

正規化候補の目検・再結合確認で、固定幅表に次の不具合を確認した。

- Table A4-2 のカテゴリ行 `Faulty design or construction` が固定幅スライスで `Faulty design or construct | ion |` に分割されていた。
- Table A5-1 が本文末尾の `Index` を終端として認識できず、索引行を表データとして巻き込んでいた。

このため正規化RUNは進めず、WHO LBM個別パーサの修正RUNとして切り出した。

## 変更内容

- `RawFixedWidthTableSpec` に、インデントなし・複数空白なしの単一カテゴリ行を1列目へ保持する指定を追加した。
- Table A4-2 のみ上記指定を有効化し、カテゴリ行を空セル付きの1行として保持するようにした。
- 表ブロックの終端検出を正規化済みテキストの prefix 判定に変更し、`INDEX` / `Index` の表記差で終端を見落とさないようにした。
- 共通パーサには触れていない。

## 検証

- `python -m pytest tests/test_who_lbm_general_tables.py -q`
  - `12 passed`
- `python -m pytest tests/test_who_lbm_general_tables.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_v3_skip_blocks.py tests/test_who_lbm_v2_drop_toc_and_annex_dedupe.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_chap8_survey_parser.py tests/test_text2ir_who_lbm_3rd.py -q`
  - `31 passed`

## 確認観点

- Table A4-2 の先頭行が `["Faulty design or construction", "", ""]` として復元されること。
- Table A5-1 に索引由来の `alarms 21, 60` が混入しないこと。
- 既存の Table A5-1 `Acetaldehyde` 行で `Can form explosive` が崩れないこと。
