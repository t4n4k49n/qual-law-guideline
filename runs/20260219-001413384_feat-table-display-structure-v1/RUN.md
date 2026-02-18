# RUN: 20260219-001413384_feat-table-display-structure-v1

- run_id: `20260219-001413384_feat-table-display-structure-v1`
- branch: `feat/table-display-structure-v1`

## 目的
- Markdown table を text2ir で構造化し、table_row 選択時に祖先（table title/header）と子孫（note）を regdoc_profile で宣言可能にする。

## 実装
- `src/qai_text2ir/text_parser.py`
  - Markdown table block 検出を追加（header + separator + rows）。
  - `table` / `table_header` / `table_row` ノード生成。
  - caption (`Table ...` / `Figure ...`) を `table.heading` へ採用。
  - table直後の注記行を `note` ノード化して table 配下へ追加。
  - kind prefix を追加（`tbl`, `tblh`, `tblr`）。
  - `table` / `table_header` を structural 扱いに追加。
- `src/qai_text2ir/cli.py`
  - `selectable_kinds` に `table_row` を追加。
  - `grouping_policy` に `table_row -> table` を追加。
  - `context_display_policy` に `table_row` 用 `include_descendants*` 設定を追加。
- `src/qai_text2ir/context_display.py`
  - `resolve_context_nodes()` を追加（祖先 + 子孫解決）。
- docs
  - `docs/specs/table_display_requirements.md`
  - `docs/NORMALIZED_RUN_OUTPUT_4FILES_GUIDE.md`
- tests
  - `tests/fixtures/markdown_table_sample.txt`
  - `tests/test_markdown_table_parsing.py`

## 実行
- `python -m pytest -q tests/test_markdown_table_parsing.py -p no:cacheprovider`
- `python -m pytest -q -p no:cacheprovider`

## 確認結果
- テーブル構造: `table -> table_header -> table_row*` を確認。
- 表注記: `table` 配下に `note` を確認。
- 文脈解決: table_row 選択で祖先（table/table_header）+ note を取得、兄弟 row は除外。
- テスト: `78 passed, 1 skipped`。

## 生成物
- `runs/20260219-001413384_feat-table-display-structure-v1/RUN.md`
- `out/20260219-001413384_feat-table-display-structure-v1/`（同名運用のため作成）
