<!-- PR_BODY_FILE: runs/20260526-040709227_feat-mhlw-csv-annex2-semantic-records/PR.md -->

## まとめ

CSVガイドライン別紙2のHTML表を、表示行の保持だけでなく、カテゴリ単位の意味recordとしてレビューできる形に進めました。記号値と脚注番号を分解し、カテゴリ3の複数表示行も1カテゴリrecordに束ねたため、正式正規化RUNで候補粒度を判断しやすくなります。

## 変更内容

- `mhlw_csv_annex2_table_adapter` に semantic record生成を追加
- `カテゴリ分類表` をカテゴリ単位5 recordへ分解
- `◎` / `○` / `△` / `―` を `status` / `meaning` / `footnote_refs` に分解
- 表2 `本ガイドラインの対象外` を1 semantic recordとして保持
- 元のHTML table row、`cells`、列スキーマ、source spanは維持
- semantic inventoryとRUN記録を追加

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_mhlw_csv_annex2_tables.py tests\test_text2ir_csv_guideline.py tests\test_mhlw_csv_annex_source_recovery.py tests\test_mhlw_csv_annexes.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `17 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-040709227_feat-mhlw-csv-annex2-semantic-records --doc-id jp_mhlw_csv_guideline_annex2_semantic_v1 --mode normal --out runs\20260526-040709227_feat-mhlw-csv-annex2-semantic-records\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-040709227_feat-mhlw-csv-annex2-semantic-records --doc-id jp_mhlw_csv_guideline_annex2_semantic_v1 --mode normal --out runs\20260526-040709227_feat-mhlw-csv-annex2-semantic-records\special_structure_audit.md
```

結果: `pass`

## 残る課題

- CSV `別紙1` は画像参照のままで、OCR/転記方針決定が次フェーズです。
- semantic recordsを正式なDQ候補粒度にするかは、正規化RUN readinessで判断します。
