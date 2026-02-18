# RUN: 20260219-005614494_feat-normal-note-descendants-v1

- run_id: `20260219-005614494_feat-normal-note-descendants-v1`
- branch: `feat/normal-note-descendants-v1`

## 目的
- 表以外の通常本文でも注書き（Note/備考/脚注）を note ノードとして抽出し、`include_descendants` 設定で同時表示できるようにする。

## 実装
- `src/qai_text2ir/text_parser.py`
  - `preprocess.extract_notes`（enabled/start_regexes/max_lines）を追加。
  - 注書き開始判定とブロック収集ロジックを追加。
  - 直前の選択候補（subitem/item/paragraph/statement/table_row）配下へ note を生成。
  - table 処理との重複回避（table 側で消費した行は再処理されない）。
- `src/qai_text2ir/cli.py`
  - `dq_gmp_checklist.context_display_policy` の subitem/item/paragraph/statement に `include_descendants*` を追加。
- docs
  - `docs/specs/notes_display_requirements.md`
  - `docs/NORMALIZED_RUN_OUTPUT_4FILES_GUIDE.md` 追記
- tests
  - `tests/fixtures/normal_note_sample.txt`
  - `tests/test_normal_note_descendants.py`

## 実行
- `python scripts/check_bidi_controls.py`
- `python -m pytest -q tests/test_normal_note_descendants.py tests/test_markdown_table_parsing.py -p no:cacheprovider`
- `python -m pytest -q -p no:cacheprovider`

## 確認結果
- BIDI/hidden 制御文字: 0件
- 新規 note 抽出テスト: pass
- 全体テスト: `80 passed, 1 skipped`

## 生成物
- `runs/20260219-005614494_feat-normal-note-descendants-v1/RUN.md`
- `out/20260219-005614494_feat-normal-note-descendants-v1/`（同名運用）
