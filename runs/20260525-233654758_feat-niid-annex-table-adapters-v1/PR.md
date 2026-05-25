<!-- PR_BODY_FILE: runs/20260525-233654758_feat-niid-annex-table-adapters-v1/PR.md -->

## まとめ

NIID別表・付表のうち、前RUNで列復元候補とした5件をtable nodeとして分離しました。これにより、これまでannex本文として保持していた表を `table_row` 粒度で追跡できるようになり、次のセル単位復元や候補表示判断へ進む土台ができます。

## 変更内容

- `niid_annex_table_adapter` を追加
- `付表2`, `付表3`, `付表4`, `別表7`, `別表10` をtable node化
- table単位に `reconstructed_columns` を追加
- row単位は `raw_line` として保持し、セル復元はwarning付きで次段階に残す
- RUNに正規化完成までの残課題を更新

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_niid_annex_inventory.py tests\test_text2ir_niid_pathogen_annex.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `13 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-233654758_feat-niid-annex-table-adapters-v1 --doc-id jp_niid_pathogen_safety_management_annex_tables_v1 --mode normal --out runs\20260525-233654758_feat-niid-annex-table-adapters-v1\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-233654758_feat-niid-annex-table-adapters-v1 --doc-id jp_niid_pathogen_safety_management_annex_tables_v1 --mode normal --out runs\20260525-233654758_feat-niid-annex-table-adapters-v1\special_structure_audit.md
```

結果: `pass`

## 補足

- このPRは開発PRであり、正式な正規化RUNではありません。
- `data/normalized/` への昇格は行っていません。
- 今回はtable node化までで、セル単位の完全な列復元は次段階です。
