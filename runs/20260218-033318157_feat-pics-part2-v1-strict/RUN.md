# RUN: 20260218-033318157_feat-pics-part2-v1-strict

- run_id: `20260218-033318157_feat-pics-part2-v1-strict`
- branch: `feat/pics-part2-v1-strict`

## 目的
- PIC/S GMP Guide PE 009-17 Part II（API GMP）を text2ir で正規化し、strict quality gate を通す。
- TOC/フッタ/ランニングヘッダ由来ノイズを抑制しつつ、Part II の節構造を保持する。

## 一次ソース
- docview: `https://picscheme.org/docview/6607`
- publications: `https://picscheme.org/en/publications`
- retrieved_at: `2026-02-18`

## 入力生成
- 出力入力ファイル:
  - `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt`
- 手順:
  - `pdftotext -layout -nopgbrk pe009-17_part2.pdf data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt`
- 生成後に UTF-8/LF 正規化を実施。

## 実装
- `src/qai_text2ir/profiles/pics_part2_default_v1.yaml` を追加
  - `skip_blocks` で TOC (`TABLE OF CONTENTS`) を本文 `1. INTRODUCTION` まで除外
  - Part II フッタ行、サイト行、ページ番号行を drop
  - 制御文字を strip
  - chapter heading 継続結合を有効化
  - repeated structural headers（chapter）抑止を有効化
  - marker_types:
    - chapter: `1. INTRODUCTION` 形式
    - section: `1.1 Objective` 形式
    - paragraph: `2.19 ...` 形式
    - item: `1. ...` 形式
    - bullet: `•//`
- tests 追加:
  - `tests/test_pics_part2_v1.py`
  - `tests/fixtures/pics_part2_toc_intro_fixture.txt`
  - `tests/fixtures/pics_part2_bullet_fixture.txt`

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt --out-dir out/20260218-033318157_feat-pics-part2-v1-strict --doc-id pics_pe00917_part2_20230825 --title "PIC/S GMP Guide (PE 009-17) Part II (25 August 2023)" --short-title "PIC/S PE009-17 Part II" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/6607" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Part II)" --parser-profile src/qai_text2ir/profiles/pics_part2_default_v1.yaml --qualitycheck --strict --emit-only all`

## 結果
- tests: `55 passed, 1 skipped`
- strict: 成功（warning 0）
- root chapter: `1..20`（重複なし）
- TOC 由来 chapter 生成なし
- `PE 009-17 (Part II) - ... - 25 August 2023` の本文混入なし
- `Chapter X ...` 型ランニングヘッダの本文混入なし
- `` を含む bullet が subitem として生成される

## まとめ
Part II を単一文書として strict で安定処理できる状態になり、Part I で確立した運用を API GMP 側にも展開できた。これにより、PE 009-17 全体の再実行・差分確認・品質担保を同じ枠組みで回せるため、改訂追従時の運用コストとレビュー負荷を下げられる見込み。

## 生成物
- `out/20260218-033318157_feat-pics-part2-v1-strict/pics_pe00917_part2_20230825.regdoc_ir.yaml`
- `out/20260218-033318157_feat-pics-part2-v1-strict/pics_pe00917_part2_20230825.parser_profile.yaml`
- `out/20260218-033318157_feat-pics-part2-v1-strict/pics_pe00917_part2_20230825.regdoc_profile.yaml`
- `out/20260218-033318157_feat-pics-part2-v1-strict/pics_pe00917_part2_20230825.meta.yaml`
- `out/20260218-033318157_feat-pics-part2-v1-strict/manifest.yaml`
