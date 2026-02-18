# RUN: 20260218-110710555_feat-pics-annexes-full-v1-strict

- run_id: `20260218-110710555_feat-pics-annexes-full-v1-strict`
- branch: `feat/pics-annexes-full-v1-strict`

## 目的
- PIC/S PE 009-17 (Annexes) 全文を 1 regdoc として正規化し、root配下に annex 群を並べる。
- Annex境界の安定化を優先し、内部の細分（section/paragraph）は次PRへ分離する。

## ソースと入力
- source_url: `https://picscheme.org/docview/8881`
- retrieved_at: `2026-02-18`
- 入力TXT: `data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt`

## PDF→TXT 手順（再現用）
- 既存入力を再利用。
- 新規生成する場合の手順:
  - `pdftotext -layout -nopgbrk pe009-17_annexes.pdf data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt`

## 実装
- `src/qai_text2ir/profiles/pics_annexes_default_v1.yaml` を追加。
  - TOCブロックの skip
  - footer/page number/web site 行の除去
  - 単独行ランニングヘッダ除去
  - 行末くっつきランニングヘッダ除去
  - annex heading continuation（2Aの複数行タイトル結合）
- `src/qai_text2ir/text_parser.py` を調整。
  - heading continuation 判定で footer 風行（`PE 009-17 ... 25 August 2023`）を結合対象外にする。
- tests 追加:
  - `tests/test_pics_annexes_full_profile_v1.py`
  - `tests/fixtures/pics_annexes_full_excerpt.txt`

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --out-dir out/20260218-110710555_feat-pics-annexes-full-v1-strict --doc-id pics_pe00917_annexes_20230825 --title "PIC/S GMP Guide (PE 009-17) Annexes (25 August 2023)" --short-title "PIC/S PE009-17 Annexes" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/8881" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Annexes)" --parser-profile src/qai_text2ir/profiles/pics_annexes_default_v1.yaml --qualitycheck --strict --emit-only all`

## 目視確認
- root.children に annex が複数生成（19件）
- annex num に `1`, `2A`, `11`, `15` が存在
- annex `2A` heading は複数行結合で `... FOR HUMAN USE` を含む
- TOC由来の `ANNEX 1 ... 1` 形式は annex ノード化されない
- footer `PE 009-17 (Annexes) -NNN- 25 August 2023` は本文に残存なし
- 単独行/行末ランニングヘッダの混入を抑制
- strict 実行は成功（qualitycheck warning 0）

## 既知課題
- 本runは annex境界の安定化に焦点を置いており、annex内部の section/paragraph 分割は次PRで強化予定。
- annex番号の連番上は `17 -> 19` のギャップがログ出力される（原文構成由来の可能性があり、今回は構造化失敗ではない）。

## 生成物
- `out/20260218-110710555_feat-pics-annexes-full-v1-strict/pics_pe00917_annexes_20230825.regdoc_ir.yaml`
- `out/20260218-110710555_feat-pics-annexes-full-v1-strict/pics_pe00917_annexes_20230825.parser_profile.yaml`
- `out/20260218-110710555_feat-pics-annexes-full-v1-strict/pics_pe00917_annexes_20230825.regdoc_profile.yaml`
- `out/20260218-110710555_feat-pics-annexes-full-v1-strict/pics_pe00917_annexes_20230825.meta.yaml`
- `out/20260218-110710555_feat-pics-annexes-full-v1-strict/manifest.yaml`
- `runs/20260218-110710555_feat-pics-annexes-full-v1-strict/RUN.md`
