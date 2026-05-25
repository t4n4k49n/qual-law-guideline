# RUN: 20260526-002546060_feat-mhlw-csv-annex2-table-parser

## 目的

9「CSVガイドライン」の `別紙2` について、公式page2 HTMLの表本体をCSV個別adapterでIR table nodeとして取り込む。

このRUNはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格や、正規化承認を前提にしない。

## 対象

- page1 local HTML: `data/human-readable/mhlw/csv_guideline/00tb6573.html`
- page2 local HTML: `data/human-readable/mhlw/csv_guideline/00tb6573_page2.html`
- page2 official URL: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=2`
- 出力確認先: `out/20260526-002546060_feat-mhlw-csv-annex2-table-parser/`

## 実施内容

- 公式page2 HTMLをlocal sourceとして追加した。
- CSV専用adapter `mhlw_csv_annex2_table_adapter` を追加した。
- `jp_mhlw_csv_guideline_v1` の `preprocess.mhlw_csv_annexes.annex2_html_path` でpage2 HTMLを明示した。
- `別紙2` 配下に、公式page2 HTML由来の `table` 2件と `table_row` 8件を追加した。
- rowspan/colspanはHTMLセル展開として処理し、各行に `cells` と列スキーマを保持した。
- 共通HTML抽出器や共通Parserには手を入れていない。

## 別紙2 table inventory

詳細は `csv_annex2_table_inventory.md` と `csv_annex2_table_inventory.json` に記録した。

| 表 | 見出し | 行数 | 列数 | 状態 |
| --- | --- | ---: | ---: | --- |
| 1 | カテゴリ分類表 | 7 | 20 | HTML表セルを展開し、列スキーマ付きで保持 |
| 2 | 本ガイドラインの対象外 | 1 | 2 | HTML表セルを展開し、列スキーマ付きで保持 |

## 共通/個別の境界

- 共通へ入れたもの: なし。
- 個別へ閉じたもの:
  - CSVガイドラインの公式page2 HTMLパス。
  - `別紙2` の2表構成。
  - `カテゴリ分類表` の20列スキーマ。
  - `本ガイドラインの対象外` の2列スキーマ。
  - MHLW page2 HTMLの空colspec行除外、rowspan/colspan展開。

## 今回入れない課題

- `別紙1` 画像のOCRまたは手入力転記。
- `別紙2` の記号値 `◎` / `○` / `△` / `―` と脚注番号の意味分解。
- `別紙2` のカテゴリ3など、複数行にまたがる意味単位のrecord統合。
- DQチェックシート向け候補粒度の最終確定。
- `data/normalized/` への昇格。

## 正規化完成までの残課題

- CSV `別紙2`: HTML表セルはIR化できたが、行単位はまだHTML上の表示行に近い。カテゴリ単位のrecord統合が必要。
- CSV `別紙2`: `◎` / `○` / `△` / `―` と脚注番号を分解し、実施要否・条件・脚注参照として意味列化する。
- CSV `別紙1`: 画像由来情報を取得し、OCRまたは手入力転記でIR化する。
- 正式版昇格は正規化RUNで別途行う。

## 正規化の度合い

- 本文階層: 既存Parser profileの水準を維持。
- `別紙2`: 表本体を `table` / `table_row` としてIRへ取り込み済み。HTMLセル単位の列スキーマは付与済み。
- `別紙2`: 意味値分解、脚注分解、カテゴリ単位record統合は未実施。
- `別紙1`: 画像参照のまま。OCR/転記は未実施。
- 正式版昇格: 未実施。

したがって、今回の成果は「CSV別紙2の表本体を欠落させず、列付きHTML tableとしてIRに載せる段階」であり、CSV別紙全体の完成正規化ではない。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_mhlw_csv_annex2_tables.py tests\test_mhlw_csv_annex_source_recovery.py tests\test_mhlw_csv_annexes.py tests\test_text2ir_csv_guideline.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `16 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.mhlw_csv_annex2_tables --input data\human-readable\mhlw\csv_guideline\00tb6573_page2.html --out-json runs\20260526-002546060_feat-mhlw-csv-annex2-table-parser\csv_annex2_table_inventory.json --out-md runs\20260526-002546060_feat-mhlw-csv-annex2-table-parser\csv_annex2_table_inventory.md
```

結果: inventory生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input out\20260526-002546060_feat-mhlw-csv-annex2-table-parser\00tb6573.extracted.txt --out-dir out\20260526-002546060_feat-mhlw-csv-annex2-table-parser --doc-id jp_mhlw_csv_guideline_annex2_table_v1 --title "医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン" --short-title "CSVガイドライン" --doc-type guideline --source-url https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573 --source-format html --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_mhlw_csv_guideline_v1 --candidate-visibility-profile-id jp_mhlw_csv_guideline_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功、qualitycheck warning なし。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-002546060_feat-mhlw-csv-annex2-table-parser --doc-id jp_mhlw_csv_guideline_annex2_table_v1 --mode normal --out runs\20260526-002546060_feat-mhlw-csv-annex2-table-parser\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-002546060_feat-mhlw-csv-annex2-table-parser --doc-id jp_mhlw_csv_guideline_annex2_table_v1 --mode normal --out runs\20260526-002546060_feat-mhlw-csv-annex2-table-parser\special_structure_audit.md
```

結果: `pass`
