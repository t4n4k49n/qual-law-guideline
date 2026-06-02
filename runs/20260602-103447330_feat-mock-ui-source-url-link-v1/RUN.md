# RUN: feat/mock-ui-source-url-link-v1

## 目的

モックUIで法令フォルダを選択した直後に、該当する meta YAML の法令ソースURLを表示し、元の法令を開きやすくする。

## 変更内容

- `doc.sources[].url` から法令ソースURLを抽出する処理を追加。
- フォルダ選択（`data/normalized`, `out/*`）の選択メニュー直下に、選択中フォルダのソースリンクを表示。
- 壊れた meta YAML でも `url:` 行だけは回収できるフォールバックを追加。
- URL抽出と表示用短縮の単体テストを追加。

## 検証

- `python -m pytest tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 20 passed
