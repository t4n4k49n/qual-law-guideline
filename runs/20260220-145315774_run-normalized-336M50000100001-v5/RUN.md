# RUN: 20260220-145315774_run-normalized-336M50000100001-v5

## 1. 対象
- 種別: 正規化RUN
- doc_id: `jp_egov_336M50000100001_20260501_507M60000100117`
- 入力XML: `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336M50000100001_20260501_507M60000100117\336M50000100001_20260501_507M60000100117.xml`
- e-Gov URL: `https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117`

## 2. 実行
- 実行コマンド:
  - `./.venv/Scripts/python.exe -m qai_xml2ir.cli --input %USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336M50000100001_20260501_507M60000100117\336M50000100001_20260501_507M60000100117.xml --out-dir out/20260220-145315774_run-normalized-336M50000100001-v5 --doc-id jp_egov_336M50000100001_20260501_507M60000100117 --retrieved-at 2026-02-20 --source-url https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117 --emit-only all`
- 出力:
  - `out/20260220-145315774_run-normalized-336M50000100001-v5/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_ir.yaml`
  - `out/20260220-145315774_run-normalized-336M50000100001-v5/jp_egov_336M50000100001_20260501_507M60000100117.parser_profile.yaml`
  - `out/20260220-145315774_run-normalized-336M50000100001-v5/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_profile.yaml`
  - `out/20260220-145315774_run-normalized-336M50000100001-v5/jp_egov_336M50000100001_20260501_507M60000100117.meta.yaml`
  - `out/20260220-145315774_run-normalized-336M50000100001-v5/manifest.yaml`

## 3. 検証（4-1）
- `assert_unique_nids`: pass
- `check_annex_article_nids`: collisions=0, invalid_annex=0
- `check_appendix_scoped_indices`: problems=0
- `check_ord_format_and_order`: problems=0
- schema: `qai.regdoc_ir.v3`
- `parser_profile.id`: `jp_law_default_v1`

## 4. AIレビュー（4-2）
- 対象1: `art209_3.p1.tbl1`
  - 旧: `table_header.text = 一　第一類医薬品 | 第１類医薬品`, `table_row=2行`
  - 新: `table_header.text = null`, `table_row=3行`
  - 判定: ヘッダ無し表として妥当（先頭行をtable_rowで保持）
- 対象2: `art218_2_4.p1.tbl1`
  - 旧: `table_header.text = 医薬品 | 使用数量`, `table_row=3行`
  - 新: `table_header.text = 医薬品 | 使用数量`, `table_row=3行`
  - 判定: 実質ヘッダあり表として妥当
- 注記: AIレビューは目視代替。最終確認はPRで人間が実施。

## 5. 人間レビュー用比較素材（4-3）
- `runs/20260220-145315774_run-normalized-336M50000100001-v5/art209_3_old_table.yaml`
- `runs/20260220-145315774_run-normalized-336M50000100001-v5/art209_3_new_table.yaml`
- `runs/20260220-145315774_run-normalized-336M50000100001-v5/art218_2_4_old_table.yaml`
- `runs/20260220-145315774_run-normalized-336M50000100001-v5/art218_2_4_new_table.yaml`
- `runs/20260220-145315774_run-normalized-336M50000100001-v5/deepest_item_summary.yaml`

## 6. 変更差分サマリ
- normalized既存値との比較:
  - regdoc_ir: changed
  - parser_profile: unchanged
  - regdoc_profile: unchanged
  - meta: changed

## 7. 実行環境
- Python: `./.venv/Scripts/python.exe`
- tool_version: `0.1.0`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`

## 8. 昇格（7）
- 状態: 実施済み（同一PRへ追コミット）
- 昇格コミット: `c73f8d5daf1dd05fb898b6627b2ed5fd78444026`
- 置換対象:
  - `data/normalized/jp_egov_336M50000100001_20260501_507M60000100117/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_ir.yaml`
  - `data/normalized/jp_egov_336M50000100001_20260501_507M60000100117/jp_egov_336M50000100001_20260501_507M60000100117.meta.yaml`
- 必須コマンド結果:
  - `git rev-parse --verify c73f8d5daf1dd05fb898b6627b2ed5fd78444026`: 成功
  - `git fetch origin`: 成功
  - `git merge-base --is-ancestor c73f8d5daf1dd05fb898b6627b2ed5fd78444026 origin/main`: `false`
- 判定:
  - `origin/main` 祖先条件は未達（main未反映）。完了報告は保留。

