# RUN: 20260219-031945386_feat-test-table-md-realdata

## 目的
- 実データ由来の Markdown 表を使って、table 実装（caption/header/row/note/context）のテスト妥当性を確認する。
- テストで判明した修正点を反映し、今後の課題を明確化する。

## 入力
- `runs/20260219-024359384_feat-extract-table-contexts-api-gmp-v1-all/table_context_extractions.jsonl`
- 抜粋して fixture 化:
  - `tests/fixtures/markdown_table_real_excerpt.md`

## 実施内容
- 実データ由来 fixture を追加し、以下を検証:
  - 日本語 caption (`表1`) を table heading に取り込めるか
  - 表ヘッダ/行 (`table_header` / `table_row`) が構造化されるか
  - 表下注記（`注 1)` 等）が `note` として table 配下に入るか
- 失敗原因を修正:
  - `**表...**` の装飾付き caption を検出できるよう修正
  - 表直後の空行を挟む注記を table note として収集できるよう修正
  - table note のトリガに日本語注記を追加

## 実行コマンド
- `python -m pytest -q tests/test_markdown_table_parsing.py`
- `python -m pytest -q tests/test_normal_note_descendants.py`

## 結果
- `tests/test_markdown_table_parsing.py`: 3 passed
- `tests/test_normal_note_descendants.py`: 2 passed

## 今後の課題
1. 注記トリガの網羅性拡張
- `注記`, `備考`, `※`, 記号脚注（`†`, `‡`）の連続・複合パターンを追加検証する。

2. caption 表記ゆれの追加対応
- 全角記号混在（`表１：`, `表1.`）や括弧付き番号（`表(1)`）の検出精度を追加評価する。

3. context 表示の回帰防止
- `table_row` 選択時に `table_header` と `note` のみを拾い、兄弟 row を拾わないことを実データ派生 fixture で増補する。
