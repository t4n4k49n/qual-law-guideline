# RUN: 20260218-055612198_feat-pics-annex1-v2-strict

- run_id: `20260218-055612198_feat-pics-annex1-v2-strict`
- branch: `feat/pics-annex1-v2-strict`

## 目的
- PIC/S PE 009-17 (Annexes) の Annex 1（Manufacture of sterile medicinal products）を単体文書として正規化する。
- Annex 11/15 で確立したヘッダ・フッタ除去と見出し結合を、最も複雑な Annex 1 に横展開する。

## 一次ソース
- `https://picscheme.org/docview/8881`
- retrieved_at: `2026-02-18`

## 入力作成手順
1. Annexes全文TXT化
   - `pdftotext -layout -nopgbrk pe009-17_annexes.pdf data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt`
2. Annex 1 抜粋（汎用化したsliceスクリプト）
   - `python scripts/slice_pics_annex.py --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --annex-id 1 --output data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`

## 実装
- `scripts/slice_pics_annex.py` を Annex ID 文字列対応へ更新
  - `--annex-id`（`--annex`/`--annex-no` 互換）を追加
  - `ANNEX <id>` 単独行を厳格判定
  - 終端は「次の Annex 見出し」を自動検出
  - 本文中の `Annex 1` 参照では切れない
- `src/qai_text2ir/profiles/pics_annex1_default_v2.yaml` を追加
  - `context_root_kind: annex`
  - `structural_kinds: [annex, section]`
  - `Document map` ブロックの `skip_blocks` 除去
  - Annexesフッタ行の drop
  - 行末連結ヘッダ（`...Annex 1 Manufacture of sterile medicinal products`）strip
  - `ANNEX 1` + 次行タイトルの heading 結合
  - section/paragraph/item/subitem の抽出
- テスト追加
  - `tests/test_slice_pics_annex.py`
  - `tests/test_pics_annex1_profile_v2.py`

## 実行
- `python -m pytest -q tests/test_slice_pics_annex.py tests/test_pics_annex1_profile_v2.py`
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt --out-dir out/20260218-055612198_feat-pics-annex1-v2-strict --doc-id pics_pe00917_annex1_20230825 --title "PIC/S GMP Guide (PE 009-17) Annex 1 Manufacture of sterile medicinal products (25 August 2023)" --short-title "PIC/S PE009-17 Annex 1" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/8881" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Annexes)" --parser-profile src/qai_text2ir/profiles/pics_annex1_default_v2.yaml --qualitycheck --strict --emit-only all`

## 結果
- tests: `62 passed, 1 skipped`
- strict: 成功（warning 0）
- root 配下に annex(1) が 1件
- annex heading: `MANUFACTURE OF STERILE MEDICINAL PRODUCTS`
- section(1): `Scope`, section(2): `Principle`, section(3): `Pharmaceutical Quality System (PQS)`
- paragraph(3.1) が section(3) 配下に配置
- `` 箇条書き由来の subitem を複数生成
- フッタ `PE 009-17 (Annexes) -N- 25 August 2023` の本文混入なし
- 行末ランニングヘッダ `...Annex 1 Manufacture of sterile medicinal products` の本文混入なし

## 既知の残課題
- Annex 1 末尾の `Glossary` は本文テキスト上で無番号見出しのため、現profileでは `section(11)` ではなく本文扱い。
- Annexes全体（Annex 1〜22）の一括正規化は次PRで対応。

## まとめ
Annex 1 のように構造と本文量が大きいケースでも strict を維持できたことで、Annexes 系PDF処理の再利用性を実運用レベルで確認できた。特に `Document map` スキップと行末ヘッダ除去の組み合わせが効いたため、後続の Annex 群を同じパターンで展開しやすい基盤が整った。

## 生成物
- `out/20260218-055612198_feat-pics-annex1-v2-strict/pics_pe00917_annex1_20230825.regdoc_ir.yaml`
- `out/20260218-055612198_feat-pics-annex1-v2-strict/pics_pe00917_annex1_20230825.parser_profile.yaml`
- `out/20260218-055612198_feat-pics-annex1-v2-strict/pics_pe00917_annex1_20230825.regdoc_profile.yaml`
- `out/20260218-055612198_feat-pics-annex1-v2-strict/pics_pe00917_annex1_20230825.meta.yaml`
- `out/20260218-055612198_feat-pics-annex1-v2-strict/manifest.yaml`
