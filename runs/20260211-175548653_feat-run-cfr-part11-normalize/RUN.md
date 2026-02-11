# RUN

run_id: 20260211-175548653_feat-run-cfr-part11-normalize
branch: feat/run-cfr-part11-normalize
started_at: 2026-02-11 17:55 (JST)

## 目的（1文）
- 21 CFR PART11（Un-formatted TXT）を現行text2irで正規化し、4 YAMLを生成する。

## Done Definition（完了条件）
- [x] 指定入力から4 YAMLを生成
- [x] 実行ログを runs に保存
- [x] 生成ファイル一覧を RUN.md に記録

## 入力
- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\human-readable\11.CFR\Un-fomatted\PART11.txt`

## 実行コマンド
- `python -m qai_text2ir.cli --input "%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\human-readable\11.CFR\Un-fomatted\PART11.txt" --out-dir "out/20260211-175548653_feat-run-cfr-part11-normalize" --doc-id us_cfr_part11_unformatted_normalizedcheck --title "21 CFR Part 11" --short-title "CFR Part 11" --cfr-title 21 --cfr-part 11 --source-url "https://www.ecfr.gov/current/title-21/part-11" --retrieved-at "2026-02-11" --emit-only all`

## 結果（事実ベース）
- 4 YAML を `out/20260211-175548653_feat-run-cfr-part11-normalize/` に生成
- 実行ログを `runs/20260211-175548653_feat-run-cfr-part11-normalize/text2ir_part11.log` に保存
- 実行時ログは marker ambiguity 警告が 12 行出力（処理は完了）

## 生成物
- `out/20260211-175548653_feat-run-cfr-part11-normalize/us_cfr_part11_unformatted_normalizedcheck.regdoc_ir.yaml`
- `out/20260211-175548653_feat-run-cfr-part11-normalize/us_cfr_part11_unformatted_normalizedcheck.meta.yaml`
- `out/20260211-175548653_feat-run-cfr-part11-normalize/us_cfr_part11_unformatted_normalizedcheck.parser_profile.yaml`
- `out/20260211-175548653_feat-run-cfr-part11-normalize/us_cfr_part11_unformatted_normalizedcheck.regdoc_profile.yaml`
- `runs/20260211-175548653_feat-run-cfr-part11-normalize/text2ir_part11.log`

