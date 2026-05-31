<!-- PR_BODY_FILE: runs/20260531-023248221_run-normalized-niid-pathogen-safety-v8/PR.md -->

## まとめ

NIID病原体等安全管理規程の正規化候補をv8として作り直しました。別表4/5について、PDF上の結合セルや表外箇条書きがIRデータとして誤って欠落・混入しないよう、再結合Markdownで確認できる形にしています。

## 内容

- `runs/20260531-023248221_run-normalized-niid-pathogen-safety-v8/promotion_candidate/` を作成
- 別表4の `実験室` / `実験室内` 結合セル値を全BSL列へ複製
- 別表5の `○ 運搬の基準（1種～4種病原体等）` 以降をtable_rowから除外
- 運搬基準本文を `ann5.not3` のnoteとして保持
- `TABLE4_5_RECONSTRUCTION_CHECK.md` に表4/5の再結合Markdownを収録
- 再発防止として、表5に `運搬の基準` がtable_rowとして混入しないテストを追加

## 検証

- `.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_niid_pathogen_safety.py tests/test_niid_annex_table_cells.py tests/test_text2ir_niid_pathogen_annex.py tests/test_niid_annex_inventory.py -q`
  - `13 passed`
- `.\.venv\Scripts\python.exe -m pytest -q`
  - `257 passed, 1 skipped`
- `.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir runs/20260531-023248221_run-normalized-niid-pathogen-safety-v8/promotion_candidate --doc-id jp_niid_pathogen_safety_management_20240401 --mode promotion --out runs/20260531-023248221_run-normalized-niid-pathogen-safety-v8/GOAL_CHECK.md`
  - PASS
- `.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir runs/20260531-023248221_run-normalized-niid-pathogen-safety-v8/promotion_candidate --doc-id jp_niid_pathogen_safety_management_20240401 --mode promotion --format markdown --out runs/20260531-023248221_run-normalized-niid-pathogen-safety-v8/SPECIAL_STRUCTURE_AUDIT.md`
  - PASS
- `.\.venv\Scripts\python.exe tools\check_ir_structure.py runs\20260531-023248221_run-normalized-niid-pathogen-safety-v8\promotion_candidate`
  - PASS
- local path literal scan against the v8 run, parser code, and tests
  - no matches

## 注意

このPRでは `data/normalized/` は変更していません。承認後に昇格専用PRで反映します。
