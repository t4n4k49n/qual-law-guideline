# RUN: PICS Annex 1 Tables 1-6

- run_id: `20260523-101731707_feat-pics-annex1-tables`
- branch: `feat/pics-annex1-tables`
- prompt: `out/administrators-memos/20260523.........問題発展型特殊パーサー/103.PICS_Annex1_Talbes1-6/codex_pics_annex1_tables_prompt.md`
- target: `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`

## 実施内容

- PIC/S Annex 1 の Table 1-6 を `table` / `table_header` / `table_row` / `note` として構造化する専用正規化を追加した。
- `pics_annex1_default_v2` に限定して有効化し、通常の汎用テーブル検出結果を対象表だけ置換するようにした。
- `pics_annexes_default_v3` の subtree refine 内でも Annex 1 子プロファイルの同正規化が動くようにし、複合Annex再生成でも Table 1-6 が構造化されるようにした。
- Table 3/4 は本文段落内に混入していた表キャプションと固定幅本文を分離し、操作例を grade-operation の table_row として保持した。
- Table 1/2/5/6 は grade A-D、測定単位、注記/脚注を保持した。

## 生成・監査結果

- Annex 1 再生成先: `out/20260523-101731707_feat-pics-annex1-tables/pics_pe00917_annex1_20230825_after2`
- 複合Annex再生成先: `out/20260523-101731707_feat-pics-annex1-tables/pics_pe00917_annexes_20230825_after2`
- Annex 1 special structure audit: pass
  - source_tables: 6
  - generated_tables: 6
  - generated_rows: 35
  - unresolved_special_blocks: 0
- Annex 1 GOAL check: pass
  - table: 6
  - table_header: 6
  - table_row: 35
  - warnings: none
- 複合Annex GOAL check: pass
- 複合Annex special structure audit: warn
  - Annex 1 Table 1-6 は構造化済み
  - 残る unresolved は Annex 2A/2B/3/7/14/19 と figure 系で、今回対象外

## 成果物

- `PICS_ANNEX1_TABLES_REPORT.md`
- `PICS_ANNEX1_TABLES_REPORT.json`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `SPECIAL_STRUCTURE_AUDIT.json`
- `GOAL_CHECK_RESULT.md`
- `COMBINED_ANNEXES_SPECIAL_STRUCTURE_AUDIT.md`
- `COMBINED_ANNEXES_SPECIAL_STRUCTURE_AUDIT.json`
- `COMBINED_ANNEXES_GOAL_CHECK_RESULT.md`

## テスト

- `python -m pytest tests/test_pics_annex1_tables.py tests/test_pics_annexes_refine_v3_fallback.py tests/test_pics_annexes_refine_v2.py -q`
  - 12 passed
- `python -m pytest -q`
  - 183 passed, 1 skipped
