<!-- PR_BODY_FILE: runs/20260526-002546060_feat-mhlw-csv-annex2-table-parser/PR.md -->

## まとめ

CSVガイドライン別紙2の表本体を、公式page2 HTMLからIRのtable/table_rowとして取り込めるようにしました。これにより、別紙2は「表題だけ」ではなく、カテゴリ分類表と対象外表を列スキーマ付きでレビューできる状態になり、次の意味値分解・脚注分解へ進めます。

## 変更内容

- 公式page2 HTMLを `data/human-readable/mhlw/csv_guideline/00tb6573_page2.html` として追加
- CSV専用 `mhlw_csv_annex2_table_adapter` を追加
- `jp_mhlw_csv_guideline_v1` からpage2 HTMLを明示参照
- `別紙2` 配下に `table` 2件、`table_row` 8件を生成
- RUNに、今回入れない課題と正規化完成までの残課題を記録

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_mhlw_csv_annex2_tables.py tests\test_mhlw_csv_annex_source_recovery.py tests\test_mhlw_csv_annexes.py tests\test_text2ir_csv_guideline.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `16 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-002546060_feat-mhlw-csv-annex2-table-parser --doc-id jp_mhlw_csv_guideline_annex2_table_v1 --mode normal --out runs\20260526-002546060_feat-mhlw-csv-annex2-table-parser\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-002546060_feat-mhlw-csv-annex2-table-parser --doc-id jp_mhlw_csv_guideline_annex2_table_v1 --mode normal --out runs\20260526-002546060_feat-mhlw-csv-annex2-table-parser\special_structure_audit.md
```

結果: `pass`

## 備考

- 公式page2: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=2`
- `data/normalized/` への昇格は行っていません。
- 別紙1画像のOCR、別紙2の意味値分解・脚注分解・カテゴリ単位record統合は次フェーズ以降です。
