# RUN: 20260218-152931213_feat-pics-annexes-refined-v2

- run_id: `20260218-152931213_feat-pics-annexes-refined-v2`
- branch: `feat/pics-annexes-refined-v2`

## 目的
- Annexes全文1ドキュメントのまま、annex 1/2A/11/15 だけを既存単体profileで再パース（2段階パース）して内部構造を精緻化する。
- 再パース後も `source_spans.locator` の行番号を全文txt基準で維持する。

## 実装概要
- `src/qai_text2ir/text_parser.py`
  - `parse_text_to_ir` に `lines_override`, `line_no_offset`, `finalize` を追加（後方互換）。
  - `finalize=False` 時は postprocess/qualitycheck/ord/index をスキップ。
  - `postprocess.refine_subtrees` 設定に応じ、対象subtreeを profile dispatch で再パースする機能を追加。
  - subtree置換時に nid prefix を必要に応じて揃える処理を追加。
- `src/qai_text2ir/profiles/pics_annexes_default_v2.yaml`
  - annexes全文境界抽出（v1相当） + refine_subtrees dispatch 設定を追加。
  - dispatch: annex `1`,`2A`,`11`,`15`。
- tests
  - `tests/test_pics_annexes_refine_v2.py`
  - `tests/fixtures/pics_annexes_refine_excerpt.txt`

## 再現手順
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --out-dir out/20260218-152931213_feat-pics-annexes-refined-v2 --doc-id pics_pe00917_annexes_20230825_refined --title "PIC/S GMP Guide (PE 009-17) Annexes (25 August 2023) [refined]" --short-title "PIC/S Annexes refined" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/8881" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Annexes)" --parser-profile src/qai_text2ir/profiles/pics_annexes_default_v2.yaml --qualitycheck --strict --emit-only all`

## 確認観点
- strict: 成功（qualitycheck warning 0）
- root.children に annex が複数並ぶ（19件）
- annex `1`, `2A`, `11`, `15` が存在し、各subtreeに section/paragraph/item 等が生成
- annex `2A` に Part A/Part B（chapter）が存在
- mapping外 annex（例: 3）は境界のみ（childrenなし）のまま保持
- `source_spans.locator` は全文行番号を維持
  - 例: annex15 paragraph 2.4 -> `line:12486`
- 既存互換
  - `python -m pytest -q` -> `69 passed, 1 skipped`

## 既知メモ
- refine対象の単体profileが marker ambiguity/gap を warning 出力する場合があるが、strict判定対象の qualitycheck warning には該当しない。

## 生成物
- `out/20260218-152931213_feat-pics-annexes-refined-v2/pics_pe00917_annexes_20230825_refined.regdoc_ir.yaml`
- `out/20260218-152931213_feat-pics-annexes-refined-v2/pics_pe00917_annexes_20230825_refined.parser_profile.yaml`
- `out/20260218-152931213_feat-pics-annexes-refined-v2/pics_pe00917_annexes_20230825_refined.regdoc_profile.yaml`
- `out/20260218-152931213_feat-pics-annexes-refined-v2/pics_pe00917_annexes_20230825_refined.meta.yaml`
- `out/20260218-152931213_feat-pics-annexes-refined-v2/manifest.yaml`
- `runs/20260218-152931213_feat-pics-annexes-refined-v2/RUN.md`
