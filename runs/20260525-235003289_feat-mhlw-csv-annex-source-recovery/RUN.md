# RUN: 20260525-235003289_feat-mhlw-csv-annex-source-recovery

## 目的

9「CSVガイドライン」の `別紙1` / `別紙2` について、前フェーズで残したソース補完判断をCSV個別開発として整理する。

このRUNはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格や、正規化承認を前提にしない。

## 対象

- local page1 HTML: `data/human-readable/mhlw/csv_guideline/00tb6573.html`
- 公式page1: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=1`
- 公式page2: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=2`
- 別紙1画像: `https://www.mhlw.go.jp/web/t_img?img=6676058`
- 補助取得先: `out/20260525-235003289_feat-mhlw-csv-annex-source-recovery/`
- 共有成果: `runs/20260525-235003289_feat-mhlw-csv-annex-source-recovery/`

## 実施内容

- CSVガイドライン専用のソース回収inventory `qai_text2ir.mhlw_csv_annex_source_recovery` を追加した。
- 共通HTML抽出器や共通Parserには手を入れていない。
- `別紙1` は公式画像エンドポイントを回収候補として特定し、HTTP 200を確認した。
- `別紙2` はlocal page1 HTMLでは表題のみだが、公式page2 HTMLに表本体があることを確認した。
- 前フェーズの「HTMLに表本体なし」という記録は、正確には「localに保存済みのpage1 HTMLには表本体なし」と整理した。

## ソース回収inventory

詳細は `csv_annex_source_recovery.md` と `csv_annex_source_recovery.json` に記録した。

| 別紙 | 回収候補 | 状態 | OCR | 次フェーズ判断 |
| --- | --- | --- | --- | --- |
| 別紙1 | `https://www.mhlw.go.jp/web/t_img?img=6676058` | HTTP 200 | 要 | 画像取得後、OCRまたは手入力転記で本文化する。 |
| 別紙2 | `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=2` | 公式page2に表本体あり | 不要 | page2 HTMLを正本候補として取得し、HTML表parserを個別実装する。 |

## 共通/個別の境界

- 共通へ入れたもの: なし。
- 個別へ閉じたもの:
  - CSVガイドライン固有の公式page2 URL。
  - `別紙1` の画像エンドポイント到達性判定。
  - `別紙2` の公式page2表本体候補判定。
  - `別紙2` page2 HTMLが表タイトルではなく表本体から始まるという実データ上の注意。

## 今回入れない課題

- `別紙1` 画像ファイルのGit管理対象化。
- `別紙1` のOCR、または手入力転記。
- `別紙2` page2 HTML表のIR table node化。
- `別紙2` 表セルの列復元、意味列への確定正規化。
- `data/normalized/` への昇格。

これらはソース回収判断を超えるため、次フェーズ以降で扱う。

## 正規化完成までの残課題

- CSV `別紙2`: 公式page2 HTMLを入力として表本体を取り込み、`table` / `table_row` として保持する。
- CSV `別紙2`: カテゴリ、内容、各文書・試験列、備考の列スキーマを確定する。
- CSV `別紙1`: 画像を取得し、OCRまたは手入力転記でライフサイクルモデルの内容を本文化する。
- CSV `別紙1`: 画像由来情報を、figure扱いにするか、補助表/説明ノードにするかを決める。
- 正式版昇格は正規化RUNで別途行う。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_mhlw_csv_annex_source_recovery.py tests\test_mhlw_csv_annexes.py tests\test_text2ir_csv_guideline.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `14 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.mhlw_csv_annex_source_recovery --input data\human-readable\mhlw\csv_guideline\00tb6573.html --page2-html out\20260525-235003289_feat-mhlw-csv-annex-source-recovery\00tb6573_page2.html --image-http-status 200 --out-json runs\20260525-235003289_feat-mhlw-csv-annex-source-recovery\csv_annex_source_recovery.json --out-md runs\20260525-235003289_feat-mhlw-csv-annex-source-recovery\csv_annex_source_recovery.md
```

結果: source recovery inventory生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input out\20260525-235003289_feat-mhlw-csv-annex-source-recovery\00tb6573.extracted.txt --out-dir out\20260525-235003289_feat-mhlw-csv-annex-source-recovery --doc-id jp_mhlw_csv_guideline_source_recovery_v1 --title "医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン" --short-title "CSVガイドライン" --doc-type guideline --source-url https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573 --source-format html --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_mhlw_csv_guideline_v1 --candidate-visibility-profile-id jp_mhlw_csv_guideline_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功、qualitycheck warning なし。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-235003289_feat-mhlw-csv-annex-source-recovery --doc-id jp_mhlw_csv_guideline_source_recovery_v1 --mode normal --out runs\20260525-235003289_feat-mhlw-csv-annex-source-recovery\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-235003289_feat-mhlw-csv-annex-source-recovery --doc-id jp_mhlw_csv_guideline_source_recovery_v1 --mode normal --out runs\20260525-235003289_feat-mhlw-csv-annex-source-recovery\special_structure_audit.md
```

結果: `pass`
