<!-- PR_BODY_FILE: runs/20260525-225501792_feat-raw-line-table-column-restore-prototype/PR.md -->

## まとめ

6/7の主要表について、これまでの `raw_line` 保持から一歩進め、レビュー可能な列復元候補をIRに持たせました。raw rowとsource spanは維持したまま、復元できる意味単位を `reconstructed_records` として明示し、復元対象外の行はwarningで残すため、正式正規化へ進む前の確認がしやすくなります。

## 変更内容

- 原薬GMPガイドライン表1に列復元プロトタイプを追加
- 無菌操作法指針の表1/表2/表3に列復元プロトタイプを追加
- table nodeへ `reconstructed_columns` / `reconstructed_records` / `non_data_raw_rows` を追加
- table_row nodeへ `column_reconstruction_record_id` またはwarningを追加
- RUNに、正規化完成まで残る課題を文書別に整理

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_goal_check.py tests\test_special_structure_audit.py -q
```

結果: `23 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_api_gmp_guideline_column_restore_v2 --mode normal --out runs\20260525-225501792_feat-raw-line-table-column-restore-prototype\goal_check_api_gmp.md
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_aseptic_processing_guideline_column_restore_v2 --mode normal --out runs\20260525-225501792_feat-raw-line-table-column-restore-prototype\goal_check_aseptic.md
```

結果: どちらも `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_api_gmp_guideline_column_restore_v2 --mode normal --out runs\20260525-225501792_feat-raw-line-table-column-restore-prototype\special_structure_audit_api_gmp.md
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_aseptic_processing_guideline_column_restore_v2 --mode normal --out runs\20260525-225501792_feat-raw-line-table-column-restore-prototype\special_structure_audit_aseptic.md
```

結果: どちらも `pass`

## 補足

- このPRは開発PRであり、正式な正規化RUNではありません。
- `data/normalized/` への昇格は行っていません。
- 完全な表正規化ではなく、列復元候補をIRに持たせる段階です。
