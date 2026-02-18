# RUN: 20260219-032631636_feat-table-followups-v1

## 目的
- 前runで挙げた残課題を反映する。
  1. 注記トリガの網羅性拡張
  2. caption表記ゆれ（`表１：`, `表1.`, `表(1)`）の追加対応
  3. 実データ派生fixtureで context 回帰防止（兄弟row除外）の増補

## 変更
- `src/qai_text2ir/text_parser.py`
  - `TABLE_CAPTION_PATTERN` を拡張し、以下を許容:
    - `表１：...`
    - `表1....`
    - `表(1)...`
  - `TABLE_NOTE_TRIGGER_PATTERN` を拡張し、以下を許容:
    - 日本語注記プレフィックス（`注`, `注記`, `備考`, `※`, `（注）`）
    - 記号脚注（`†`, `‡`, `*`, `•`）の連続・空白なしケース
    - `(\*)` 形式の英数/roman脚注
- `tests/fixtures/markdown_table_caption_note_variants.md` を追加
  - caption/注記表記ゆれを含む実行用fixture
- `tests/test_markdown_table_parsing.py` を拡張
  - caption表記ゆれ + 記号脚注の検証
  - 実データ派生fixtureで `table_row` 選択時に兄弟rowが含まれないことを検証

## テスト
- `python -m pytest -q tests/test_markdown_table_parsing.py` → 5 passed
- `python -m pytest -q tests/test_normal_note_descendants.py` → 2 passed

## 結果
- 残課題3点を実装・検証まで完了。
