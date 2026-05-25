# RUN: 20260526-040709227_feat-mhlw-csv-annex2-semantic-records

## 目的

9「CSVガイドライン」の `別紙2` について、公式page2 HTMLから取り込んだ表セルを、カテゴリ単位recordと意味値へ分解する。

このRUNはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格や、正規化承認を前提にしない。

## 対象

- page1 local HTML: `data/human-readable/mhlw/csv_guideline/00tb6573.html`
- page2 local HTML: `data/human-readable/mhlw/csv_guideline/00tb6573_page2.html`
- 出力確認先: `out/20260526-040709227_feat-mhlw-csv-annex2-semantic-records/`

## 実施内容

- `mhlw_csv_annex2_table_adapter` に `semantic_records` を追加した。
- `カテゴリ分類表` の表示行7行を、カテゴリ単位の5 recordへ束ねた。
- `カテゴリ3` は2つの表示行を1つのrecordにし、各行を `variants` として保持した。
- `◎` / `○` / `△` / `―` を `status` / `meaning` / `footnote_refs` に分解した。
- 表2 `本ガイドラインの対象外` も1 semantic recordとして保持した。
- 元のHTML table row、`cells`、列スキーマ、source spanは維持した。

## 結果

詳細は `csv_annex2_semantic_inventory.md` と `csv_annex2_semantic_inventory.json` に記録した。

| 表 | 意味record | 内容 |
| --- | ---: | --- |
| `カテゴリ分類表` | 5 | カテゴリ1,2,3,4,5。カテゴリ3は2 variants |
| `本ガイドラインの対象外` | 1 | 対象外説明を1 recordとして保持 |

## warning / 保留

- `カテゴリ2` はHTML上の該当セルが空の箇所を含むため、`blank_semantic_value` を残した。
- `カテゴリ2` は `category_name` が空欄のため、`blank_category_name_preserved` を残した。
- `semantic_records` はレビュー候補であり、正式な `table_row` 置換やDQ候補粒度確定は正規化RUN readinessで判断する。

## 正規化完成までの残課題

- CSV `別紙1`: 画像由来情報を取得し、OCRまたは手入力転記でIR化する。
- CSV `別紙2`: semantic recordを正式な選択候補粒度にするか、既存 `table_row` を候補に維持するかを正規化RUN readinessで判断する。
- 正式版昇格は正規化RUNで別途行う。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_mhlw_csv_annex2_tables.py tests\test_text2ir_csv_guideline.py tests\test_mhlw_csv_annex_source_recovery.py tests\test_mhlw_csv_annexes.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `17 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.mhlw_csv_annex2_tables --input data\human-readable\mhlw\csv_guideline\00tb6573_page2.html --out-json runs\20260526-040709227_feat-mhlw-csv-annex2-semantic-records\csv_annex2_semantic_inventory.json --out-md runs\20260526-040709227_feat-mhlw-csv-annex2-semantic-records\csv_annex2_semantic_inventory.md
```

結果: inventory生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input out\20260526-040709227_feat-mhlw-csv-annex2-semantic-records\00tb6573.extracted.txt --out-dir out\20260526-040709227_feat-mhlw-csv-annex2-semantic-records --doc-id jp_mhlw_csv_guideline_annex2_semantic_v1 --title "医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン" --short-title "CSVガイドライン" --doc-type guideline --source-url https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573 --source-format html --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_mhlw_csv_guideline_v1 --candidate-visibility-profile-id jp_mhlw_csv_guideline_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-040709227_feat-mhlw-csv-annex2-semantic-records --doc-id jp_mhlw_csv_guideline_annex2_semantic_v1 --mode normal --out runs\20260526-040709227_feat-mhlw-csv-annex2-semantic-records\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-040709227_feat-mhlw-csv-annex2-semantic-records --doc-id jp_mhlw_csv_guideline_annex2_semantic_v1 --mode normal --out runs\20260526-040709227_feat-mhlw-csv-annex2-semantic-records\special_structure_audit.md
```

結果: `pass`
