# RUN: 20260525-134750168_feat-csv-guideline-parser-v1

## 目的

9「CSVガイドライン」向けの `text2ir` parser profile を開発する。

このRUNはParser開発であり、正式な正規化RUNではない。`data/normalized/` への昇格や、正規化承認を前提にしない。

## 対象

- ソース: `data/human-readable/mhlw/csv_guideline/00tb6573.html`
- 抽出TXT: `out/20260525-134750168_feat-csv-guideline-parser-v1/00tb6573.extracted.txt`
- 公開元URL: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573`
- 出力確認先: `out/20260525-134750168_feat-csv-guideline-parser-v1/`

## 実施内容

- CSVガイドライン専用profile `jp_mhlw_csv_guideline_v1` を追加した。
  - 共通 `jp_guideline_default_v1` を継承する。
  - MHLW通知の前文を本文開始の `1．総則` まで除外する。
  - 重複する文書タイトル行の除去は、この専用profileに閉じる。
  - 章番号 `1．` と節番号 `1．1` は既存のJP共通markerを利用する。
- `extract-mhlw-html` でMHLW HTMLから本文候補TXTを生成した。
- 実データbundleを `out/` に生成し、構造確認を行った。
- 共通profileや共通parserには変更を入れていない。
  - CSV固有の通知名・タイトル名は、共通規則に混ぜない。
  - 今後ほかのMHLW通知HTMLでも同じ構造が確認できた場合だけ、共通化を再検討する。

## 検証

```powershell
.venv\Scripts\python.exe -m pytest tests\test_text2ir_csv_guideline.py -q
```

結果: `3 passed`

```powershell
.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input out\20260525-134750168_feat-csv-guideline-parser-v1\00tb6573.extracted.txt --out-dir out\20260525-134750168_feat-csv-guideline-parser-v1 --doc-id jp_mhlw_csv_guideline_20101021 --title "医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン" --short-title "CSVガイドライン" --doc-type guideline --source-url https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573 --source-format html --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_mhlw_csv_guideline_v1 --strict --overwrite-manifest
```

結果: bundle生成成功、qualitycheck warning なし。

```powershell
.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-134750168_feat-csv-guideline-parser-v1 --doc-id jp_mhlw_csv_guideline_20101021 --mode normal --out runs\20260525-134750168_feat-csv-guideline-parser-v1\goal_check.md
```

結果: `PASS`

```powershell
.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-134750168_feat-csv-guideline-parser-v1 --doc-id jp_mhlw_csv_guideline_20101021 --mode normal --out runs\20260525-134750168_feat-csv-guideline-parser-v1\special_structure_audit.md
```

結果: `pass`

```powershell
.venv\Scripts\python.exe -m pytest tests\test_text2ir_csv_guideline.py tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_goal_check.py tests\test_profile_loader_extends.py -q
```

結果: `21 passed`

## 実データ確認サンプル

- `document/root` -> `chapter cha1`（1 総則） -> `paragraph cha1.p1_3`（1.3 カテゴリ分類）
- `document/root` -> `chapter cha3`（3 コンピュータ化システムの開発、検証及び運用管理に関する文書の作成）
- `document/root` -> `chapter cha10`（10 用語集）

## 残課題

- `別紙1` はHTML上で画像参照、`別紙2` は表題行のみとして抽出されている。今回のParser開発では本文階層の安定化までを対象とし、別紙画像や別紙表の構造化は個別adapter検討時の材料として扱う。
- MHLW通知HTMLの前文構造は、現時点ではCSVガイドライン専用profileの処理に留めた。複数文書で同じ境界規則を確認できるまでは共通profileへ昇格しない。
