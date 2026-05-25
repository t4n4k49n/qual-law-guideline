# RUN: 20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1

## 目的

8「病原体等安全管理規程」のtable化済み5表について、セル単位復元v1を追加する。

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

## 結果

詳細は `niid_annex_table_cell_inventory.md` と `niid_annex_table_cell_inventory.json` に記録した。

| 対象 | rows | セル復元 | 保留 | 状態 |
| --- | ---: | ---: | ---: | --- |
| `付表2` | 28 | 0 | 28 | partial |
| `付表3` | 21 | 15 | 6 | partial |
| `付表4` | 24 | 5 | 19 | partial |
| `別表7` | 30 | 11 | 19 | partial |
| `別表10` | 33 | 10 | 23 | partial |

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

## 今回入れない課題

- `付表2` の複数行セル復元。
- `付表4` のABSL単位record統合。
- `別表7` / `別表10` の複数行record統合。
- `別表4`, `別表5`, `別表8` の複雑表adapter化。
- `別表2`, `別表3`, `別表6`, `別表9` の節/番号構造化。
- `data/normalized/` への昇格。

## 正規化完成までの残課題

8 病原体等安全管理規程:

- `付表2` は単純セル分割では進めず、複数行セル/見出し再構成を別フェーズ化する。
- `付表4` はABSL単位のrecord統合を検討する。
- `別表7` / `別表10` は記帳項目・具体的内容・参照条項を複数行recordとして束ねる。
- `別表4`, `別表5`, `別表8` は計画Mで複雑表レビューを行う。
- `別表2`, `別表3`, `別表6`, `別表9` は列復元ではなく節/番号構造化として判断する。

全体:

- 正式な正規化RUNへ進む前に、復元済み行、保留行、原文保持対象を文書ごとに確定する。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_niid_annex_table_cells.py tests\test_text2ir_niid_pathogen_annex.py tests\test_niid_annex_inventory.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `14 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\niid\pathogen_safety_management\source_texts\Kanrikitei3_20240401.txt --out-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_cell_reconstruction_v1 --title "国立感染症研究所病原体等安全管理規程 別表・付表" --short-title "病原体等安全管理規程 別表" --doc-type guideline --source-url https://www.niid.go.jp/niid/images/biosafe/kanrikitei/Kanrikitei3_20240401.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_niid_pathogen_safety_management_annex_v1 --candidate-visibility-profile-id jp_niid_pathogen_safety_management_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_cell_reconstruction_v1 --mode normal --out runs\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1 --doc-id jp_niid_pathogen_safety_management_cell_reconstruction_v1 --mode normal --out runs\20260526-014107139_feat-niid-annex-table-cell-reconstruction-v1\special_structure_audit.md
```

結果: `pass`
