# RUN: 20260217-162857781_run-who-lbm-v3-skip-toc-part

- run_id: `20260217-162857781_run-who-lbm-v3-skip-toc-part`
- branch: `feat/who-lbm-v3-toc-part-annex-fix`

## 目的
- WHO LBM 3rd の TOC混入と Annex重複を止め、本文ベースの構造に戻す。
- PART 構造を有効化し、`part -> chapter` の入れ子を安定化する。
- `--qualitycheck --strict` を warning 0 で通す。

## 変更
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v3.yaml`
  - `preprocess.skip_blocks` で `Contents`/TOC開始行 から `Foreword` までをスキップ。
  - TOC行の保険 drop regex を維持。
  - `part_roman` を `PART I` / `PART I.` の両方で検出可能に調整。
  - `annex` マーカーを `^ANNEX ...` に限定し、本文参照の `Annex 4.` 誤検出を抑止。
- `src/qai_text2ir/text_parser.py`
  - root直下の chapter を最寄り part に再配置する後処理 `_nest_root_chapters_under_parts` を追加。
  - part が先に出ない場合の chapter も、最初の part 配下へ移送するよう補正。
- `src/qai_text2ir/cli.py`
  - `--family` オプションを追加。
  - family 未指定時は `jurisdiction=WHO` なら `WHO_LBM` を既定選択。
- `tests/fixtures/who_lbm_contents_block_excerpt.txt`
  - TOCブロック + 本文開始の抜粋を更新。
- `tests/fixtures/who_lbm_annex_repeated_excerpt.txt`
  - `ANNEX 4.` + 次行 heading のケースへ更新。
- `tests/test_who_lbm_v3_skip_blocks.py`
  - TOC非構造化、part配下chapter、annex heading正規化を検証。

## 実行
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir out/20260217-162857781_run-who-lbm-v3-skip-toc-part --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory biosafety manual, 3rd edition (2004)" --short-title "WHO LBM 3rd" --jurisdiction WHO --language en --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at "2026-02-17" --who-publication-id "9241546506" --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v3.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- tests: `41 passed, 1 skipped`
- strict: 成功（warning 0）
- root直下の TOC風 heading（末尾ページ番号付き chapter/annex/part）は 0
- root直下 annex は `1..5` 各1件で重複なし
- part `I..IX` が生成され、chapter は part 配下に配置
- `Annex 4 .` のドット単独 heading は 0（`annex_dot_heading=[]`）
- Foreword は preamble にあり annex 側へ吸い込みなし

## まとめ
今回の修正で、WHO LBM 3rd の構造ノイズ源だった TOC起因ノードと Annex誤検出を切り離し、章立てを本文準拠に戻せた。これにより downstream の検索・参照・差分比較での構造ぶれが減り、以後のWHO文書追加でも strict gate を品質の安全網として再利用できる。

## 生成物
- `out/20260217-162857781_run-who-lbm-v3-skip-toc-part/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- `out/20260217-162857781_run-who-lbm-v3-skip-toc-part/who_lbm_3rd_2004_9241546506.parser_profile.yaml`
- `out/20260217-162857781_run-who-lbm-v3-skip-toc-part/who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
- `out/20260217-162857781_run-who-lbm-v3-skip-toc-part/who_lbm_3rd_2004_9241546506.meta.yaml`
- `out/20260217-162857781_run-who-lbm-v3-skip-toc-part/manifest.yaml`
- `runs/20260217-162857781_run-who-lbm-v3-skip-toc-part/RUN.md`
