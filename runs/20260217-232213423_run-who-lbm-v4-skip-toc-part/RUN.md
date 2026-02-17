# RUN: 20260217-232213423_run-who-lbm-v4-skip-toc-part

- run_id: `20260217-232213423_run-who-lbm-v4-skip-toc-part`
- branch: `feat/who-lbm-v4-skip-toc-part`

## 目的
- WHO LBM 3rd の TOC起因の構造崩れを止め、本文ベースの章構造へ戻す。
- Foreword を preamble に保持し、Annex 側への誤吸い込みを防ぐ。
- strict qualitycheck を warning 0 で通す。

## 変更
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml` を追加。
  - `skip_blocks` で `Contents` から本文 `Foreword` までをブロックスキップ。
  - TOC行の保険drop regex を維持。
  - `part/chapter/annex` 構造化を有効化し、annex punctuation を marker 側で吸収。
- `src/qai_text2ir/profile_loader.py`
  - WHO_LBM 既定プロファイルを v4 優先（v4 -> v3 -> v2 -> v1 fallback）へ更新。
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v3.yaml`
  - `applies_to.defaults` を `false` に変更。
- `src/qai_text2ir/text_parser.py`
  - `drop_repeated_structural_headers` に part 重複抑止を追加。
  - `Annex n.` 参照行の誤構造化を抑止。
  - 構造見出し結合を拡張（空行を挟む annex 見出し結合を許容。ただし `ANNEX` 行のみ）。
- `tests/fixtures/who_lbm_excerpt_skip_toc.txt` を追加。
- `tests/test_who_lbm_v4_skip_toc_and_annex_heading.py` を追加。
- `tests/test_text2ir_who_lbm_3rd.py`
  - WHO default profile の期待値を v4 に更新。

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir out/20260217-232213423_run-who-lbm-v4-skip-toc-part --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory biosafety manual, 3rd edition (2004)" --short-title "WHO LBM 3rd" --jurisdiction WHO --language en --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at "2026-02-17" --who-publication-id "9241546506" --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- tests: `43 passed, 1 skipped`
- strict: 成功（warning 0）
- root直下の TOC風 heading（末尾ページ番号付き chapter/annex/part）は 0
- Foreword は preamble に存在し、annex 5 text への混入なし
- chapter 1..8 は part I 配下で生成
- root直下 annex は `1..5` 各1ノード（重複なし）
- annex(4).heading は `Equipment safety`（句読点のみ heading なし）

## まとめ
TOCを行単位でなくブロック単位で除去する形へ切り替えたことで、WHO LBM 3rd の構造崩れ（Foreword吸い込み・本文章欠落）を再現性高く抑止できた。加えて annex/preamble の境界が安定し、strict を継続的な品質ゲートとして機能させられる状態に戻せた。

## 生成物
- `out/20260217-232213423_run-who-lbm-v4-skip-toc-part/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- `out/20260217-232213423_run-who-lbm-v4-skip-toc-part/who_lbm_3rd_2004_9241546506.parser_profile.yaml`
- `out/20260217-232213423_run-who-lbm-v4-skip-toc-part/who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
- `out/20260217-232213423_run-who-lbm-v4-skip-toc-part/who_lbm_3rd_2004_9241546506.meta.yaml`
- `out/20260217-232213423_run-who-lbm-v4-skip-toc-part/manifest.yaml`
- `runs/20260217-232213423_run-who-lbm-v4-skip-toc-part/RUN.md`
