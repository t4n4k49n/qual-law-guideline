<!-- PR_BODY_FILE: runs/20260525-231917460_feat-niid-annex-table-inventory/PR.md -->

## まとめ

病原体等安全管理規程の別表・付表について、列復元に進む前の表別inventoryを追加しました。16個の別表・付表を、列復元候補、複雑候補、列復元対象外、番号/節構造化候補に分けたため、次のadapter実装で対象範囲を絞り、無理な個別最適を避けやすくなります。

## 変更内容

- `niid_annex_inventory` を追加
- NIID別表・付表16件の形式分類をJSON/Markdownで出力
- 列復元候補と複雑候補を分離
- RUNに、正規化完成まで残る課題と次PRの対象候補を記録

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_niid_annex_inventory.py tests\test_text2ir_niid_pathogen_annex.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `12 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-231917460_feat-niid-annex-table-inventory --doc-id jp_niid_pathogen_safety_management_annex_inventory_v1 --mode normal --out runs\20260525-231917460_feat-niid-annex-table-inventory\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-231917460_feat-niid-annex-table-inventory --doc-id jp_niid_pathogen_safety_management_annex_inventory_v1 --mode normal --out runs\20260525-231917460_feat-niid-annex-table-inventory\special_structure_audit.md
```

結果: `pass`

## 補足

- このPRは開発PRであり、正式な正規化RUNではありません。
- `data/normalized/` への昇格は行っていません。
- このPRではtable adapter実装には入らず、次PRの対象を絞るところまでです。
