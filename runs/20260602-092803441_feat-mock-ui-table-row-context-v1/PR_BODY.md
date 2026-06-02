<!-- PR_BODY_FILE: runs/20260602-092803441_feat-mock-ui-table-row-context-v1/PR_BODY.md -->

## まとめ
mock-uiの表行デモを、実データ上の非連続行選択で確認できる形に更新しました。表示例4で「選んだ行だけがチェックシートに出る」ことを直感的に確認できるようになり、表ヘッダや別表見出しの重複もprofileで抑制できるようにしています。これにより、チェックシート候補の表行表示をレビューしやすくし、今後の表示プロファイル調整をコード直書きではなく設定中心で進めやすくします。

## 変更内容
- 表示例4を `jp_pmda_api_gmp_guideline_20011102` の表1に差し替え
- 表示例4の選択行を1行目・3行目にし、2行目を飛ばす非連続選択デモに変更
- `data/mock_ui/profiles/table_row_context_default.yaml` を追加
- `table_row` の文脈表示で複数の祖先kindを停止点にできるように対応
- profile指定で同一見出しの重複表示を抑制できるように対応
- mock-ui課題の具体例MarkdownとRUN記録を追加

## 動作確認
- `python -m pytest tests/test_mock_ui_render.py -q`
  - 16 passed
- `python -m pytest tests/test_mock_ui_candidate_visibility.py tests/test_xml2ir_profiles_table_context.py -q`
  - 4 passed

