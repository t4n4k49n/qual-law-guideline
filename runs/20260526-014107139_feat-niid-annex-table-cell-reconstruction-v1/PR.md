<!-- PR_BODY_FILE: runs/20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1/PR.md -->

## まとめ

NIID別表・付表について、安全に分割できる行へセル候補を付けたうえで、16件すべてのreadiness上の扱いを決め切りました。複雑表や折返し表は追加開発へ先送りせず、raw tableまたはannex textとして昇格候補に倒しています。

## 変更内容

- `niid_annex_table_adapter` にセル復元v1を追加
- 列数どおりに分割できる行へ `cells` / `columns` / `cell_reconstruction` を付与
- 分割不能行へ `fixed_width_cell_split_deferred` warningを付与
- 16件すべてに `normalization_readiness` を付与
- RUNに表ごとの復元行数、保留行数、昇格候補としての持ち方を記録

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_niid_annex_table_cells.py tests\test_text2ir_niid_pathogen_annex.py tests\test_niid_annex_inventory.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `15 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_readiness_v1 --mode normal --out runs\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_readiness_v1 --mode normal --out runs\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1\special_structure_audit.md
```

結果: `pass`

## 備考

- `付表2` は折返しが強く、raw table + 列スキーマで昇格候補に倒しています。
- `別表4`, `別表5`, `別表8` は複雑表adapter化を追加開発で引き延ばさず、raw annex textとして昇格候補に倒しています。
- `data/normalized/` への昇格は行っていません。
