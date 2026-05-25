# RUN: 20260526-011550152_feat-table-record-review-6-7

## 目的

6/7の既存 `reconstructed_records` について、正式な `table_row` 昇格前のレビュー判断をIR内とRUN成果物に記録する。

このRUNはParser/adapter開発であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- 6 原薬GMPガイドライン 表1: `cha1.p1_3.tbl1`
- 7 無菌操作法指針 表1: `cha7.p7_1.tbl1`
- 7 無菌操作法指針 表2: `cha11.p11_3.tbl2`
- 7 無菌操作法指針 表3: `cha11.p11_3.tbl3`

## 実施内容

- 6/7の各tableに `record_review` を追加した。
- 各 `reconstructed_records` に `review_status: reviewed_candidate` と `promotion_status: deferred` を付けた。
- 正式 `table_row` 昇格は実施せず、既存のraw `table_row` とsource spanを維持した。
- `table_record_review_6_7` inventoryを追加し、表ごとの候補粒度、昇格判断、保留raw row、残課題を一覧化した。

## 判断

今回の候補粒度は `reconstructed_record` とする。

ただし、正式 `table_row` 昇格は延期する。

理由:

- 6 表1はPDFの灰色部分など、TXTから復元できない視覚情報が残る。
- 7 表1/表3は複数段ヘッダと注記参照の厳密対応が未確定。
- 7 表2は `C，D` の区域条件をrecord候補として束ねたが、DQ候補表示粒度の確認が必要。
- 既存raw `table_row` はsource span追跡と候補表示の安定性が高いため、置き換えずに保持する。

## 結果

詳細は `table_record_review_6_7.md` と `table_record_review_6_7.json` に記録した。

| 対象 | records | 候補粒度 | table_row昇格 | 主な残課題 |
| --- | ---: | --- | --- | --- |
| 6 表1 | 7 | reconstructed_record | deferred | PDF視覚情報 |
| 7 表1 | 4 | reconstructed_record | deferred | 複数段ヘッダ、注記参照 |
| 7 表2 | 4 | reconstructed_record | deferred | `C，D` 条件の候補粒度 |
| 7 表3 | 4 | reconstructed_record | deferred | 注記とセルの対応 |

## 正規化の度合い

- raw row保持: 維持。
- record候補: レビュー済み候補として明示。
- 正式table_row昇格: 未実施。
- DQ候補粒度: 表単位では `reconstructed_record` を候補とするが、正式採用はreadiness判定まで保留。

したがって、今回の成果は「6/7のrecord候補をレビュー判断付きで安定化する段階」であり、完全な表正規化ではない。

## 今回入れない課題

- `reconstructed_records` の正式 `table_row` node化。
- 6 表1のPDFレイアウト解析または画像確認。
- 7 表1/表3の注記とセルの厳密なリンク。
- DQチェックシートでraw rowとrecordのどちらを表示するかの最終決定。
- `data/normalized/` への昇格。

## 正規化完成までの残課題

6/7:

- record候補を正式 `table_row` 化するか、正規化RUN readinessで最終判断する。
- 6 表1のPDF視覚情報を扱う必要があるか決める。
- 7 表1/表3の注記参照をtable noteに留めるか、セル参照へ結び付けるか決める。

8:

- 計画Lの `feat/niid-annex-table-cell-reconstruction-v1` へ進む。

9:

- 計画N/Oの別紙2意味値分解と別紙1 OCR/転記方針へ進む。

全体:

- 計画Pで正規化RUN readinessを判定する。

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_table_record_review_6_7.py tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_goal_check.py tests\test_special_structure_audit.py -q
```

結果: `24 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.table_record_review_6_7 --out-json runs\20260526-011550152_feat-table-record-review-6-7\table_record_review_6_7.json --out-md runs\20260526-011550152_feat-table-record-review-6-7\table_record_review_6_7.md
```

結果: inventory生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\pmda\api_gmp_guideline\source_texts\000156438.txt --out-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_api_gmp_guideline_record_review_v1 --title "原薬GMPのガイドライン" --short-title "原薬GMPガイドライン" --doc-type guideline --source-url https://www.pmda.go.jp/files/000156438.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_pmda_api_gmp_guideline_v1 --candidate-visibility-profile-id jp_pmda_api_gmp_guideline_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\pmda\aseptic_processing_guideline\source_texts\000206144.txt --out-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_aseptic_processing_guideline_record_review_v1 --title "無菌操作法による無菌医薬品の製造に関する指針" --short-title "無菌操作法指針" --doc-type guideline --source-url https://www.pmda.go.jp/files/000206144.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_pmda_aseptic_processing_guideline_v1 --candidate-visibility-profile-id jp_pmda_aseptic_processing_guideline_visibility_v1 --strict --overwrite-manifest
```

結果: bundle生成成功。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_api_gmp_guideline_record_review_v1 --mode normal --out runs\20260526-011550152_feat-table-record-review-6-7\goal_check_api_gmp.md
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_aseptic_processing_guideline_record_review_v1 --mode normal --out runs\20260526-011550152_feat-table-record-review-6-7\goal_check_aseptic.md
```

結果: どちらも `PASS`。

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_api_gmp_guideline_record_review_v1 --mode normal --out runs\20260526-011550152_feat-table-record-review-6-7\special_structure_audit_api_gmp.md
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260526-011550152_feat-table-record-review-6-7 --doc-id jp_pmda_aseptic_processing_guideline_record_review_v1 --mode normal --out runs\20260526-011550152_feat-table-record-review-6-7\special_structure_audit_aseptic.md
```

結果: どちらも `pass`。
