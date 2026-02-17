# RUN: 20260218-011744140_feat-who-lbm-v4-marker-ref-join

- run_id: `20260218-011744140_feat-who-lbm-v4-marker-ref-join`
- branch: `feat/who-lbm-v4-marker-ref-join`

## 目的
- WHO LBM 3rd の heading 欠落（折り返し行が text 先頭に残る問題）を解消する。
- 本文中の `Annex N.` 参照を annex 開始として誤検出しないようにする。
- strict qualitycheck を維持したまま、WHO以外にも横展開可能な parser 改善にする。

## 変更
- `src/qai_text2ir/text_parser.py`
  - `_merge_structural_marker_heading_lines()` で current line の marker/remainder 判定を `strip_inline_regexes` 適用後の cleaned text に統一。
  - `merge` 時の modal 判定も raw slicing ではなく cleaned remainder を基準化。
  - `preprocess.join_mid_sentence_marker_refs_into_prev`（opt-in）を parse フローに接続。
  - `_should_drop_repeated_structural_header_line()` で bare `Annex N.` の無条件 drop を廃止し、同一 annex コンテキスト内の反復時のみ drop。
- `src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml`
  - `merge_structural_heading_continuations` を `kinds: ["chapter","annex","part"]`, `max_next_line_len: 80` に更新。
  - `join_mid_sentence_marker_refs_into_prev` を追加（annex参照行の前行連結）。
  - annex marker を bare `Annex 4.` を拾いにくい形に更新。
- `tests/test_who_lbm_heading_merge.py`
  - chapter heading continuation 結合テスト
  - noisy annex marker (`• 140 •ANNEX 4`) + 次行タイトル結合テスト
  - 本文中 `Annex 4.` 参照の誤annex化防止テスト
- `tests/test_who_lbm_v4_skip_toc_and_annex_heading.py`
  - v4 annex marker 行の次行 heading 取り込みテストを更新
- `tests/fixtures/who_annex_mid_sentence_ref.txt` を追加
- `tests/fixtures/who_heading_wrap_annex.txt` を更新

## 実行
- `python -m pytest -q tests/test_who_lbm_heading_merge.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py`
- `python -m pytest -q`
- `python -m qai_text2ir.cli --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir out/20260218-011744140_feat-who-lbm-v4-marker-ref-join --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory biosafety manual, 3rd edition (2004)" --short-title "WHO LBM 3rd" --jurisdiction WHO --language en --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at "2026-02-18" --who-publication-id "9241546506" --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- tests: `47 passed, 1 skipped`
- strict: 成功（warning 0）
- heading 統合:
  - chapter 2: `Microbiological risk assessment`
  - chapter 3: `Basic laboratories – Biosafety Levels 1 and 2`
  - chapter 16: `Biosafety and recombinant DNA technology`
  - chapter 19: `The biosafety officer and biosafety committee`
  - annex 4: `Equipment safety`
- 本文参照保持:
  - chapter 11 text に `presented in Annex 4.` が残る
- root 重複:
  - root 直下の `(kind,num)` 重複なし（annex 4 は1件）

## まとめ
本文構造の誤分岐を生む2つの原因（見出し折り返しと `Annex N.` 参照誤検出）を parser の汎用前処理で吸収し、出力の可読性と参照信頼性を同時に改善した。strict 品質ゲートを維持したまま改善できたため、同種PDFへの展開コストを下げながら再発を防止できる状態になった。

## 生成物
- `out/20260218-011744140_feat-who-lbm-v4-marker-ref-join/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- `out/20260218-011744140_feat-who-lbm-v4-marker-ref-join/who_lbm_3rd_2004_9241546506.parser_profile.yaml`
- `out/20260218-011744140_feat-who-lbm-v4-marker-ref-join/who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
- `out/20260218-011744140_feat-who-lbm-v4-marker-ref-join/who_lbm_3rd_2004_9241546506.meta.yaml`
- `out/20260218-011744140_feat-who-lbm-v4-marker-ref-join/manifest.yaml`
- `runs/20260218-011744140_feat-who-lbm-v4-marker-ref-join/RUN.md`
