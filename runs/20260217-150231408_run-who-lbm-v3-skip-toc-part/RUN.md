# RUN: 20260217-150231408_run-who-lbm-v3-skip-toc-part

- run_id: `20260217-150231408_run-who-lbm-v3-skip-toc-part`
- branch: `feat/who-lbm-v3-skip-toc-part`

## 目的
- `skip_blocks` を導入し、WHO LBM 3rd の Contentsブロック由来の構造ノイズを除去する。
- Annex見出し再掲による root 直下の重複 sibling を抑止する。
- `--qualitycheck --strict` を warning 0 で通す。

## 入力
- `data/human-readable/who/WHO_LBM_3rd.txt`
- source_url: `https://www.who.int/publications/i/item/9241546506`
- retrieved_at: `2026-02-17`

## 変更
- `src/qai_text2ir/text_parser.py`
  - preprocess に `skip_blocks`（start/end/include_start/include_end/max_lines）を追加。
  - parse loop で strip_inline 後の `stripped_raw` に対して block skip を実行。
  - end未検出時の安全弁（max_lines超過）で warning をログ出力。
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v3.yaml` を追加。
  - `skip_blocks` で `Contents` 〜 `Foreword` を一括スキップ。
  - `structural_kinds` に `part/chapter/annex` を定義。
  - `part_roman` marker を追加。
  - `drop_repeated_structural_headers` を part/chapter/annex で有効化。
- `src/qai_text2ir/profile_loader.py`
  - WHO_LBM の既定を v3 優先、v2、v1 の順でフォールバック。
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v2.yaml`
  - `applies_to.defaults: false` に変更。
- `tests/fixtures/who_lbm_contents_block_excerpt.txt` を追加。
- `tests/fixtures/who_lbm_annex_repeated_excerpt.txt` を追加。
- `tests/test_who_lbm_v3_skip_blocks.py` を追加。
- `tests/test_text2ir_who_lbm_3rd.py`
  - loader の既定 profile id 検証を v3 に更新。

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir out/20260217-150231408_run-who-lbm-v3-skip-toc-part --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory biosafety manual, 3rd edition (2004)" --short-title "WHO LBM 3rd" --jurisdiction WHO --language en --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at "2026-02-17" --who-publication-id "9241546506" --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v3.yaml --qualitycheck --strict --emit-only all`

## 結果
- pytest: `41 passed, 1 skipped`
- strict: warning 0
- parser_profile 出力 id: `who_lbm_3rd_default_v3`
- root 直下で TOC由来（末尾ページ番号）heading は 0
- root 直下 annex の `(kind,num)` 重複は 0（annex 1〜5 が各1）
- part parser は実装済みだが、当該入力TXTでは Contentsブロック外に `PART ...` 見出しがないため root part は 0（fixtureテストで part 生成自体は検証済み）

## 目視レビュー観点
- chapter/annex heading に TOCページ番号末尾が混入していないこと。
- root annex の重複 sibling がないこと。
- Foreword 以降の本文 chapter が正常に構造化されていること。

## 生成物
- `out/20260217-150231408_run-who-lbm-v3-skip-toc-part/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- `out/20260217-150231408_run-who-lbm-v3-skip-toc-part/who_lbm_3rd_2004_9241546506.parser_profile.yaml`
- `out/20260217-150231408_run-who-lbm-v3-skip-toc-part/who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
- `out/20260217-150231408_run-who-lbm-v3-skip-toc-part/who_lbm_3rd_2004_9241546506.meta.yaml`
- `out/20260217-150231408_run-who-lbm-v3-skip-toc-part/manifest.yaml`
- `runs/20260217-150231408_run-who-lbm-v3-skip-toc-part/RUN.md`
