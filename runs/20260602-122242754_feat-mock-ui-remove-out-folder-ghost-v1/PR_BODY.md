## まとめ

モックUIで `4yaml内包フォルダ指定` から通常のフォルダ選択へ戻ったときに、`out/*` が再び候補へ出てしまう問題を修正しました。通常の法令選択は正式版の `data/normalized` だけに絞り、一時生成物は4yamlフォルダ指定で扱う運用を保ちます。

## 変更内容

- 通常フォルダ選択の候補生成から `out/*` 探索を削除
- 表示文言を `フォルダ選択（data/normalized）` に変更
- セッションに古い `out/...` の選択値が残っていた場合、先頭の `data/normalized` 候補へ戻す
- `out` に4yamlが存在しても通常候補に混ざらないことをテストで確認

## 検証

- `python -m pytest tests/test_mock_ui_yaml_folder_source.py tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 31 passed

<!-- PR_BODY_FILE: runs/20260602-122242754_feat-mock-ui-remove-out-folder-ghost-v1/PR_BODY.md -->
