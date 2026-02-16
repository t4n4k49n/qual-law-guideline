# RUN: 20260217-014756984_feat-eu-gmp-chap1-v2-strict-zero

run_id: 20260217-014756984_feat-eu-gmp-chap1-v2-strict-zero
branch: feat/eu-gmp-chap1-v2-strict-zero

## 目的
- EU GMP Chapter 1 text2ir を仕上げ、`--qualitycheck --strict` で warning 0 を達成する。

## 実装
- `src/qai_text2ir/profiles/eu_gmp_chap1_default_v2.yaml` を新規追加。
  - `drop_line_regexes`: `^\d{1,3}$`, `^\f$`
  - `use_indent_dedent: true`
  - `dedent_pop_kinds: ["subitem", "item"]`
  - marker 追加: `item_roman_rparen`（`i)` 形式）
- `src/qai_text2ir/text_parser.py`
  - qualitycheck のページ番号検出を preformatted 判定と無関係に常時実行。
  - postprocess で preformatted ブロックにも hyphen-wrap 修復を適用（改行foldはしない）。
- `tests/test_text2ir_eu_gmp_chap1.py`
  - preprocess drop（ページ番号除去）検証を v2 プロファイルで実施。
  - 1.13 の `i)`/`ii)` item化 + dedent復帰 + `8`除去を検証。
  - preformatted ブロックでも `system- ... based` が `system-based` になることを検証。

## 実行コマンド
- `python -m pytest -q tests/test_text2ir_eu_gmp_chap1.py`
- `python -m pytest -q tests/test_text2ir_normalization.py tests/test_text2ir_bundle.py tests/test_text2ir_cfr_quality_v2.py`
- `python -m qai_text2ir.cli --input data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt --out-dir out/20260217-014756984_feat-eu-gmp-chap1-v2-strict-zero --doc-id eu_gmp_vol4_chap1_20130131 --title "EU GMP Vol.4 Chapter 1 Pharmaceutical Quality System" --short-title "EU GMP Ch1 PQS" --jurisdiction EU --language en --doc-type guideline --source-url "https://health.ec.europa.eu/document/download/e458c423-f564-4171-b344-030a461c567f_en" --source-format pdf --retrieved-at "2026-02-12" --eu-volume "4" --parser-profile src/qai_text2ir/profiles/eu_gmp_chap1_default_v2.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- strict: 成功（warning 0）
- ページ番号行（1〜8）の単独行: 0件
- paragraph `1.13`: children に item `i` / `ii` を生成
- `Examples ...`: item(ii) ではなく paragraph `1.13` 側に帰属
- item `(xiv)`: `system-based` で出力（未解決 hyphen-wrap なし）

## 生成物
- `out/20260217-014756984_feat-eu-gmp-chap1-v2-strict-zero/eu_gmp_vol4_chap1_20130131.regdoc_ir.yaml`
- `out/20260217-014756984_feat-eu-gmp-chap1-v2-strict-zero/eu_gmp_vol4_chap1_20130131.parser_profile.yaml`
- `out/20260217-014756984_feat-eu-gmp-chap1-v2-strict-zero/eu_gmp_vol4_chap1_20130131.regdoc_profile.yaml`
- `out/20260217-014756984_feat-eu-gmp-chap1-v2-strict-zero/eu_gmp_vol4_chap1_20130131.meta.yaml`
- `out/20260217-014756984_feat-eu-gmp-chap1-v2-strict-zero/manifest.yaml`
- `runs/20260217-014756984_feat-eu-gmp-chap1-v2-strict-zero/RUN.md`

## 補足（PDF→txt）
- 参照PDFからtxtを再生成する場合の例:
  - `pdftotext -layout -nopgbrk <source_pdf> data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt`
