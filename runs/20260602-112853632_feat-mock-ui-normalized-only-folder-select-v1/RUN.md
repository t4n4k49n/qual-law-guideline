# RUN: feat/mock-ui-normalized-only-folder-select-v1

## 目的

モックUIの通常フォルダ選択から `out/*` 候補を外し、正式版の `data/normalized` だけを表示する。

## 変更内容

- `フォルダ選択（data/normalized, out/*）` の表示を `フォルダ選択（data/normalized）` に変更。
- 通常のフォルダ選択候補を `data/normalized` 配下だけに限定。
- `out/*` は「4yaml内包フォルダ指定」でセッション内に明示選択する運用に分離。
- 未使用になった `out/*` 候補探索関数を削除。
- `out/*` が通常候補に混ざらないことをテストで確認。

## 検証

- `python -m pytest tests/test_mock_ui_yaml_folder_source.py tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 28 passed
