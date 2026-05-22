# TABLE_NOTE_INVENTORY

## Phase 9B Summary

入力側のTable/Note候補を棚卸しする `qai_text2ir.table_note_inventory` を追加した。

実装方針:

- `Table 1:` / `Table 1.` / `Table 1 Maximum...` を table caption 候補として検出。
- `Note 1:` / `Note:` / `(a)` 等を note / footnote-like 候補として検出。
- Markdown tableは既存仕様を維持。
- 固定幅表は安全に列数が揃う場合のみ `table/table_header/table_row` 化。
- 不安定な固定幅表は `preformatted` + `kind_raw=possible_table` + `possible_plaintext_table_not_structured` として保持。
- 表下注記は可能な範囲で `note` として保持。

## Real Input Smoke

PIC/S Annex 1 full input smoke:

- input: `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`
- output: `out/20260522-130045_text2ir-final-goal-closure/phase9b_smoke_annex1_v3/`
- result: strict exit 0
- observed IR counts: `preformatted=4`, `note=9`

この時点では、Annex 1の複雑なPDF由来固定幅表は安全な `table_row` 化ではなく、`possible_table` として保持している。これは「黙殺しない」ことを優先する判断である。

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_table_note_real_samples.py tests\test_table_note_inventory.py tests\test_markdown_table_parsing.py tests\test_text2ir_goal_check.py
```

Result:

- `20 passed`
