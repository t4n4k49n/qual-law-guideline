# RUN: 20260218-161714868_feat-pics-annexes-refined-v3-fallback

- run_id: `20260218-161714868_feat-pics-annexes-refined-v3-fallback`
- branch: `feat/pics-annexes-refined-v3-fallback`

## 目的
- refine_subtrees の mapping外 annex に fallback profile を適用し、境界のみだった annex を最低限の内部構造付きへ引き上げる。
- dispatch対象 annex（1/2A/11/15）の精緻化品質は維持する。

## 実装
- `src/qai_text2ir/text_parser.py`
  - `postprocess.refine_subtrees` に `fallback_profile_id` 対応を追加。
  - dispatch未ヒット時、`keep_unmapped=true` かつ `fallback_profile_id` 設定時のみ fallback で再パース。
- `src/qai_text2ir/profiles/pics_annex_generic_default_v1.yaml`
  - mapping外 annex 用の汎用profileを追加（section/paragraph/item/subitem の安全側基線）。
- `src/qai_text2ir/profiles/pics_annexes_default_v3.yaml`
  - v2を継承しつつ `fallback_profile_id: pics_annex_generic_default_v1` を有効化。
- tests
  - `tests/test_pics_annexes_refine_v3_fallback.py`
  - `tests/fixtures/pics_annexes_refine_fallback_excerpt.txt`

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --out-dir out/20260218-161714868_feat-pics-annexes-refined-v3-fallback --doc-id pics_pe00917_annexes_20230825_refined_v3 --title "PIC/S GMP Guide (PE 009-17) Annexes (25 August 2023) [refined v3 fallback]" --short-title "PIC/S Annexes refined v3" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/8881" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Annexes)" --parser-profile src/qai_text2ir/profiles/pics_annexes_default_v3.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- strict: 成功（qualitycheck warning 0）
- dispatch対象 annex 1/2A/11/15 は従来どおり内部構造化
- mapping外 annex も fallback で内部構造化
  - 例: annex 13 に section/paragraph が生成（paragraph locator: `line:10977`）
- source_spans.locator は全文行番号基準を維持
- フッタ/ランニングヘッダの大量混入は確認されず

## 既知メモ
- subparse中の marker ambiguity / gap は parserログとして出力されるが、strict判定対象の qualitycheck warning ではない。

## 生成物
- `out/20260218-161714868_feat-pics-annexes-refined-v3-fallback/pics_pe00917_annexes_20230825_refined_v3.regdoc_ir.yaml`
- `out/20260218-161714868_feat-pics-annexes-refined-v3-fallback/pics_pe00917_annexes_20230825_refined_v3.parser_profile.yaml`
- `out/20260218-161714868_feat-pics-annexes-refined-v3-fallback/pics_pe00917_annexes_20230825_refined_v3.regdoc_profile.yaml`
- `out/20260218-161714868_feat-pics-annexes-refined-v3-fallback/pics_pe00917_annexes_20230825_refined_v3.meta.yaml`
- `out/20260218-161714868_feat-pics-annexes-refined-v3-fallback/manifest.yaml`
- `runs/20260218-161714868_feat-pics-annexes-refined-v3-fallback/RUN.md`
