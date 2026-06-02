## まとめ

モックUIの法令データ切替で、txtconcatファイルアップロードではなく、4 YAML を内包するフォルダを直接選べるようにしました。レビューや検証の場で一時生成した YAML セットをセッション内で扱いやすくしつつ、通常の法令フォルダ選択には余計な候補を混ぜない運用へ寄せます。

## 変更内容

- `アップロード（4yamlのtxtconcat形式）` を `4yaml内包フォルダ指定` に変更
- OS のフォルダ選択ダイアログでフォルダを選べるように変更
- 有効な 4 YAML セットがちょうど1つある場合だけ、選択モードと法令データを切り替え
- キャンセル、不足、複数セット、prefix不一致では、選択前のモード・法令・選択済み有効パスを維持
- Streamlit の radio widget key と確定済みモードを分離し、復元時の widget state 例外を回避
- txtconcat アップロード依存をモックUIから削除

## 検証

- `python -m pytest tests/test_mock_ui_yaml_folder_source.py tests/test_mock_ui_source_links.py tests/test_mock_ui_render.py -q`
  - 27 passed

<!-- PR_BODY_FILE: runs/20260602-105640272_feat-mock-ui-yaml-folder-source-v1/PR_BODY.md -->
