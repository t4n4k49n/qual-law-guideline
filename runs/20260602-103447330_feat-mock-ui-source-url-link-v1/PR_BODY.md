## まとめ

モックUIで法令を選んだ直後に、参照元の法令ソースへ移動できるリンクを表示するようにしました。確認対象の法令と原典の往復がしやすくなり、レビュー時の根拠確認にかかる手間を減らします。

## 変更内容

- `meta.yaml` の `doc.sources[].url` から法令ソースURLを抽出
- フォルダ選択（`data/normalized`, `out/*`）の選択メニュー直下に、選択中フォルダのソースリンクを表示
- meta YAML が一部壊れていても `url:` 行を拾えるフォールバックを追加
- URL抽出と表示用短縮の単体テストを追加

## 検証

- `python -m pytest tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 20 passed

<!-- PR_BODY_FILE: runs/20260602-103447330_feat-mock-ui-source-url-link-v1/PR_BODY.md -->
