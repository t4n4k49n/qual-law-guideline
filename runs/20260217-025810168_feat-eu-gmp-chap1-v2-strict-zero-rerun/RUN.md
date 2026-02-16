# RUN: 20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun

run_id: 20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun
branch: feat/eu-gmp-chap1-v2-strict-zero-rerun

## 目的
- EU GMP Chapter 1 の text2ir を v2 profile で再仕上げし、strict で warning 0 を達成する。

## 実装
- `src/qai_text2ir/profiles/eu_gmp_chap1_default_v2.yaml`
  - preprocess に以下を設定:
    - `^\d{1,3}$`（単独ページ番号）
    - `^Commission.*B-1049.*Telephone:.*$`（EU Commission フッタ）
    - `^Pharmaceutical Quality System\d*$`（ヘッダ繰り返し）
    - `^\f$`（フォームフィード）
  - `use_indent_dedent: true` / `dedent_pop_kinds: ["subitem", "item"]`
  - `item_roman_rparen`（`i)`）marker を保持。
- `src/qai_text2ir/profiles/eu_gmp_chap1_default_v1.yaml`
  - `applies_to.defaults: false` に変更（v2優先化）。
- `src/qai_text2ir/profile_loader.py`
  - `family="EU_GMP"` の既定を `eu_gmp_chap1_default_v2.yaml` に変更。
  - 併せて `family="PICS"` の既定を `pics_part1_default_v1.yaml` に設定。
- `tests/test_text2ir_eu_gmp_chap1.py`
  - ページ番号/フッタ/ヘッダノイズ除去の検証を追加。
  - 1.13 の `i)`/`ii)` item化 + Examples の paragraph帰属 + `8`除去を検証。
  - `load_parser_profile(family="EU_GMP")` が v2 を返すことを検証。

## 実行コマンド
- `python -m pytest -q tests/test_text2ir_eu_gmp_chap1.py`
- `python -m pytest -q tests/test_text2ir_normalization.py tests/test_text2ir_bundle.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_profiles_pics.py`
- `python -m qai_text2ir.cli --input data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt --out-dir out/20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun --doc-id eu_gmp_vol4_chap1_20130131 --title "EU GMP Vol.4 Chapter 1 Pharmaceutical Quality System" --short-title "EU GMP Ch1 PQS" --jurisdiction EU --language en --doc-type guideline --source-url "https://health.ec.europa.eu/document/download/e458c423-f564-4171-b344-030a461c567f_en" --source-format pdf --retrieved-at "2026-02-12" --eu-volume "4" --parser-profile src/qai_text2ir/profiles/eu_gmp_chap1_default_v2.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- strict: 成功（warning 0）
- regdoc_ir から以下が除去された:
  - 単独ページ番号行（1〜8）
  - `Commission ... B-1049 ... Telephone: ...` フッタ
  - `Pharmaceutical Quality System1` 型ヘッダ
- paragraph `1.13` は item `i` / `ii` に分割され、`Examples ...` は paragraph 側に帰属。
- item `(xiv)` は `system-based` で出力され、未解決 hyphen-space pattern は 0。

## 生成物
- `out/20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun/eu_gmp_vol4_chap1_20130131.regdoc_ir.yaml`
- `out/20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun/eu_gmp_vol4_chap1_20130131.parser_profile.yaml`
- `out/20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun/eu_gmp_vol4_chap1_20130131.regdoc_profile.yaml`
- `out/20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun/eu_gmp_vol4_chap1_20130131.meta.yaml`
- `out/20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun/manifest.yaml`
- `runs/20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun/RUN.md`
