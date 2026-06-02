## まとめ

表示例を適用した後に、現在どの表示例が効いているかを画面上で確認できるようにしました。表示例セクションも他の設定項目と同じ折りたたみ形式にそろえ、法令・プロファイル・選択の一括適用状態が読み取りやすくなります。

## 変更内容

- 表示例セクションを expander 形式に変更
- expander ヘッダに `表示例：<適用中の表示例>` を表示
- 選択メニューのラベルを `あらかじめ準備してある典型サンプルを選択（法令・プロファイル・選択を一括適用）` に変更
- 表示例適用時の法令、プロファイル、選択NIDを署名として保存
- 法令、プロファイル、選択NIDが変わった場合だけ表示例を解除
- 表示カスタマイズ変更では表示例を解除しない
- 表示例署名と表示名生成の単体テストを追加

## 検証

- `python -m pytest tests/test_mock_ui_yaml_folder_source.py tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 30 passed

<!-- PR_BODY_FILE: runs/20260602-115152652_feat-mock-ui-active-preset-indicator-v1/PR_BODY.md -->
