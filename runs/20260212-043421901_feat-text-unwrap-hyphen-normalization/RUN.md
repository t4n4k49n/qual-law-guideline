# RUN

run_id: 20260212-043421901_feat-text-unwrap-hyphen-normalization
branch: feat/text-unwrap-hyphen-normalization
started_at: 2026-02-12 04:34 (JST)

## 目的（1文）
- PART211.txt を text2ir で実行し、4 YAML を生成する。

## Done Definition（完了条件）
- [x] 4 YAML生成
- [x] 実行ログ保存

## 入力
- `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\human-readable\11.CFR\Un-fomatted\PART211.txt`

## 実行コマンド
- `python -m qai_text2ir.cli --input "...\PART211.txt" --out-dir "out/20260212-043421901_feat-text-unwrap-hyphen-normalization" --doc-id us_cfr_part211_unformatted_unwrapcheck --title "21 CFR Part 211" --short-title "CFR Part 211" --cfr-title 21 --cfr-part 211 --source-url "https://www.ecfr.gov/current/title-21/part-211" --retrieved-at "2026-02-12" --emit-only all`

## 生成物
- `out/20260212-043421901_feat-text-unwrap-hyphen-normalization/us_cfr_part211_unformatted_unwrapcheck.regdoc_ir.yaml`
- `out/20260212-043421901_feat-text-unwrap-hyphen-normalization/us_cfr_part211_unformatted_unwrapcheck.meta.yaml`
- `out/20260212-043421901_feat-text-unwrap-hyphen-normalization/us_cfr_part211_unformatted_unwrapcheck.parser_profile.yaml`
- `out/20260212-043421901_feat-text-unwrap-hyphen-normalization/us_cfr_part211_unformatted_unwrapcheck.regdoc_profile.yaml`
- `runs/20260212-043421901_feat-text-unwrap-hyphen-normalization/text2ir_part211.log`
