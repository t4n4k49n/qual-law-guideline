# RUN: 20260217-110608950_feat-who-lbm-v2-clean-headers

- run_id: `20260217-110608950_feat-who-lbm-v2-clean-headers`
- branch: `feat/who-lbm-v2-clean-headers`

## 目的
- WHO LBM 3rd の regdoc_ir で、TOC起因の chapter/annex 混入とページ内ランニングヘッダ重複を抑止する。
- strict qualitycheck を維持しつつ、構造整合チェック（重複 sibling / TOC風 heading）を追加する。

## 変更
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml` を追加。
  - TOC行除去 regex（chapter/annex + 末尾ページ番号、Foreword/Acknowledgements、References/Index）を追加。
  - `chapter_num_dot` に末尾ページ番号除外 `(?!.*\s+\d{1,3}\s*$)` を追加。
  - `preprocess.drop_repeated_structural_headers` を有効化（kinds: chapter/annex）。
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v1.yaml`
  - `applies_to.defaults: false` に変更。
- `src/qai_text2ir/profile_loader.py`
  - `family="WHO_LBM"` の既定 profile を `who_lbm_3rd_default_v2.yaml` に変更。
- `src/qai_text2ir/text_parser.py`
  - profile opt-in の重複構造ヘッダ抑止を追加。
  - `_find_last_in_stack`, `_norm`, `_should_drop_repeated_structural_header_line` など補助関数を追加。
  - qualitycheck に構造整合チェックを追加：
    - 同一親で `(kind, num)` 重複 sibling の warning。
    - chapter/annex heading の TOC風（末尾ページ番号）warning。
- `tests/test_text2ir_who_lbm_3rd.py`
  - profile既定v2化テストへ更新。
  - `test_drop_toc_entries_dont_create_chapters` を追加。
  - `test_drop_repeated_running_headers_inside_chapter` を追加。

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir out/20260217-110608950_feat-who-lbm-v2-clean-headers --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory biosafety manual, 3rd edition (2004)" --short-title "WHO LBM 3rd" --jurisdiction WHO --language en --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at "2026-02-17" --who-publication-id "9241546506" --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- tests: `37 passed, 1 skipped`
- strict: 成功（warning 0）
- root直下の TOC風 heading（末尾ページ番号付き chapter/annex）は 0
- chapter 10 配下の「章タイトル同一 item」重複は 0
- root直下 `annex num=5` は 1ノードに収束

## 生成物
- `out/20260217-110608950_feat-who-lbm-v2-clean-headers/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- `out/20260217-110608950_feat-who-lbm-v2-clean-headers/who_lbm_3rd_2004_9241546506.parser_profile.yaml`
- `out/20260217-110608950_feat-who-lbm-v2-clean-headers/who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
- `out/20260217-110608950_feat-who-lbm-v2-clean-headers/who_lbm_3rd_2004_9241546506.meta.yaml`
- `out/20260217-110608950_feat-who-lbm-v2-clean-headers/manifest.yaml`
- `runs/20260217-110608950_feat-who-lbm-v2-clean-headers/RUN.md`
