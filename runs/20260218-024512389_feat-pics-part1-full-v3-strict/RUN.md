# RUN: 20260218-024512389_feat-pics-part1-full-v3-strict

- run_id: `20260218-024512389_feat-pics-part1-full-v3-strict`
- branch: `feat/pics-part1-full-v3-strict`

## 目的
- PIC/S PE 009-17 (Part I) を Chapter 1 単体ではなく全体（Ch1〜Ch9）で正規化する。
- TOC/フッタ/ランニングヘッダ由来ノイズを抑え、`--qualitycheck --strict` を通す。

## 一次ソース
- `https://picscheme.org/docview/6606`
- `https://picscheme.org/en/publications`
- retrieved_at: `2026-02-18`

## 入力準備
- 生成入力: `data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt`
- 再現コマンド:
  - `pdftotext -layout -nopgbrk pe-009-17-part1.pdf data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt`
- 生成後に UTF-8/LF 正規化を実施。

## 変更
- `src/qai_text2ir/profiles/pics_part1_default_v3.yaml` を追加
  - TOC ブロックスキップ（`TABLE OF CONTENT(S)` 〜 本文 `CHAPTER 1`）
  - フッタ/サイト行/ページ行の drop
  - 行末にくっつく `...Chapter X Title` の strip
  - `CHAPTER` 見出しの継続行結合
  - 同一 chapter の繰り返しヘッダ drop
  - bullet を `[•]` の両方で subitem 化
- `src/qai_text2ir/profile_loader.py`
  - PICS 既定を `v3 -> v2 -> v1` の順でフォールバック
- tests
  - `tests/test_pics_part1_full_v3.py` を追加
  - `tests/fixtures/pics_part1_full_v3_toc_fixture.txt` を追加
  - `tests/fixtures/pics_part1_full_v3_bullet_fixture.txt` を追加
  - `tests/test_text2ir_profiles_pics.py` の default profile 期待値を v3 に更新

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt --out-dir out/20260218-024512389_feat-pics-part1-full-v3-strict --doc-id pics_pe00917_part1_20230825 --title "PIC/S GMP Guide (PE 009-17) Part I (25 August 2023)" --short-title "PIC/S PE009-17 Part I" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/6606" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Part I)" --parser-profile src/qai_text2ir/profiles/pics_part1_default_v3.yaml --qualitycheck --strict --emit-only all`

## 結果
- tests: `53 passed, 1 skipped`
- strict: 成功（warning 0）
- root 直下 chapter: `1,2,3,4,5,6,7,8,9`
- TOC 由来 chapter 生成なし
- フッタ `PE 009-17 (Part I) - ... - 25 August 2023` の本文混入なし
- ランニングヘッダ由来 `Chapter X ...` の大量混入なし
- bullet `` を含む行が subitem として生成されることをテストで確認

## まとめ
Part I 全体を単一文書として strict で安定処理できる状態になり、章単位の個別調整から全体運用へ移行できる基盤が整った。これにより、文書全体での差分確認・再実行・品質保証のコストを下げながら、次段のプロファイル横展開と保守を進めやすくなる。

## 生成物
- `out/20260218-024512389_feat-pics-part1-full-v3-strict/pics_pe00917_part1_20230825.regdoc_ir.yaml`
- `out/20260218-024512389_feat-pics-part1-full-v3-strict/pics_pe00917_part1_20230825.parser_profile.yaml`
- `out/20260218-024512389_feat-pics-part1-full-v3-strict/pics_pe00917_part1_20230825.regdoc_profile.yaml`
- `out/20260218-024512389_feat-pics-part1-full-v3-strict/pics_pe00917_part1_20230825.meta.yaml`
- `out/20260218-024512389_feat-pics-part1-full-v3-strict/manifest.yaml`
