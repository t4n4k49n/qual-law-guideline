# RUN: 20260525-225501792_feat-raw-line-table-column-restore-prototype

## 目的

6/7の既存 `raw_line` tableについて、列復元・意味正規化のプロトタイプを追加する。

これはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- 6 原薬GMPガイドライン 表1
  - 既存table: `cha1.p1_3.tbl1`
  - raw rows: 26
- 7 無菌操作法指針 表1/表2/表3
  - 既存table: `cha7.p7_1.tbl1`
  - 既存table: `cha11.p11_3.tbl2`
  - 既存table: `cha11.p11_3.tbl3`
  - raw rows: 14 / 9 / 7

## 実装

- `api_gmp_table1_adapter` に列復元プロトタイプを追加した。
- `aseptic_processing_table_adapter` に列復元プロトタイプを追加した。
- 既存の `raw_line`、`cells: [raw_line]`、source spanは残した。
- table nodeに以下を追加した。
  - `column_reconstruction: prototype`
  - `column_reconstruction_status: partial`
  - `reconstructed_columns`
  - `reconstructed_records`
  - `non_data_raw_rows`
- table_row nodeには、復元recordへ属する行だけ `column_reconstruction_record_id` を付けた。
- header行、注記的行、視覚情報行など、セル復元対象にしない行には `column_reconstruction_warning` を付けた。

## 判断

今回の実装は、行ごとの `cells` を直接置き換えない。

理由:

- 既存の `table_row` はDQ候補やsource span追跡に使えるため、raw rowとしての安定性を優先する。
- 6表1、7表1は複数行セルや視覚情報があり、row単位の `cells` へ直接上書きすると誤った意味付けを固定する。
- 復元済みの意味単位は、table単位の `reconstructed_records` としてレビュー可能にする。

## 結果

| 対象 | 復元records | 非データ/警告行 | 状態 |
| --- | ---: | ---: | --- |
| 6 表1 | 7 | 3 | partial |
| 7 表1 | 4 | 7 | partial |
| 7 表2 | 4 | 3 | partial |
| 7 表3 | 4 | 3 | partial |

## 正規化度

このRUNで、6/7の主要表は `raw_line` 保持から「セル候補付きtable」へ進んだ。

達成済み:

- 表単位に列名候補を持つ。
- 複数raw rowを1つの意味recordへ束ねられる。
- 復元できない行をwarning付きで残せる。
- raw rowとsource spanを失わない。

未達:

- `reconstructed_records` を正式な `table_row` nodeへ昇格する判断。
- 6表1の灰色部分など、PDF視覚情報の復元。
- 7表1/表3の注記とセルの厳密な対応付け。
- 複数段ヘッダの標準表現化。
- DQチェックシートで、raw rowとreconstructed recordのどちらを候補粒度にするかの最終判断。

したがって、この出力は「完全な表正規化」ではなく、「レビュー可能な列復元候補をIR内に持つ段階」とする。

## 正規化完成までの残課題

6 原薬GMPガイドライン:

- 表1の `reconstructed_records` の列名・セル内容をレビューで確定する。
- 灰色部分の視覚情報を扱うか判断する。TXTだけでは復元不能なため、必要ならPDFレイアウト解析または画像確認が必要。
- `ＧＭＰ要求事項の増大` を表の注記/方向指示としてどう表すか決める。

7 無菌操作法指針:

- 表1の複数段ヘッダと注1/注2のセル対応を確定する。
- 表2の `C，D` にまたがる区域条件の候補表示粒度を決める。
- 表3の注1/注2を、表全体注記に留めるかセル参照へ結び付けるか決める。

8 病原体等安全管理規程:

- 別表・付表ごとの形式分類が未実施。
- 列復元対象と原文保持対象を分ける必要がある。
- 8は次段階で `feat/niid-annex-table-inventory` を先に行う。

9 CSVガイドライン:

- `別紙1` の画像取得/OCR判断が未実施。
- `別紙2` の表本体ソース確認が未実施。
- 9は列復元以前に `feat/mhlw-csv-annex-source-recovery` が必要。

全体:

- 正式な正規化RUNへ進む前に、6/7の列復元候補をレビューし、8/9の保留理由を確定する必要がある。
- `data/normalized/` への昇格は未実施。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_goal_check.py tests\test_special_structure_audit.py -q
```

結果: `23 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\pmda\api_gmp_guideline\source_texts\000156438.txt --out-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_api_gmp_guideline_column_restore_v2 --title "原薬GMPのガイドライン" --short-title "原薬GMPガイドライン" --doc-type guideline --source-url https://www.pmda.go.jp/files/000156438.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_pmda_api_gmp_guideline_v1 --candidate-visibility-profile-id jp_pmda_api_gmp_guideline_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\pmda\aseptic_processing_guideline\source_texts\000206144.txt --out-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_aseptic_processing_guideline_column_restore_v2 --title "無菌操作法による無菌医薬品の製造に関する指針" --short-title "無菌操作法指針" --doc-type guideline --source-url https://www.pmda.go.jp/files/000206144.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_pmda_aseptic_processing_guideline_v1 --candidate-visibility-profile-id jp_pmda_aseptic_processing_guideline_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_api_gmp_guideline_column_restore_v2 --mode normal --out runs\20260525-225501792_feat-raw-line-table-column-restore-prototype\goal_check_api_gmp.md
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_aseptic_processing_guideline_column_restore_v2 --mode normal --out runs\20260525-225501792_feat-raw-line-table-column-restore-prototype\goal_check_aseptic.md
```

結果: どちらも `PASS`、Warningsなし。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_api_gmp_guideline_column_restore_v2 --mode normal --out runs\20260525-225501792_feat-raw-line-table-column-restore-prototype\special_structure_audit_api_gmp.md
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-225501792_feat-raw-line-table-column-restore-prototype --doc-id jp_pmda_aseptic_processing_guideline_column_restore_v2 --mode normal --out runs\20260525-225501792_feat-raw-line-table-column-restore-prototype\special_structure_audit_aseptic.md
```

結果: どちらも `pass`。

## 次のPR

計画どおり、次は8の別表・付表を表別に分類する。

ブランチ案:

- `feat/niid-annex-table-inventory`
