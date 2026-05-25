# RUN: 20260525-233654758_feat-niid-annex-table-adapters-v1

## 目的

8「病原体等安全管理規程」の別表・付表について、前RUNで列復元候補とした対象をtable nodeとして分離保持する。

これはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

前RUN `20260525-231917460_feat-niid-annex-table-inventory` で列復元候補とした以下5件を対象にした。

- `付表2`
- `付表3`
- `付表4`
- `別表7`
- `別表10`

## 実装

- `src/qai_text2ir/niid_annex_tables.py` を追加した。
- `jp_niid_pathogen_safety_management_annex_v1` profileでのみ `niid_annex_tables.enabled` を有効化した。
- 共通parserの固定幅表検出は緩めていない。
- 対象5件を `annex -> table -> table_header -> table_row` として分離した。
- tableは現時点では `raw_line` 行保持とし、table単位に列候補を `reconstructed_columns` として持たせた。
- 各 `table_row` には `cells: [raw_line]` と `column_reconstruction_warning` を残し、セル単位の確定復元は次段階に回した。
- annex本文にはtable前の説明文だけを残し、table本体は子tableへ移した。

## 共通化しない理由

NIID別表・付表は、文書固有の別表番号、見出し、横長固定幅、ページ分割、複数行セルが強く絡む。共通parserに寄せると通常本文や番号付き要求事項を誤ってtable化する可能性が高いため、NIID専用adapterに閉じた。

## 結果

| 対象 | 形式 | rows | 状態 |
| --- | --- | ---: | --- |
| `付表2` | fixed_width_matrix | 28 | raw rows with column schema |
| `付表3` | fixed_width_matrix | 21 | raw rows with column schema |
| `付表4` | fixed_width_matrix | 24 | raw rows with column schema |
| `別表7` | fixed_width_matrix | 30 | raw rows with column schema |
| `別表10` | fixed_width_comparison_table | 33 | raw rows with column schema |

合計:

- table: 5
- table_header: 5
- table_row: 136

## 正規化度

このRUNで、8の一部別表・付表は「annex本文保持」から「table node分離」へ進んだ。

達成済み:

- 対象5件をtableとしてIR上で追跡できる。
- DQ候補に出せる `table_row` 粒度を確保した。
- table単位の列候補を持たせた。
- source spanは維持している。

未達:

- セル単位の列復元。
- 複数行セルの再結合。
- `別表7` / `別表10` の意味record化。
- `付表2` / `付表3` / `付表4` の横持ち列の確定。

したがって、この出力は「完全な表正規化」ではなく、「table node化と列候補付与まで」の段階とする。

## 正規化完成までの残課題

8 病原体等安全管理規程:

- `付表2`, `付表3`, `付表4`, `別表7`, `別表10` のセル単位復元。
- `別表4`, `別表5`, `別表8` の手動レビューと、adapter化するか原文保持に留めるかの判断。
- `別表2`, `別表3` をBSL/ABSL別の節構造として扱うか判断。
- `別表6`, `別表9` を番号付き要求事項として構造化するか判断。

6/7:

- `reconstructed_records` を正式な表行へ昇格するか判断。
- 注記、複数段ヘッダ、PDF視覚情報の扱いを確定する。

9:

- `別紙1` 画像取得/OCR判断。
- `別紙2` 表本体ソース確認。

全体:

- 正式な正規化RUNへ進む前に、復元済み・保留・対象外の区別を文書ごとに確定する。
- `data/normalized/` への昇格は未実施。

## この開発に入れない課題

- `別表4`, `別表5`, `別表8` の複雑表adapter化。
- セル単位の完全な列復元。
- 番号付き要求事項/節構造化。
- `data/normalized/` への昇格。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_niid_annex_inventory.py tests\test_text2ir_niid_pathogen_annex.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `13 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\niid\pathogen_safety_management\source_texts\Kanrikitei3_20240401.txt --out-dir out\20260525-233654758_feat-niid-annex-table-adapters-v1 --doc-id jp_niid_pathogen_safety_management_annex_tables_v1 --title "国立感染症研究所病原体等安全管理規程 別表・付表" --short-title "病原体等安全管理規程 別表" --doc-type guideline --source-url https://www.niid.go.jp/niid/images/biosafe/kanrikitei/Kanrikitei3_20240401.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_niid_pathogen_safety_management_annex_v1 --candidate-visibility-profile-id jp_niid_pathogen_safety_management_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-233654758_feat-niid-annex-table-adapters-v1 --doc-id jp_niid_pathogen_safety_management_annex_tables_v1 --mode normal --out runs\20260525-233654758_feat-niid-annex-table-adapters-v1\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-233654758_feat-niid-annex-table-adapters-v1 --doc-id jp_niid_pathogen_safety_management_annex_tables_v1 --mode normal --out runs\20260525-233654758_feat-niid-annex-table-adapters-v1\special_structure_audit.md
```

結果: `pass`

## 次のPR

計画上の残りは9「CSVガイドライン」別紙のソース補完。

ブランチ案:

- `feat/mhlw-csv-annex-source-recovery`
