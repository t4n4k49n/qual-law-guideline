## まとめ

モックUIの通常フォルダ選択から `out/*` を外し、正式な `data/normalized` の候補だけを表示するようにしました。一時生成した YAML セットは前回追加した `4yaml内包フォルダ指定` でセッション内に選ぶ運用へ分離し、法令選択メニューの雑音を減らします。

## 変更内容

- `フォルダ選択（data/normalized, out/*）` を `フォルダ選択（data/normalized）` に変更
- 通常のフォルダ選択候補を `data/normalized` 配下だけに限定
- 未使用になった `out/*` 候補探索関数を削除
- `out/*` が通常候補に混ざらないことをテストで確認

## 検証

- `python -m pytest tests/test_mock_ui_yaml_folder_source.py tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 28 passed

<!-- PR_BODY_FILE: runs/20260602-112853632_feat-mock-ui-normalized-only-folder-select-v1/PR_BODY.md -->
