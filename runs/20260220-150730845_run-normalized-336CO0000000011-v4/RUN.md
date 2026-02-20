# RUN: 20260220-150730845_run-normalized-336CO0000000011-v4

## 1. 対象
- 種別: 正規化RUN
- doc_id: `jp_egov_336CO0000000011_20260501_507CO0000000362`
- 入力XML: `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336CO0000000011_20260501_507CO0000000362\336CO0000000011_20260501_507CO0000000362.xml`
- e-Gov URL: `https://laws.e-gov.go.jp/law/336CO0000000011/20260501_507CO0000000362`

## 2. 実行
- 実行コマンド:
  - `./.venv/Scripts/python.exe -m qai_xml2ir.cli --input %USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336CO0000000011_20260501_507CO0000000362\336CO0000000011_20260501_507CO0000000362.xml --out-dir out/20260220-150730845_run-normalized-336CO0000000011-v4 --doc-id jp_egov_336CO0000000011_20260501_507CO0000000362 --retrieved-at 2026-02-20 --source-url https://laws.e-gov.go.jp/law/336CO0000000011/20260501_507CO0000000362 --emit-only all`
- 出力:
  - `out/20260220-150730845_run-normalized-336CO0000000011-v4/jp_egov_336CO0000000011_20260501_507CO0000000362.regdoc_ir.yaml`
  - `out/20260220-150730845_run-normalized-336CO0000000011-v4/jp_egov_336CO0000000011_20260501_507CO0000000362.parser_profile.yaml`
  - `out/20260220-150730845_run-normalized-336CO0000000011-v4/jp_egov_336CO0000000011_20260501_507CO0000000362.regdoc_profile.yaml`
  - `out/20260220-150730845_run-normalized-336CO0000000011-v4/jp_egov_336CO0000000011_20260501_507CO0000000362.meta.yaml`
  - `out/20260220-150730845_run-normalized-336CO0000000011-v4/manifest.yaml`

## 3. 検証（4-1）
- `assert_unique_nids`: pass
- `check_annex_article_nids`: collisions=0, invalid_annex=0
- `check_appendix_scoped_indices`: problems=0
- `check_ord_format_and_order`: problems=0
- schema: `qai.regdoc_ir.v3`
- `parser_profile.id`: `jp_law_default_v1`

## 4. AIレビュー（4-2）
- 最深item: `art37_6.p3.i2`（深さ=5）
- 同列item数: 3
- 同列最短: `art37_6.p3.i2`（`第二種医療機器製造販売業許可を受けている者が第一種医療機器製造販売業許可を受けた場合`）
- 既存normalizedの同一nid比較:
  - old text: `第二種医療機器製造販売業許可を受けている者が第一種医療機器製造販売業許可を受けた場合`
  - new text: `第二種医療機器製造販売業許可を受けている者が第一種医療機器製造販売業許可を受けた場合`
- 注記: AIレビューは目視代替。最終確認はPRで人間が実施。

## 5. 人間レビュー用比較素材（4-3）
- `runs/20260220-150730845_run-normalized-336CO0000000011-v4/deepest_item_summary.yaml`
- `runs/20260220-150730845_run-normalized-336CO0000000011-v4/manifest.yaml`

## 6. 変更差分サマリ
- normalized既存値との比較:
  - regdoc_ir: changed
  - parser_profile: changed
  - regdoc_profile: changed
  - meta: changed

## 7. 実行環境
- Python: `./.venv/Scripts/python.exe`
- tool_version: `0.1.0`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`

## 8. 昇格（7）
- 状態: 実施済み（同一PRへ追コミット）
- 昇格コミット: `68bdda1ad89e97eb3a84ab9c722f6b515d0be140`
- 置換対象:
  - `data/normalized/jp_egov_336CO0000000011_20260501_507CO0000000362/jp_egov_336CO0000000011_20260501_507CO0000000362.regdoc_ir.yaml`
  - `data/normalized/jp_egov_336CO0000000011_20260501_507CO0000000362/jp_egov_336CO0000000011_20260501_507CO0000000362.parser_profile.yaml`
  - `data/normalized/jp_egov_336CO0000000011_20260501_507CO0000000362/jp_egov_336CO0000000011_20260501_507CO0000000362.regdoc_profile.yaml`
  - `data/normalized/jp_egov_336CO0000000011_20260501_507CO0000000362/jp_egov_336CO0000000011_20260501_507CO0000000362.meta.yaml`
- 必須コマンド結果:
  - `git rev-parse --verify 68bdda1ad89e97eb3a84ab9c722f6b515d0be140`: 成功
  - `git fetch origin`: 成功
  - `git merge-base --is-ancestor 68bdda1ad89e97eb3a84ab9c722f6b515d0be140 origin/main`: `false`
- 判定:
  - `origin/main` 祖先条件は未達（main未反映）。完了報告は保留。
