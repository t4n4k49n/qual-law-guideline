# RUN: feat/mock-ui-yaml-folder-source-v1

## 目的

モックUIの法令選択で、未使用になっている txtconcat アップロード方式をやめ、4 YAML を内包するフォルダ指定方式に変更する。

## 変更内容

- データソース切替の「アップロード（4yamlのtxtconcat形式）」を「4yaml内包フォルダ指定」に変更。
- 指定フォルダ内に `.regdoc_ir.yaml` / `.parser_profile.yaml` / `.regdoc_profile.yaml` / `.meta.yaml` が各1件だけある場合のみ有効化。
- 4 YAML セットが不足、複数、または prefix 不一致の場合は異常扱いにし、「フォルダ選択」ONへ戻す。
- 無効なフォルダ指定では既存の法令データへ切り替えず、現在のフォルダ選択状態を維持する。
- `4yaml内包フォルダ指定` 選択時に OS のフォルダ選択ダイアログを開き、有効フォルダ選択後だけモードを確定する。
- キャンセル・無効フォルダでは選択前のモード、法令、選択済み有効パスを維持する。
- Streamlit の radio widget key と確定済みモードを分離し、復元時に描画済み widget key を直接変更しないようにした。
- txtconcat アップロード依存をモックUIから削除。

## 検証

- `python -m pytest tests/test_mock_ui_yaml_folder_source.py tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 27 passed
