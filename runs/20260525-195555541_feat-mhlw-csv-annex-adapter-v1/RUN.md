# RUN: 20260525-195555541_feat-mhlw-csv-annex-adapter-v1

## 目的

9「CSVガイドライン」の `別紙1` / `別紙2` を、本文Parser profileへ混ぜずに個別adapterとして分離する。

このRUNはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格や、正規化承認を前提にしない。

## 対象

- ソース: `data/human-readable/mhlw/csv_guideline/00tb6573.html`
- 抽出TXT: `out/20260525-195555541_feat-mhlw-csv-annex-adapter-v1/00tb6573.extracted.txt`
- 公開元URL: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573`
- 出力確認先: `out/20260525-195555541_feat-mhlw-csv-annex-adapter-v1/`

## 実施内容

- CSVガイドライン専用adapter `mhlw_csv_annex_adapter` を追加した。
- `jp_mhlw_csv_guideline_v1` の `preprocess.mhlw_csv_annexes.enabled` で明示的に有効化した。
- 共通HTML抽出器 `extract_mhlw_t_doc_lines` には別紙固有処理を入れていない。
- IR上では本文末尾に混入していた別紙表示を `chapter 10` から切り離し、root直下の `annex` ノードとして保持した。
- HTML inventoryで、抽出TXTだけでは見えない `別紙1` の画像hrefと `別紙2` の表行有無を確認できるようにした。

## 別紙inventory

詳細は `runs/20260525-195555541_feat-mhlw-csv-annex-adapter-v1/csv_annex_inventory.md` と `csv_annex_inventory.json` に記録した。

| 別紙 | IRでの保持 | HTML確認結果 | 抽出可否 | 判断 |
| --- | --- | --- | --- | --- |
| 別紙1 | `annex1`、見出し `コンピュータ化システムのライフサイクルモデル`、表示ラベル `画像1 (36KB)` | `href=t_img?img=6676058` | 内容テキストは不可 | 画像参照メタ情報のみ保持。OCRは次フェーズ以降。 |
| 別紙2 | `annex2`、見出し `カテゴリ分類表と対応例` | HTML内の後続 `tr` は `0` | 表本体は不可 | 表題のみ保持。表本体復元や代替ソース確認は次フェーズ以降。 |

## 共通/個別の境界

- 共通へ入れたもの: なし。
- 個別へ閉じたもの:
  - CSVガイドライン固有の `別紙1` / `別紙2` 判定。
  - `別紙1` の画像リンク inventory。
  - `別紙2` の「表題のみで表本体なし」という判定。
  - `chapter 10` 末尾からの別紙プレースホルダ分離。

## 今回入れない課題

- `別紙1` 画像の取得/OCR。
- `別紙2` 表本体の代替ソース取得、または画像・PDF等からの復元。
- 別紙表の列復元、意味列への正規化、DQチェックシート向けの最終候補粒度判断。
- `data/normalized/` への昇格。

これらは、今回の「別紙の有無・形式・抽出可否を追跡可能にする」開発を超えるため、別フェーズで扱う。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_mhlw_csv_annexes.py tests\test_text2ir_csv_guideline.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `12 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input out\20260525-195555541_feat-mhlw-csv-annex-adapter-v1\00tb6573.extracted.txt --out-dir out\20260525-195555541_feat-mhlw-csv-annex-adapter-v1 --doc-id jp_mhlw_csv_guideline_annex_adapter_v1 --title "医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン" --short-title "CSVガイドライン" --doc-type guideline --source-url https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573 --source-format html --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_mhlw_csv_guideline_v1 --candidate-visibility-profile-id jp_mhlw_csv_guideline_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功、qualitycheck warning なし。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-195555541_feat-mhlw-csv-annex-adapter-v1 --doc-id jp_mhlw_csv_guideline_annex_adapter_v1 --mode normal --out runs\20260525-195555541_feat-mhlw-csv-annex-adapter-v1\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-195555541_feat-mhlw-csv-annex-adapter-v1 --doc-id jp_mhlw_csv_guideline_annex_adapter_v1 --mode normal --out runs\20260525-195555541_feat-mhlw-csv-annex-adapter-v1\special_structure_audit.md
```

結果: `pass`

## 正規化の度合い

- 本文階層: 既存Parser profileの水準を維持。
- 別紙: 形式・見出し・抽出可否のinventory化まで。
- 表の列復元/意味正規化: 未実施。
- 正式版昇格: 未実施。

したがって、今回の成果は「別紙を欠落・本文混入させないための開発成果」であり、別紙内容の完全正規化ではない。
