# RUN

## Run ID
`20260602-092803441_feat-mock-ui-table-row-context-v1`

## Branch
`feat/mock-ui-table-row-context-v1`

## Purpose
mock-uiに残っているtable_row表示課題について、具体例Markdownを残しつつ、表示例4・table_row文脈表示profile・重複見出し抑制を実装する。

## Outputs
- `MOCK_UI_ISSUE_EXAMPLES.md`
- `data/mock_ui/display_examples.yaml`
- `data/mock_ui/profiles/table_row_context_default.yaml`
- `src/qai_mock_ui/render.py`
- `tests/test_mock_ui_render.py`

## Scope
- 表示例4を、実データのtable_row 1行目・3行目を選ぶ非連続2行デモに更新する。
- table_row用のmock-ui profileを追加する。
- profileから同一見出しの重複抑制を指定できるようにする。
- 正規化データ本体は変更しない。

## Notes
- 表示例4は現行設定では「表2行」と書かれているが、選択NIDは1件のみ。
- `jp_egov_336M50000100002_20260501_507M60000100117` の対象別表は、正式IR上も1行だけだった。
- 2行tableデモは、`jp_pmda_api_gmp_guideline_20011102` の表1から1行目と3行目を選ぶ形にした。
