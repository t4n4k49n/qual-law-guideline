<!-- PR_BODY_FILE: runs/20260526-121357155_feat-niid-visual-table-integration-plan-v1/PR.md -->

## まとめ

NIID病原体等安全管理規程の視覚レビュー済み表を既存adapter出力に組み込み、これまでraw/partial扱いだった主要5表をcompleteなtable recordとして扱える状態にしました。元の固定幅raw rowsは監査用に残しているため、レビュー済み構造を使いながら、後から原抽出との対応も追えます。

## 変更内容

- 視覚レビュー済み5表のNIID専用データ定義を追加
- `付表2`, `付表3`, `付表4`, `別表7`, `別表10` をvisual reviewed tableとしてadapter出力へ統合
- 既存raw rowsを `raw_table_audit` に保持
- readiness decisionを `promotion_candidate_as_visual_reviewed_table` へ更新
- 関連テストをvisual reviewed complete前提へ更新
- 1 PRで完結する実施計画と結果をRUNに記録

## 検証

- `python -m pytest tests\test_niid_annex_table_cells.py tests\test_text2ir_niid_pathogen_annex.py tests\test_niid_annex_inventory.py -q`
- `python -m pytest -q`
- `git diff --check`

## 次アクション

次は正式な正規化RUNとして、このadapter出力をもとに `promotion_candidate/` を作り、レビュー後に `data/normalized/` へ昇格する段階に進めます。
