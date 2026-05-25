<!-- PR_BODY_FILE: runs/20260526-011550152_feat-table-record-review-6-7/PR.md -->

## まとめ

6/7の表record候補について、正式なtable_row昇格前のレビュー判断をIRとRUN成果物に残しました。raw rowとsource spanは維持しつつ、候補粒度を `reconstructed_record` として明示したため、正規化RUN readinessで昇格可否を判断しやすくなります。

## 変更内容

- 6 表1、7 表1/2/3に `record_review` メタデータを追加
- 各 `reconstructed_records` に `review_status` / `promotion_status` を追加
- `table_record_review_6_7` inventory CLIを追加
- RUNに、昇格延期理由、残課題、検証結果を記録

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_table_record_review_6_7.py tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_goal_check.py tests\test_special_structure_audit.py -q
```

結果: `24 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_api_gmp_guideline_record_review_v1 --mode normal --out runs\20260526-011550152_feat-table-record-review-6-7\goal_check_api_gmp.md
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_aseptic_processing_guideline_record_review_v1 --mode normal --out runs\20260526-011550152_feat-table-record-review-6-7\goal_check_aseptic.md
```

結果: どちらも `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_api_gmp_guideline_record_review_v1 --mode normal --out runs\20260526-011550152_feat-table-record-review-6-7\special_structure_audit_api_gmp.md
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_aseptic_processing_guideline_record_review_v1 --mode normal --out runs\20260526-011550152_feat-table-record-review-6-7\special_structure_audit_aseptic.md
```

結果: どちらも `pass`

## 備考

- 正式な `table_row` 昇格はまだ行っていません。
- `data/normalized/` への昇格は行っていません。
- 次は計画Lの `feat/niid-annex-table-cell-reconstruction-v1` が候補です。
