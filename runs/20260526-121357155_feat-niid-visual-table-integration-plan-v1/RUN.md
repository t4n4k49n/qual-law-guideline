# RUN: 20260526-121357155_feat-niid-visual-table-integration-plan-v1

## 目的

NIID病原体等安全管理規程について、視覚レビュー復元済みの `付表2`, `付表3`, `付表4`, `別表7`, `別表10` を既存のannex table adapter出力へ組み込み、正式な正規化RUN直前の昇格候補判断に近づける。

このRUNはコード実装RUNであり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 計画

1 PRで完結させる。

1. NIID専用adapterに視覚レビュー済み5表のrecord定義を追加する。
2. 既存の固定幅raw rowsは破棄せず、`raw_table_audit` としてtable nodeに保持する。
3. table rowsは視覚レビュー済みrecordへ差し替え、`cell_reconstruction_status=complete` として扱う。
4. readiness decisionを `promotion_candidate_as_visual_reviewed_table` に更新する。
5. 既存テストを、raw/partial前提からvisual reviewed complete前提へ更新する。

2 PRに分ける場合の境界は、PR1をデータ定義追加、PR2をadapter差し替えにする案だった。ただし変更範囲がNIID専用adapterとテストに閉じるため、今回は1 PRで進めた。

## 実施内容

- `src/qai_text2ir/niid_visual_reviewed_tables.py` を追加し、v1/v2視覚レビューRUNの5表をNIID専用データとして定義した。
- `src/qai_text2ir/niid_annex_tables.py` を更新し、固定幅分割後に視覚レビュー済みrecordへ差し替える処理を追加した。
- `parser=niid_annex_table_adapter` は維持し、視覚レビュー由来であることは `visual_review_parser` に記録した。
- 固定幅分割の旧結果は `raw_table_audit` に残した。
- `付表3`, `別表7`, `別表10` は固定幅監査用列と最終視覚復元列を分けた。
- テストを更新し、5表がcomplete tableとして出力されることを確認した。

## 成果

| annex | records | status |
| --- | ---: | --- |
| 付表2 | 4 | visual reviewed complete |
| 付表3 | 15 | visual reviewed complete |
| 付表4 | 4 | visual reviewed complete |
| 別表7 | 18 | visual reviewed complete |
| 別表10 | 13 | visual reviewed complete |

## 残課題

- 正式な正規化RUNは未実施。
- 次に正規化RUNへ進む場合は、このadapter出力をもとに `promotion_candidate/` を作り、PR承認後に `data/normalized/` へ昇格する。
- `別表4`, `別表5`, `別表8` はraw annex textとして保持する判断のままであり、追加の視覚表復元対象にはしていない。

## 検証

- `python -m pytest tests\test_niid_annex_table_cells.py tests\test_text2ir_niid_pathogen_annex.py tests\test_niid_annex_inventory.py -q`
  - `7 passed`
- `python -m pytest -q`
  - `244 passed, 1 skipped`
