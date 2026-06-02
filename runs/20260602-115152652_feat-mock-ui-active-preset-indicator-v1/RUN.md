# RUN: feat/mock-ui-active-preset-indicator-v1

## 目的

表示例を選択後、セレクトボックスが無選択へ戻っても、現在どの表示例が適用中かわかるようにする。

## 変更内容

- 表示例セクションを他の設定項目と同じ expander 形式に変更。
- expander ヘッダに「表示例：<適用中の表示例>」を表示。
- expander 内に「あらかじめ準備してある典型サンプルを選択（法令・プロファイル・選択を一括適用）」ラベルの選択メニューを配置。
- 表示例適用時の法令、プロファイル、選択NIDを署名として保存。
- 下段の法令選択、プロファイル、選択NIDが表示例適用時の署名から変わった場合、適用中表示を消して表示例を解除。
- 表示カスタマイズは表示例の対象外として、解除条件には含めない。
- 表示例名と署名生成の単体テストを追加。

## 検証

- `python -m pytest tests/test_mock_ui_yaml_folder_source.py tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 30 passed
