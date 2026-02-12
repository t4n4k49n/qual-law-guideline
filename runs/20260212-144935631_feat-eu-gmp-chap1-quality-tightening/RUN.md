# RUN: 20260212-144935631_feat-eu-gmp-chap1-quality-tightening

run_id: 20260212-144935631_feat-eu-gmp-chap1-quality-tightening
branch: feat/eu-gmp-chap1-quality-tightening

## 目的
- EU GMP Chapter 1 text2ir の精緻化として、PDF由来ノイズ除去・prose unwrap/hyphen-wrap修復・i)/ii)列挙のitem化とdedent復帰を実装し、bundle成果物を更新する。

## 実装
- `src/qai_text2ir/profiles/eu_gmp_chap1_default_v1.yaml`
  - `preprocess.drop_line_regexes` / `drop_line_exact` / `use_indent_dedent` / `dedent_pop_kinds` を追加。
  - `item_roman_rparen` marker（`i)`形式）を追加。
- `src/qai_text2ir/text_parser.py`
  - preprocess設定を読み、行単位ノイズ（ページ番号等）を段落区切り化せずスキップ。
  - `is_preformatted_line` を再設計（4space単独判定を廃止、tab/罫線/表揃え/大インデント判定へ）。
  - 非preformattedブロックで改行畳み込み+hyphen-wrap修復を実施（`system-
 based` 対応）。
  - dedentヒューリスティクスを追加し、item/subitemから親段落へ復帰可能にした。
  - qualitycheckに `page-number-only line remains` を追加。
- `tests/test_text2ir_eu_gmp_chap1.py`
  - `test_drop_page_numbers_and_fix_hyphen_wrap` を追加。
  - `test_parse_item_roman_rparen_and_dedent_back_to_paragraph` を追加。

## 実行コマンド
- `python -m pytest -q tests/test_text2ir_eu_gmp_chap1.py`
- `python -m pytest -q tests/test_text2ir_normalization.py`
- `python -m pytest -q tests/test_text2ir_cfr_quality_v2.py`
- `python -m pytest -q tests/test_text2ir_bundle.py tests/test_text2ir_cfr_notes.py tests/test_text2ir_marker_disambiguation.py`
- `python -m pytest -q tests/test_text2ir_profiles_pics.py`
- `python -m qai_text2ir.cli --input data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt --out-dir out/20260212-144935631_feat-eu-gmp-chap1-quality-tightening --doc-id eu_gmp_vol4_chap1_20130131 --title "EU GMP Vol.4 Chapter 1 Pharmaceutical Quality System" --short-title "EU GMP Ch1 PQS" --jurisdiction EU --language en --doc-type guideline --source-url "https://health.ec.europa.eu/document/download/e458c423-f564-4171-b344-030a461c567f_en" --source-format pdf --retrieved-at "2026-02-12" --eu-volume "4" --parser-profile src/qai_text2ir/profiles/eu_gmp_chap1_default_v1.yaml --emit-only all`

## 結果
- out/20260212-144935631_feat-eu-gmp-chap1-quality-tightening/ に4 YAMLを生成。
- 受入確認:
  - 単独ページ番号行（`1`〜`8`）は regdoc_ir から除去された。
  - qualitycheck の `unresolved hyphen-space pattern remains` は 0。
  - paragraph `1.13` 配下に `i)` / `ii)` item が生成され、`Examples ...` 文は item(ii) ではなく paragraph `1.13` text 側へ復帰。

## 生成物
- `out/20260212-144935631_feat-eu-gmp-chap1-quality-tightening/eu_gmp_vol4_chap1_20130131.regdoc_ir.yaml`
- `out/20260212-144935631_feat-eu-gmp-chap1-quality-tightening/eu_gmp_vol4_chap1_20130131.parser_profile.yaml`
- `out/20260212-144935631_feat-eu-gmp-chap1-quality-tightening/eu_gmp_vol4_chap1_20130131.regdoc_profile.yaml`
- `out/20260212-144935631_feat-eu-gmp-chap1-quality-tightening/eu_gmp_vol4_chap1_20130131.meta.yaml`
- `out/20260212-144935631_feat-eu-gmp-chap1-quality-tightening/manifest.yaml`
- `runs/20260212-144935631_feat-eu-gmp-chap1-quality-tightening/RUN.md`
