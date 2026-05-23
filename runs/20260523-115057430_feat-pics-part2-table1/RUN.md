# RUN: PICS Part II Table 1

- run_id: `20260523-115057430_feat-pics-part2-table1`
- branch: `feat/pics-part2-table1`
- prompt: `out/administrators-memos/20260523.........問題発展型特殊パーサー/105.PICS_PartII_Table1/codex_pics_part2_table1_prompt.md`
- target: `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt`

## 実施内容

- PIC/S Part II の `Table 1: Application of this Guide to API Manufacturing` を専用正規化で構造化した。
- `pics_part2_default_v1` に限定して有効化し、Table 1が `cha1.sec1_2.text` に吸収されないようにした。
- Table 1を `table` / `table_header` / `table_row` / `note` として保持した。
- 製造タイプ7行と、`Increasing GMP requirements` をtable annotation noteとして保持した。
- PDFのgrey shadingはテキスト層から信頼復元できないため、`shading_reconstructed: false` と注記をtable dataへ記録した。

## 生成・監査結果

- Part II 再生成先: `out/20260523-115057430_feat-pics-part2-table1/after_part2`
- special structure audit: pass
  - generated_tables: 1
  - generated_rows: 7
  - unresolved_special_blocks: 0
- GOAL check: pass
  - table: 1
  - table_header: 1
  - table_row: 7
  - warnings: none

## 成果物

- `PICS_PART2_TABLE1_REPORT.md`
- `PICS_PART2_TABLE1_REPORT.json`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `SPECIAL_STRUCTURE_AUDIT.json`
- `GOAL_CHECK_RESULT.md`

## テスト

- `python -m pytest tests/test_pics_part2_table1.py -q`
  - 5 passed
- `python -m pytest tests/test_pics_annex1_tables.py tests/test_pics_annex2a_structures.py tests/test_pics_part2_table1.py -q`
  - 17 passed
- `python -m pytest -q`
  - 192 passed, 1 skipped
