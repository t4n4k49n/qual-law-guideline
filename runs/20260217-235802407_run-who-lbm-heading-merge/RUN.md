# RUN: 20260217-235802407_run-who-lbm-heading-merge

- run_id: `20260217-235802407_run-who-lbm-heading-merge`
- branch: `feat/who-lbm-heading-merge-v4`

## 目的
- WHO LBM 3rd の chapter/annex 見出しの行折り返し欠落を解消し、可読性と参照品質を上げる。
- Foreword/preamble や strict quality gate を壊さずに heading 補正を導入する。

## 変更
- `src/qai_text2ir/text_parser.py`
  - `preprocess.merge_structural_heading_continuations`（opt-in）を追加。
  - `_merge_structural_marker_heading_lines` を拡張し、以下を結合対象化。
    - marker行の remainder が空 or 句読点のみ（`.:-–—`）
    - kind別 continuation 判定（chapter/annex など）を満たす次行
  - 次行判定は `strip_inline_regexes` 適用後の文字列で実施。
  - 行数は維持し、結合した次行は空文字に置換。
  - TOC風 heading qualitycheck の誤検知を抑えるため、末尾ページ番号判定を `\s{2,}\d{1,3}` に調整。
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml`
  - `merge_structural_heading_continuations` を有効化（chapter/annex, max_next_line_len=60, max_merge_lines=2, max_blank_lookahead=2）。
  - annex marker を `(?:[.:\-–—])?` に拡張。
- `tests/fixtures/who_heading_wrap_chapter.txt` を追加。
- `tests/fixtures/who_heading_wrap_annex.txt` を追加。
- `tests/test_who_lbm_heading_merge.py` を追加（chapter/annex の heading 結合テスト）。

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir out/20260217-235802407_run-who-lbm-heading-merge --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory biosafety manual, 3rd edition (2004)" --short-title "WHO LBM 3rd" --jurisdiction WHO --language en --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at "2026-02-17" --who-publication-id "9241546506" --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- tests: `45 passed, 1 skipped`
- strict: 成功（warning 0）
- chapter heading の統合確認:
  - 2: `Microbiological risk assessment`
  - 3: `Basic laboratories – Biosafety Levels 1 and 2`
  - 4: `The containment laboratory – Biosafety Level 3`
  - 5: `The maximum containment laboratory – Biosafety Level 4`
  - 16: `Biosafety and recombinant DNA technology`
- annex heading の統合確認:
  - annex 4: `Negative-pressure flexible-film isolators`
- Foreword は preamble に保持、annex 5 への混入なし

## まとめ
見出し折り返しを parser の汎用機能として吸収できるようになり、WHO LBM 3rd では章・付属書見出しの欠損が大幅に減った。構造ノードの可読性が上がり、下流の検索・比較・参照での精度改善を strict 品質ゲートを維持したまま実現できた。

## 生成物
- `out/20260217-235802407_run-who-lbm-heading-merge/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- `out/20260217-235802407_run-who-lbm-heading-merge/who_lbm_3rd_2004_9241546506.parser_profile.yaml`
- `out/20260217-235802407_run-who-lbm-heading-merge/who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
- `out/20260217-235802407_run-who-lbm-heading-merge/who_lbm_3rd_2004_9241546506.meta.yaml`
- `out/20260217-235802407_run-who-lbm-heading-merge/manifest.yaml`
- `runs/20260217-235802407_run-who-lbm-heading-merge/RUN.md`
