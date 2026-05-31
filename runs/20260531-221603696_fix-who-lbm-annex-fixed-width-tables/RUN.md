# WHO LBM Annex固定幅表の再結合修正

- run_id: `20260531-221603696_fix-who-lbm-annex-fixed-width-tables`
- branch: `fix/who-lbm-annex-fixed-width-tables`
- 対象: WHO Laboratory Biosafety Manual, 3rd ed.
- doc_id: `who_lbm_3rd_2004_9241546506`

## 目的

WHO LBM 3rd の正規化RUN目検で、Annex 4/5 の固定幅表が普通の本文に残っていることを確認した。
共通パーサーには触れず、WHO LBM専用後処理だけで `Table A4-1`、`Table A4-2`、`Table A5-1` を table node として再結合する。

## 変更

- `src/qai_text2ir/who_lbm_general_tables.py` のWHO LBM専用後処理に、Annex固定幅表3件の定義を追加。
- 固定幅表は視覚行を `table_row` として保持し、`raw_line` と `cells` を併記する。
- caption行やページヘッダはtable rowから除外する。
- 元本文から固定幅表本体を除去し、参照文だけを残す。
- `tests/test_who_lbm_general_tables.py` にAnnex固定幅表の回帰テストを追加。

## 検証

```text
python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_who_lbm_general_tables.py tests/test_who_lbm_chap8_survey_parser.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py -q
25 passed
```

```text
python -m qai_text2ir.cli bundle ... --strict --out-dir out/20260531-214027995_run-normalized-who-lbm-3rd-v2/annex_table_fix_check_20260531-220500
success
```

```text
python -m qai_text2ir.goal_check --bundle-dir out/20260531-214027995_run-normalized-who-lbm-3rd-v2/annex_table_fix_check_20260531-220500 --doc-id who_lbm_3rd_2004_9241546506 --mode promotion
PASS
tables: 18
table_rows: 1054
figures: 12
notes: 14
```

```text
python -m qai_text2ir.special_structure_audit --bundle-dir out/20260531-214027995_run-normalized-who-lbm-3rd-v2/annex_table_fix_check_20260531-220500 --doc-id who_lbm_3rd_2004_9241546506 --mode promotion --format markdown
pass
source_tables: 18
generated_tables: 18
generated_rows: 1054
generated_figures: 12
unresolved_special_blocks: 0
```

```text
python tools/check_ir_structure.py out/20260531-214027995_run-normalized-who-lbm-3rd-v2/annex_table_fix_check_20260531-220500
[OK] no structure problems found
```

## 目検確認

- `ann4.tbla4_1` が `Table A4-1. Equipment and operations that may create hazards` として生成されることを確認。
- `ann4.tbla4_2` が `Table A4-2. Common causes of equipment-related accidents` として生成されることを確認。
- `ann5.tbla5_1` が `Table A5-1. Chemicals: hazards and precautions` として生成されることを確認。
- `raw_line: Hypodermic ...`、`raw_line: Electrical fires ...`、`raw_line: Acetaldehyde ...`、`raw_line: Acetic acid ...` がtable row側に保持されることを確認。
- caption行がtable rowの先頭に混入しないことをテストで確認。

## 正規化RUNへの影響

このPRは通常修正であり、`data/normalized/` と正規化候補は変更しない。
このPR反映後、WHO LBM 3rd の正規化RUNを作り直す。
