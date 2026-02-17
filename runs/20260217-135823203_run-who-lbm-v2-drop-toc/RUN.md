# RUN: 20260217-135823203_run-who-lbm-v2-drop-toc

- run_id: `20260217-135823203_run-who-lbm-v2-drop-toc`
- branch: `feat/who-lbm-v2-drop-toc-strict`

## 目的
- WHO LBM 3rd の text2ir で、TOC（Contents）由来の chapter/annex 混入を止める。
- ランニングヘッダ再掲で発生する annex 重複 sibling を抑止する。
- `--qualitycheck --strict` を warning 0 で通す。

## 入力
- `data/human-readable/who/WHO_LBM_3rd.txt`
- source_url: `https://www.who.int/publications/i/item/9241546506`
- retrieved_at: `2026-02-17`

## 変更
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml`
  - title を TOC除去/重複抑止が明確な表記に更新。
  - TOC除去 regex を「スペース2つ以上 + ページ番号」基準へ更新。
  - References/Index の TOC 行除去を明示。
  - chapter/annex marker に `\s{2,}\d{1,3}` の末尾ガードを追加。
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v1.yaml`
  - `applies_to.defaults: false`（維持）。
- `src/qai_text2ir/profile_loader.py`
  - WHO_LBM は v2 を既定（維持）。
- `tests/fixtures/WHO_LBM_3rd_toc_excerpt_v2.txt` を追加。
- `tests/fixtures/WHO_LBM_3rd_annex5_repeated_header_excerpt_v2.txt` を追加。
- `tests/test_who_lbm_v2_drop_toc_and_annex_dedupe.py` を追加。
  - TOC 行が structural node を作らないこと。
  - Annex 5 の再掲ヘッダで root annex sibling が重複しないこと。
- `tests/test_text2ir_who_lbm_3rd.py`
  - TOC fixture を実データ相当の「スペース2つ以上 + ページ番号」形式に更新。

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir out/20260217-135823203_run-who-lbm-v2-drop-toc --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory biosafety manual, 3rd edition (2004)" --short-title "WHO LBM 3rd" --jurisdiction WHO --language en --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at "2026-02-17" --who-publication-id "9241546506" --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml --qualitycheck --strict --emit-only all`

## 結果
- pytest: `39 passed, 1 skipped`
- strict: warning 0
- parser_profile 出力 id: `who_lbm_3rd_default_v2`
- root直下 TOC由来（末尾ページ番号付き）chapter/annex 見出しなし
- root直下 annex 重複なし（annex 1〜5 各1、annex 5 は1つ）

## 目視レビュー観点
- root直下 chapter/annex heading の末尾にページ番号が残っていないこと。
- root直下 annex の `(kind,num)` 重複がないこと。
- chapter 10 などで章見出しと同一 item の重複が増えていないこと。

## 生成物
- `out/20260217-135823203_run-who-lbm-v2-drop-toc/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- `out/20260217-135823203_run-who-lbm-v2-drop-toc/who_lbm_3rd_2004_9241546506.parser_profile.yaml`
- `out/20260217-135823203_run-who-lbm-v2-drop-toc/who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
- `out/20260217-135823203_run-who-lbm-v2-drop-toc/who_lbm_3rd_2004_9241546506.meta.yaml`
- `out/20260217-135823203_run-who-lbm-v2-drop-toc/manifest.yaml`
- `runs/20260217-135823203_run-who-lbm-v2-drop-toc/RUN.md`
