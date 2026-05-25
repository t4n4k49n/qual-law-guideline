<!-- PR_BODY_FILE: runs/20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1/PR.md -->

## まとめ

NIID別表・付表のtable化済み5表について、安全に分割できる行だけセル候補を付けました。分割不能な行はraw rowとsource spanを維持してwarningを残すため、表の欠落防止とレビュー可能性を保ったまま、次の複数行record統合へ進めます。

## 変更内容

- `niid_annex_table_adapter` にセル復元v1を追加
- 列数どおりに分割できる行へ `cells` / `columns` / `cell_reconstruction` を付与
- 分割不能行へ `fixed_width_cell_split_deferred` warningを付与
- RUNに表ごとの復元行数、保留行数、次課題を記録

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_niid_annex_table_cells.py tests\test_text2ir_niid_pathogen_annex.py tests\test_niid_annex_inventory.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `14 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_cell_reconstruction_v1 --mode normal --out runs\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_cell_reconstruction_v1 --mode normal --out runs\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1\special_structure_audit.md
```

結果: `pass`

## 備考

- `付表2` は折返しが強く、今回の単純分割では0行復元です。RUNに次課題として記録しました。
- 複数行record統合と複雑表adapter化は次フェーズ以降です。
- `data/normalized/` への昇格は行っていません。
