# RUN: 20260218-020810912_feat-pics-part1-ch1-v2-strict

- run_id: `20260218-020810912_feat-pics-part1-ch1-v2-strict`
- branch: `feat/pics-part1-ch1-v2-strict`

## 目的
- PIC/S PE 009-17 (Part I) Chapter 1 を text2ir で安定して正規化する。
- `CHAPTER 1` 形式のランニングヘッダ再掲で chapter 重複や本文混入が起きないようにする。
- strict quality gate を維持したまま 4 YAML を生成する。

## 一次ソース
- docview: `https://picscheme.org/docview/6606`
- publications: `https://picscheme.org/en/publications`
- retrieved_at: `2026-02-18`

## 入力データ
- `data/human-readable/pics/pe009-17_part1_chap1_2023-08-25_en.txt`
- 参照元: `qual-law-guideline_OLD-HANDMADE/data/human-readable/12.PICS/PICS_PE_009-17_PART-I_CHAPTER-1.txt`
- UTF-8 / LF に正規化

## 参考手順（PDF -> Chapter 1 抽出）
- 全文抽出:
  - `pdftotext -layout -nopgbrk pe009-17_part1.pdf pe009-17_part1_2023-08-25_en.txt`
- Chapter 1 切り出し:
  - `CHAPTER 1` 行から `CHAPTER 2` 直前までを抽出

## 変更
- `src/qai_text2ir/text_parser.py`
  - `drop_repeated_structural_headers` の chapter 判定を `CHAPTER <n>` 形式に拡張。
  - 同一 chapter 文脈での `Chapter 1 ...` 再掲のみ drop し、新章開始は drop しない。
  - heading continuation 判定にガードを追加し、`PRINCIPLE` のような単語見出しの過剰結合を回避。
- `src/qai_text2ir/profiles/pics_part1_default_v2.yaml`
  - PICS Part I Chapter 1 向けの v2 profile を追加（defaults: true）。
  - preprocess に heading continuation / repeated header drop / footer除去を追加。
- `src/qai_text2ir/profile_loader.py`
  - `family == "PICS"` で `pics_part1_default_v2.yaml` を優先し、無ければ v1 へフォールバック。
- tests
  - `tests/test_pics_part1_chapter_headers.py` を追加（2ケース）。
  - `tests/fixtures/pics_part1_chapter1_heading_fixture.txt` を追加。
  - `tests/fixtures/pics_part1_chapter1_running_header_fixture.txt` を追加。
  - `tests/test_text2ir_profiles_pics.py` に loader default の検証を追加。

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_part1_chap1_2023-08-25_en.txt --out-dir out/20260218-020810912_feat-pics-part1-ch1-v2-strict --doc-id pics_pe00917_part1_chap1_20230825 --title "PIC/S GMP Guide (PE 009-17) Part I Chapter 1 Pharmaceutical Quality System" --short-title "PIC/S PE009-17 Part I Ch1" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/6606" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Part I)" --parser-profile src/qai_text2ir/profiles/pics_part1_default_v2.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- tests: `50 passed, 1 skipped`
- strict: 成功（warning 0）
- 目視:
  - root 配下に chapter(1) が 1件のみ
  - chapter(1).heading = `PHARMACEUTICAL QUALITY SYSTEM`
  - chapter(1) 配下に paragraph `1.1` 〜 `1.13` が生成
  - `Chapter 1 Pharmaceutical Quality System` の混入なし
  - `PE 009-17 (Part I)` フッタ混入なし

## まとめ
PIC/S の `CHAPTER 1` 形式に合わせて重複ヘッダ抑止と前処理を強化し、章構造の安定化を達成した。CFR/EU/WHO と異なる様式でも strict 品質ゲートで再現可能なテンプレートが整い、次段の Part I 全章展開へつながる基盤になった。

## 生成物
- `out/20260218-020810912_feat-pics-part1-ch1-v2-strict/pics_pe00917_part1_chap1_20230825.regdoc_ir.yaml`
- `out/20260218-020810912_feat-pics-part1-ch1-v2-strict/pics_pe00917_part1_chap1_20230825.parser_profile.yaml`
- `out/20260218-020810912_feat-pics-part1-ch1-v2-strict/pics_pe00917_part1_chap1_20230825.regdoc_profile.yaml`
- `out/20260218-020810912_feat-pics-part1-ch1-v2-strict/pics_pe00917_part1_chap1_20230825.meta.yaml`
- `out/20260218-020810912_feat-pics-part1-ch1-v2-strict/manifest.yaml`
