# RUN: 20260218-101934654_feat-pics-annex2a-v1-strict

- run_id: `20260218-101934654_feat-pics-annex2a-v1-strict`
- branch: `feat/pics-annex2a-v1-strict`

## 目的
- PIC/S GMP Guide PE 009-17 (Annexes) Annex 2A を text2ir で strict 品質の4 YAMLに正規化する。
- Annex 2A 見出し結合、SCOPE系無番号見出し、Part A/B、B3.3、Figure/Table 改行保持を確認する。

## 入力
- 公式ソース: `https://picscheme.org/docview/8881`
- 入力テキスト:
  - `data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt`（既存）
  - `python scripts/slice_pics_annex.py --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --annex-id 2A --output data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt`

## 変更
- `src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml`
  - Annex 2A 専用 parser_profile を追加。
  - footer/running header 除去、annex heading continuation、Part A/B・Chapter N・B3.3 等の marker を定義。
- `scripts/slice_pics_annex.py`
  - 同一 annex 見出しが複数出るケースで、最長ブロックを採用するよう改善（TOC誤抽出対策）。
- `src/qai_text2ir/text_parser.py`
  - Figure/Table 開始行を preformatted block 判定対象に追加。
  - 矢印行（↓等）を preformatted 行として扱い、改行保持を強化。
  - structural heading continuation の空remainder時挙動を、プロファイル互換を維持しつつ `kinds` で制御可能に調整。
  - 全大文字の続き行（ANNEXタイトル2行目）を heading continuation として結合可能に調整。
- tests
  - `tests/test_slice_pics_annex.py` に 2A 切り出し/重複見出し最長ブロック選択テストを追加。
  - `tests/test_pics_annex2a_preformatted.py` を追加（Figure矢印行の改行保持）。
  - `tests/fixtures/pics_slice_annex_2a_fixture.txt` を追加。

## 実行
- `python scripts/slice_pics_annex.py --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --annex-id 2A --output data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt`
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt --out-dir out/20260218-101934654_feat-pics-annex2a-v1-strict --doc-id pics_pe00917_annex2a_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 2A ATMP (25 August 2023)" --short-title "PIC/S Annex 2A (ATMP)" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/8881" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Annexes)" --parser-profile src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- strict: 成功（qualitycheck warning 0）
- root配下 annex: 1件（`num=2A`）
- annex.heading: `MANUFACTURE OF ADVANCED THERAPY MEDICINAL PRODUCTS FOR HUMAN USE`
- annex配下に section/chapter が存在（SCOPE/APPLICATION/PRINCIPLE セクション、Part A/B chapter）
- `B3.3` は paragraph として生成
- footer (`PE 009-17 (Annexes) -NN- 25 August 2023`) の本文混入: 0件
- Figure 3 ブロック: multiline維持（1行潰れなし）

## 既知メモ
- 元テキストのフロー矢印文字は抽出文字種依存で見え方が変わる場合があるが、Figureブロック自体は改行保持される。

## 生成物
- `out/20260218-101934654_feat-pics-annex2a-v1-strict/pics_pe00917_annex2a_20230825.regdoc_ir.yaml`
- `out/20260218-101934654_feat-pics-annex2a-v1-strict/pics_pe00917_annex2a_20230825.parser_profile.yaml`
- `out/20260218-101934654_feat-pics-annex2a-v1-strict/pics_pe00917_annex2a_20230825.regdoc_profile.yaml`
- `out/20260218-101934654_feat-pics-annex2a-v1-strict/pics_pe00917_annex2a_20230825.meta.yaml`
- `out/20260218-101934654_feat-pics-annex2a-v1-strict/manifest.yaml`
- `runs/20260218-101934654_feat-pics-annex2a-v1-strict/RUN.md`
