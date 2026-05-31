<!-- PR_BODY_FILE: runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/PR.md -->

## まとめ

NIID病原体等安全管理規程の正規化候補をv10として作り直しました。別表5の表外にある運搬基準がIR上で表より前に出ていたため、原文の位置関係どおり、表の後ろに保持されるよう修正しています。

## 内容

- `runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/promotion_candidate/` を作成
- 対象原文: `https://www.niid.go.jp/niid/images/cepr/kanrikitei/Kanrikitei3_20240401.pdf`
- 別表テーブル化後の annex 直下 child を source locator の行番号で並べ、原文順を保持
- 別表5の順序を `ann5.tbl1` -> `ann5.not1` -> `ann5.not2` -> `ann5.not3` に修正
- `○ 運搬の基準（1種～4種病原体等）` 以降は table_row から除外し、表の後ろの `ann5.not3` として保持
- PDF抽出由来の孤立した `•` をnote化しないよう修正
- 再発防止として、表外運搬基準が表の後ろにあることと孤立 `•` がないことをテストで固定
- 誤った昇格PR `#226` はクローズ済み

## 深い階層サンプル

- `runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/SAMPLE_EXTRACT.md`
- target: `ann5.not3`
- path: `root` -> `ann5` -> `ann5.not3`

## 検証

- `.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_niid_pathogen_safety.py tests/test_niid_annex_table_cells.py tests/test_text2ir_niid_pathogen_annex.py tests/test_niid_annex_inventory.py -q`
  - `13 passed`
- `.\.venv\Scripts\python.exe -m pytest -q`
  - `257 passed, 1 skipped`
- `.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/promotion_candidate --doc-id jp_niid_pathogen_safety_management_20240401 --mode promotion --out runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/GOAL_CHECK.md`
  - PASS
- `.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/promotion_candidate --doc-id jp_niid_pathogen_safety_management_20240401 --mode promotion --format markdown --out runs/20260531-113511077_run-normalized-niid-pathogen-safety-v10/SPECIAL_STRUCTURE_AUDIT.md`
  - PASS
- `.\.venv\Scripts\python.exe tools\check_ir_structure.py runs\20260531-113511077_run-normalized-niid-pathogen-safety-v10\promotion_candidate`
  - PASS
- local path literal scan against the v10 run, parser code, and tests
  - no matches

## 注意

このPRでは `data/normalized/` は変更していません。承認後に昇格専用PRで反映します。
