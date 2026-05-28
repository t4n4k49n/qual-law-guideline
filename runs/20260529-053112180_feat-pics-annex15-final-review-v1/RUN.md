# RUN: PIC/S Annex 15 目検最終確認・校正

- run_id: `20260529-053112180_feat-pics-annex15-final-review-v1`
- branch: `feat-pics-annex15-final-review-v1`
- target: `PIC/S PE 009-17 Annex 15 Qualification and validation`
- doc_id: `pics_pe00917_annex15_20230825`
- source: `data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt`
- profile: `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml`

## 目的

正規化RUN前に、Annex 15のTable/Warning周りと見出し・階層を目検確認し、承認NGになりやすい構造上の誤りを先に潰す。

## 実施内容

- Annex 15をstrict bundleで再生成した。
- 原文のTable/Figure/Warning/Note候補を検索した。
- IRの `kind: table` / `kind: table_row` / `kind: note` / `preformatted` / Warning候補を検索した。
- 深い階層サンプルとして、最大深度5の `ann15.sec5.p5_22.ivi` を抽出した。
- 原文253-254行の `5. PROCESS VALIDATION` と `General` を突き合わせ、`General` が見出しへ誤結合される問題を修正した。

## 修正

- `src/qai_text2ir/text_parser.py`
  - `merge_structural_heading_continuations` に `deny_next_regexes` を追加。
- `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml`
  - Annex 15では `General` のようなTitle Case単語を見出し継続から除外。
- `tests/test_pics_annex15_profile.py`
  - 大文字の見出し折り返しは結合し、Title Case小見出しは結合しない回帰テストを追加。

## 検証

- `python -m pytest tests\test_pics_annex15_profile.py -q`
  - `4 passed`
- `python -m pytest -q`
  - `252 passed, 1 skipped`
- `python -m qai_text2ir.goal_check --mode promotion`
  - PASS
- `python -m qai_text2ir.special_structure_audit --mode promotion`
  - PASS

## 成果物

- `FINAL_REVIEW.md`
- `SAMPLE_EXTRACT.md`
- `GOAL_CHECK_PROMOTION.md`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `SPECIAL_STRUCTURE_AUDIT.json`
- `PR.md`
