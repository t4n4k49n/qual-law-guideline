# RUN: 20260526-005646660_docs-remaining-normalization-plan-6-9

## 目的

6/7/8/9の個別adapter計画F-Iが完了したため、各RUNに残した課題をおさらいし、正規化完成までの次期開発計画として整理する。

このRUNはドキュメント整備であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- `docs/INDIVIDUAL_ADAPTER_NEXT_PHASE_PLAN.md`
- `docs/INDIVIDUAL_ADAPTER_COLUMN_RESTORATION_PLAN.md`
- `runs/20260525-225501792_feat-raw-line-table-column-restore-prototype/RUN.md`
- `runs/20260525-231917460_feat-niid-annex-table-inventory/RUN.md`
- `runs/20260525-233654758_feat-niid-annex-table-adapters-v1/RUN.md`
- `runs/20260525-235003289_feat-mhlw-csv-annex-source-recovery/RUN.md`
- `runs/20260526-002546060_feat-mhlw-csv-annex2-table-parser/RUN.md`

## 実施内容

- `docs/REMAINING_NORMALIZATION_PLAN_6_9.md` を追加した。
- 計画済みだったF-Iの完了状況を整理した。
- RUNに記録された未達事項を、次期開発K-Pとして分割した。
- 通常開発PRと正規化RUNを分ける方針を改めて明記した。
- 次の推奨PRを `feat/table-record-review-6-7` とした。

## おさらい

計画済みだった範囲:

| フェーズ | 対象 | 状態 |
| --- | --- | --- |
| F | 6/7/8/9 棚卸し | 完了 |
| G | 6/7 raw_line table列復元プロトタイプ | 完了 |
| H | 8 NIID 別表・付表分類とtable node化 | 完了 |
| I | 9 CSV 別紙ソース補完 | 完了 |
| 追加 | 9 CSV 別紙2 page2 HTML table adapter | 完了 |

残る主な課題:

- 6/7: `reconstructed_records` の確定、正式 `table_row` 化判断、注記・複数段ヘッダ・PDF視覚情報の扱い。
- 8: table化済み5表のセル復元、複雑表の手動レビュー、番号/節構造化判断。
- 9: 別紙2の意味値分解・脚注分解・record統合、別紙1のOCR/転記方針。
- 全体: 正規化RUN readiness判定と、親PR/子PRによる `data/normalized/` 昇格。

## 次期計画

| フェーズ | ブランチ案 | 内容 |
| --- | --- | --- |
| K | `feat/table-record-review-6-7` | 6/7のrecord確定レビュー |
| L | `feat/niid-annex-table-cell-reconstruction-v1` | 8のtable化済み5表のセル復元 |
| M | `docs/niid-complex-annex-structure-plan` | 8の複雑表・節/番号構造レビュー |
| N | `feat/mhlw-csv-annex2-semantic-records` | 9別紙2の意味値分解 |
| O | `docs/mhlw-csv-annex1-ocr-plan` | 9別紙1のOCR/転記方針 |
| P | `docs/normalized-run-readiness-6-9` | 正規化RUN readiness判定 |

## 今回入れない課題

- コード実装。
- 既存adapterの挙動変更。
- `data/normalized/` への昇格。
- 正規化RUNの親PR/子PR作成。

## 検証

```powershell
git diff --check
```

結果: 問題なし。

```powershell
rg -n "<local-path-pattern>" docs/REMAINING_NORMALIZATION_PLAN_6_9.md runs/20260526-005646660_docs-remaining-normalization-plan-6-9
```

結果: 該当なし。
