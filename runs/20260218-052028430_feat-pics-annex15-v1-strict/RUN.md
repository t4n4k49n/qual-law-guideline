# RUN: 20260218-052028430_feat-pics-annex15-v1-strict

- run_id: `20260218-052028430_feat-pics-annex15-v1-strict`
- branch: `feat/pics-annex15-v1-strict`

## 目的
- PIC/S PE 009-17 (Annexes) の Annex 15（Qualification and validation）を単体文書として正規化する。
- Annex 11 で確立したノイズ除去・見出し結合の流れを再利用し、strict quality gate で通す。

## 一次ソース
- `https://picscheme.org/docview/8881`
- retrieved_at: `2026-02-18`

## 入力作成手順
- Annexes全文TXT:
  - `pdftotext -layout -nopgbrk pe009-17_annexes_2023-08-25_en.pdf data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt`
- Annex 15抽出（汎用化したスクリプトを使用）:
  - `python scripts/slice_pics_annex.py --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --annex 15 --output data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt`

## 実装
- `scripts/slice_pics_annex.py` を Annex番号引数型へ更新
  - `--annex` で抽出対象を指定
  - 抽出範囲は `ANNEX N` から `ANNEX N+1` 直前
- `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml` を追加
  - `context_root_kind: annex`
  - `structural_kinds: [annex, section]`
  - Annexesフッタ/ヘッダ行 drop
  - 行末結合ヘッダ（`...Annex 15 Qualification and validation`）strip
  - annex/section 見出し継続結合
  - roman item（`i.`, `ii.`）・alpha item・bullet 記号を抽出
- テスト追加:
  - `tests/test_pics_annex15_profile.py`
  - `tests/fixtures/pics_annex15_header_footer_fixture.txt`
  - `tests/fixtures/pics_annex15_roman_items_fixture.txt`

## 実行
- `python -m pytest -q tests/test_pics_annex15_profile.py`
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt --out-dir out/20260218-052028430_feat-pics-annex15-v1-strict --doc-id pics_pe00917_annex15_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 15 Qualification and validation (25 August 2023)" --short-title "PIC/S PE009-17 Annex 15" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/8881" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Annexes)" --parser-profile src/qai_text2ir/profiles/pics_annex15_default_v1.yaml --qualitycheck --strict --emit-only all`

## 結果
- tests: `58 passed, 1 skipped`
- strict: 成功（warning 0）
- root 配下に annex(15) が 1件
- annex heading: `QUALIFICATION AND VALIDATION`
- section 1.. を生成、section(2) heading: `DOCUMENTATION, INCLUDING VMP`
- section(2) 配下に paragraph `2.1` `2.2` `2.3` `2.4` `2.5` を確認
- roman item（`i.` `ii.` `iii.`）を複数箇所で生成
- `PE 009-17 (Annexes) -213- 25 August 2023` の本文混入なし
- `...Annex 15 Qualification and validation` の行末混入なし

## 既知の残課題
- Annexes 全体（Annex 1〜22）の一括正規化は次PRで対応。
- Annex 15 以外の Annex 専用プロファイル統合方針（共通化/個別化）は次段で決定。

## まとめ
Annex 11 に続いて Annex 15 も strict 通過させたことで、Annexes 系PDFに対する再現可能な処理パターン（抽出スクリプト + 専用profile + 回帰テスト）を2件まで拡張できた。これにより、Annexes 全体展開時の実装リスクとレビュー負荷を先に圧縮できる状態になった。

## 生成物
- `out/20260218-052028430_feat-pics-annex15-v1-strict/pics_pe00917_annex15_20230825.regdoc_ir.yaml`
- `out/20260218-052028430_feat-pics-annex15-v1-strict/pics_pe00917_annex15_20230825.parser_profile.yaml`
- `out/20260218-052028430_feat-pics-annex15-v1-strict/pics_pe00917_annex15_20230825.regdoc_profile.yaml`
- `out/20260218-052028430_feat-pics-annex15-v1-strict/pics_pe00917_annex15_20230825.meta.yaml`
- `out/20260218-052028430_feat-pics-annex15-v1-strict/manifest.yaml`
