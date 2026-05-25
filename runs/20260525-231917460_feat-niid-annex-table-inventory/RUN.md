# RUN: 20260525-231917460_feat-niid-annex-table-inventory

## 目的

8「病原体等安全管理規程」の別表・付表について、列復元に入る前に表別分類を行い、次のadapter実装対象を絞る。

これはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- 入力: `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- 対象:
  - `別表1` から `別表10`
  - `付表1-1` から `付表4`
- 出力:
  - `runs/20260525-231917460_feat-niid-annex-table-inventory/niid_annex_table_inventory.md`
  - `runs/20260525-231917460_feat-niid-annex-table-inventory/niid_annex_table_inventory.json`

## 実装

- `src/qai_text2ir/niid_annex_inventory.py` を追加した。
- 既存の `jp_niid_pathogen_safety_management_annex_v1` profileで生成したannex IRを入力に、文書固有の分類を行う。
- 共通parserや本文profileには変更を入れていない。
- 分類はNIID別表・付表固有の見出し、表形式、復元必要性に基づくため、共通化しない。

## 分類結果

詳細は `niid_annex_table_inventory.md` / `.json` を参照。

| 区分 | 対象 | 次アクション |
| --- | --- | --- |
| 列復元候補 | `付表2`, `付表3`, `付表4`, `別表7`, `別表10` | table adapter候補 |
| 複雑な列復元候補 | `別表4`, `別表5`, `別表8` | 手動レビュー後にadapter候補 |
| 列復元対象外 | `別表1`, `付表1-1` | annex本文保持 |
| 番号・節構造化候補 | `付表1-2`, `付表1-3`, `別表2`, `別表3`, `別表6`, `別表9` | 列復元ではなく番号/節構造化を別判断 |

## 判断

- `付表2`, `付表3`, `付表4`, `別表7`, `別表10` は、列名と行単位を比較的説明しやすいため、次のtable adapter候補とする。
- `別表4`, `別表5`, `別表8` は横長で複数行セル・注記・箇条書き混在が強いため、いきなりadapter化せず手動レビューを先に行う。
- `別表2`, `別表3`, `別表6`, `別表9` は表列復元ではなく、BSL/ABSL節や番号付き要求事項としての構造化を検討する。

## 正規化度

このRUNで正規化度そのものは大きく上げていない。到達点は、8の別表・付表について「どれを列復元するか」を明確にした段階。

達成済み:

- 16個の別表・付表を分類済み。
- 列復元候補、複雑候補、対象外、番号/節構造化候補を分離。
- 次PRで扱う実装対象を絞った。

未達:

- table node化。
- table_row化。
- セル単位の意味付け。
- DQ候補粒度の最終判断。

## 正規化完成までの残課題

8 病原体等安全管理規程:

- `付表2`, `付表3`, `付表4`, `別表7`, `別表10` のtable adapter実装。
- `別表4`, `別表5`, `別表8` の手動レビューと、adapter化するか原文保持に留めるかの判断。
- `別表2`, `別表3` をBSL/ABSL別の節構造として扱うか判断。
- `別表6`, `別表9` を番号付き要求事項として構造化するか判断。

6/7:

- PR #171で追加した `reconstructed_records` を正式な表行として昇格するか判断。
- 注記、複数段ヘッダ、PDF視覚情報の扱いを確定する。

9:

- `別紙1` 画像取得/OCR判断。
- `別紙2` 表本体ソース確認。

全体:

- 正式な正規化RUNへ進む前に、復元候補と保留理由を文書ごとに確定する必要がある。
- `data/normalized/` への昇格は未実施。

## この開発に入れない課題

- NIID別表・付表のtable adapter実装。
- `別表4`, `別表5`, `別表8` の複雑表の列復元。
- `別表2`, `別表3`, `別表6`, `別表9` の番号/節構造化。
- `data/normalized/` への昇格。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_niid_annex_inventory.py tests\test_text2ir_niid_pathogen_annex.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `12 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\niid\pathogen_safety_management\source_texts\Kanrikitei3_20240401.txt --out-dir out\20260525-231917460_feat-niid-annex-table-inventory --doc-id jp_niid_pathogen_safety_management_annex_inventory_v1 --title "国立感染症研究所病原体等安全管理規程 別表・付表" --short-title "病原体等安全管理規程 別表" --doc-type guideline --source-url https://www.niid.go.jp/niid/images/biosafe/kanrikitei/Kanrikitei3_20240401.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_niid_pathogen_safety_management_annex_v1 --candidate-visibility-profile-id jp_niid_pathogen_safety_management_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-231917460_feat-niid-annex-table-inventory --doc-id jp_niid_pathogen_safety_management_annex_inventory_v1 --mode normal --out runs\20260525-231917460_feat-niid-annex-table-inventory\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-231917460_feat-niid-annex-table-inventory --doc-id jp_niid_pathogen_safety_management_annex_inventory_v1 --mode normal --out runs\20260525-231917460_feat-niid-annex-table-inventory\special_structure_audit.md
```

結果: `pass`

## 次のPR

次は、列復元候補のうち比較的境界を説明しやすい対象をtable adapter化する。

ブランチ案:

- `feat/niid-annex-table-adapters-v1`

対象候補:

- `付表2`
- `付表3`
- `付表4`
- `別表7`
- `別表10`

`別表4`, `別表5`, `別表8` は複雑候補として次PRには入れず、手動レビュー後に別フェーズ化する。
