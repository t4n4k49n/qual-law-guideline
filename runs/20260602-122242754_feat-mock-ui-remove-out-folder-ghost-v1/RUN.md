# RUN: feat/mock-ui-remove-out-folder-ghost-v1

## 目的

4yaml内包フォルダ指定後に通常のフォルダ選択へ戻ると、`out/*` 候補が再表示されるバグを修正する。

## 原因

通常フォルダ選択用の候補生成に `_discover_out_bundles()` が残っており、`data/normalized` と `out/*` を再マージしていた。さらに、セッションに古い `out/...` の `normalized_folder_key` が残ると、候補外の値が保持される余地があった。

## 変更内容

- 通常フォルダ選択から `out/*` 候補探索を削除。
- 表示文言を `フォルダ選択（data/normalized）` に変更。
- セッションに候補外の `normalized_folder_key` が残っていた場合、先頭の `data/normalized` 候補へ戻す。
- `out` に4yamlが存在しても通常候補に混ざらないことをテストで確認。

## 検証

- `python -m pytest tests/test_mock_ui_yaml_folder_source.py tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 31 passed
