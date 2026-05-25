# RUN: 20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1

## 目的

8「病原体等安全管理規程」のtable化済み5表についてセル単位復元v1を追加し、16件すべての別表・付表を正規化RUN readinessでどう扱うか判定する。

このRUNはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- `付表2`
- `付表3`
- `付表4`
- `別表7`
- `別表10`

## 実施内容

- NIID専用adapter内で、2つ以上の空白による固定幅セル分割を追加した。
- 列数どおりに分割できる行だけ `cells` と `columns` を付けた。
- 分割できない行は `cells: [raw_line]` を維持し、`fixed_width_cell_split_deferred` warningを付けた。
- table単位に `cell_reconstruction: fixed_width_cells_v1`、復元行数、保留行数を記録した。
- 共通parserや共通table検出には変更を入れていない。
- 16件すべての別表・付表に `normalization_readiness` を付け、昇格候補としての持ち方を決め切った。

## 結果

詳細は `niid_annex_table_cell_inventory.md` と `niid_annex_table_cell_inventory.json` に記録した。

| 対象 | rows | セル復元 | 保留 | readiness |
| --- | ---: | ---: | ---: | --- |
| `付表2` | 28 | 0 | 28 | `promotion_candidate_as_raw_table` |
| `付表3` | 21 | 15 | 6 | `promotion_candidate_as_partial_cell_table` |
| `付表4` | 24 | 5 | 19 | `promotion_candidate_as_partial_cell_table` |
| `別表7` | 30 | 11 | 19 | `promotion_candidate_as_partial_cell_table` |
| `別表10` | 33 | 10 | 23 | `promotion_candidate_as_partial_cell_table` |

16件全体の判定は `niid_annex_readiness.md` と `niid_annex_readiness.json` に記録した。

## Readiness判定

| 判定 | 対象 | 意味 |
| --- | --- | --- |
| `promotion_candidate_as_annex_text` | `別表1`, `付表1-1` | 表ではない説明本文として昇格候補 |
| `promotion_candidate_as_numbered_annex_text` | `付表1-2`, `付表1-3`, `別表6`, `別表9` | 番号付き要求事項/評価項目として原文保持で昇格候補 |
| `promotion_candidate_as_sectioned_annex_text` | `別表2`, `別表3` | BSL/ABSL別の節型本文として昇格候補 |
| `promotion_candidate_as_raw_annex_text` | `別表4`, `別表5`, `別表8` | 複雑表は原文保持で昇格候補 |
| `promotion_candidate_as_raw_table` | `付表2` | table化済みraw rows + 列スキーマで昇格候補 |
| `promotion_candidate_as_partial_cell_table` | `付表3`, `付表4`, `別表7`, `別表10` | 一部セル復元済みtableとして昇格候補 |

## 判断

今回のセル復元は、列数が一致する行だけに限定した。

理由:

- `付表2` は見出し・セル本文の折返しが多く、単純な固定幅分割では安全にセル化できない。
- `付表4` はABSLごとの複数行セルが多く、先頭行だけ分割できても後続行を同じrecordへ束ねる必要がある。
- `別表7` / `別表10` は複数行にまたがる意味単位があり、分割できる行だけを先にセル候補として保持する方が安全。
- raw rowとsource spanを失うとレビュー不能になるため、保留行は必ずrawのまま残す。

## 正規化の度合い

- table node化: 済み。
- table_row保持: 済み。
- セル単位復元: 一部のみ。
- 複数行record統合: 未実施。
- 複雑表の追加adapter判断: 未実施。

したがって、今回の成果は「NIID table化済み5表のうち、安全に分割できる行へセル候補を付けた段階」であり、完全な表正規化ではない。

## このPRで結論を出した事項

- `付表2` は複数行セルを無理に復元せず、raw table + 列スキーマで昇格候補とする。
- `付表3`, `付表4`, `別表7`, `別表10` は一部セル復元済みtableとして昇格候補とする。
- `別表4`, `別表5`, `別表8` は複雑表adapter化を通常開発でさらに引き延ばさず、原文保持の昇格候補とする。
- `別表2`, `別表3`, `別表6`, `別表9` は列復元対象ではなく、節/番号型annex textとして昇格候補とする。
- `data/normalized/` への昇格は正規化RUNで実施する。

## 正規化RUNに渡す判定

8「病原体等安全管理規程」については、このPRの成果を正規化RUN readiness判定に渡せる。

正規化RUNでは、16件すべてを昇格候補に含める前提でレビューする。ただし、昇格モードは同一ではなく、table/partial cell/raw annex textを併用する。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_niid_annex_table_cells.py tests\test_text2ir_niid_pathogen_annex.py tests\test_niid_annex_inventory.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `14 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\niid\pathogen_safety_management\source_texts\Kanrikitei3_20240401.txt --out-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_readiness_v1 --title "国立感染症研究所病原体等安全管理規程 別表・付表" --short-title "病原体等安全管理規程 別表" --doc-type guideline --source-url https://www.niid.go.jp/niid/images/biosafe/kanrikitei/Kanrikitei3_20240401.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_niid_pathogen_safety_management_annex_v1 --candidate-visibility-profile-id jp_niid_pathogen_safety_management_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_readiness_v1 --mode normal --out runs\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_readiness_v1 --mode normal --out runs\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1\special_structure_audit.md
```

結果: `pass`
