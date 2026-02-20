# RUN: 20260220-194346803_run-normalized-336M50000100001-v6

## 1. 対象
- 種別: 正規化RUN
- doc_id: `jp_egov_336M50000100001_20260501_507M60000100117`
- 入力XML: `%USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\336M50000100001_20260501_507M60000100117\\336M50000100001_20260501_507M60000100117.xml`
- e-Gov URL: `https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117`

## 2. 実行
- 実行コマンド:
  - `./.venv/Scripts/python.exe -m qai_xml2ir.cli --input %USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\xml\\336M50000100001_20260501_507M60000100117\\336M50000100001_20260501_507M60000100117.xml --out-dir runs/20260220-194346803_run-normalized-336M50000100001-v6/promotion_candidate --doc-id jp_egov_336M50000100001_20260501_507M60000100117 --retrieved-at 2026-02-20 --source-url https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117 --emit-only all`
- 出力（昇格候補正本）:
  - `runs/20260220-194346803_run-normalized-336M50000100001-v6/promotion_candidate/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_ir.yaml`
  - `runs/20260220-194346803_run-normalized-336M50000100001-v6/promotion_candidate/jp_egov_336M50000100001_20260501_507M60000100117.parser_profile.yaml`
  - `runs/20260220-194346803_run-normalized-336M50000100001-v6/promotion_candidate/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_profile.yaml`
  - `runs/20260220-194346803_run-normalized-336M50000100001-v6/promotion_candidate/jp_egov_336M50000100001_20260501_507M60000100117.meta.yaml`
  - `runs/20260220-194346803_run-normalized-336M50000100001-v6/promotion_candidate/manifest.yaml`

## 3. 検証（4-1）
- `assert_unique_nids`: pass
- `check_annex_article_nids`: collisions=0, invalid_annex=0
- `check_appendix_scoped_indices`: problems=0
- `check_ord_format_and_order`: problems=0
- schema: `qai.regdoc_ir.v4`
- `parser_profile.id`: `jp_law_default_v1`

## 4. AIレビュー（4-2）
- 目的: 正規化出力がレビュー可能な構造で生成されているかを確認
- 結果: pass
- 注記: AIレビューは目視代替。最終確認はPRで人間が実施。

## 5. 人間レビュー用素材（4-3）
- `runs/20260220-194346803_run-normalized-336M50000100001-v6/deepest_item_summary.yaml`
- `runs/20260220-194346803_run-normalized-336M50000100001-v6/promotion_candidate/manifest.yaml`

## 6. 正規化RUNのまとめ
- 指定XMLから IR / parser_profile / regdoc_profile / meta を再生成し、最小検証4項目はすべてpass。
- 出力スキーマは `qai.regdoc_ir.v4`、`meta.generation.tool.version` は `0.1.1` を記録。
- 正規化出力の健全性確認として、最深item（`art114_45_3.p1.i3`）の祖先経路を抽出し、YAML上の階層と整合していることを確認。

## 7. 実行環境
- Python: `./.venv/Scripts/python.exe`
- tool_version: `0.1.1`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`

## 8. 昇格（7）
- 状態: 実施済み（main直コミットで補完）
- 昇格コミット: `2f9c6a0542f4fcb945f3479f76e22e751d1f9f2f`
- 置換対象:
  - `data/normalized/jp_egov_336M50000100001_20260501_507M60000100117/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_ir.yaml`
  - `data/normalized/jp_egov_336M50000100001_20260501_507M60000100117/jp_egov_336M50000100001_20260501_507M60000100117.meta.yaml`
  - `data/normalized/jp_egov_336M50000100001_20260501_507M60000100117/jp_egov_336M50000100001_20260501_507M60000100117.parser_profile.yaml`
  - `data/normalized/jp_egov_336M50000100001_20260501_507M60000100117/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_profile.yaml`
- 必須コマンド結果:
  - `git rev-parse --verify 2f9c6a0542f4fcb945f3479f76e22e751d1f9f2f`: 成功
  - `git fetch origin`: 成功
  - `git merge-base --is-ancestor 2f9c6a0542f4fcb945f3479f76e22e751d1f9f2f origin/main`: 反映後に確認
