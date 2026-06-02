<!-- PR_BODY_FILE: runs/20260602-150000000_feat-mock-ui-article-p1-display-audit-fix-v1/PR_BODY.md -->

## まとめ
第一条第一項の統合表示を、データ構造を壊さない表示上の例外として整理し直しました。省略判定を表示文字列ではなく論理NID列で行うようにし、第一項統合ON時でも第二項・第三項や親子関係の表示が崩れないようにしています。これにより、チェックシート表示で必要な親・先祖文脈を維持しながら、重複する文脈だけを意図どおり省略できるようになります。

## 変更内容
- 第一項統合表示の仕様をRUNに整理
- 省略判定を表示文字列比較からNID列比較へ変更
- `兄弟のみ先祖省略` を同一親の兄弟だけに限定
- `共通先祖省略` で第一項統合後の表示文字列を比較キーにしないよう修正
- デバッグトレースに比較対象NIDを追加
- 仕様ベースの手動確認チェックリストを追加
- 親item未選択・子subitem選択、親子連続、兄弟連続などの回帰テストを追加

## 動作確認
- `python -m py_compile apps/mock_gmp_checklist_ui.py src/qai_mock_ui/render.py`
- `python -m pytest tests/test_mock_ui_render.py tests/test_mock_ui_yaml_folder_source.py -q`
  - `34 passed`
- 手動確認:
  - `runs/20260602-150000000_feat-mock-ui-article-p1-display-audit-fix-v1/MANUAL_CHECKLIST.md`
  - 結果: 概ね良好
