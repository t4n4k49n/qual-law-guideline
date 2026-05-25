# RUN: 20260525-224254581_docs-individual-adapter-column-plan

## 目的

6/7/8/9 個別adapter開発で積み残した列復元、意味正規化、ソース補完の対象を棚卸しし、次に着手する順序を固定する。

これは開発計画RUNであり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- 6 原薬GMPガイドライン 表1
- 7 無菌操作法指針 表1/表2/表3
- 8 病原体等安全管理規程 別表・付表
- 9 CSVガイドライン 別紙1/別紙2

## 実施内容

- `docs/INDIVIDUAL_ADAPTER_COLUMN_RESTORATION_PLAN.md` を追加した。
- 既存RUNを確認し、積み残しを以下に分類した。
  - 6/7: raw_line tableから列復元プロトタイプへ進める。
  - 8: 先に別表・付表の表別分類を行う。
  - 9: 先に別紙ソース補完/OCR判断を行う。
- 次PRは `feat/raw-line-table-column-restore-prototype` とし、6/7のraw_line tableだけを対象にする方針とした。

## 判断

| 対象 | 判断 | 理由 |
| --- | --- | --- |
| 6 表1 | 次PRで列復元プロトタイプへ進める | table node化済みで、source spanと親NIDが安定している |
| 7 表1/2/3 | 次PRで列復元プロトタイプへ進める | table node化済みで、対象表が3件に限定されている |
| 8 別表・付表 | まず表別分類 | 形式混在が強く、いきなり列復元すると個別最適が混ざりやすい |
| 9 別紙1/2 | まずソース補完 | 別紙1は画像、別紙2は表本体ソース未確定のため、列復元の入力がない |

## この開発に入れない課題

- 6/7の実際の列復元実装。
- 8の表別adapter実装。
- 9の画像取得、OCR、代替ソース取得。
- `data/normalized/` への昇格。

これらは今回の棚卸しを超えるため、次PR以降に分ける。

## 検証

文書追加のみのため、pytestは実行していない。

確認:

```text
git diff --check
```

結果: 問題なし。

## 次のPR

ブランチ案:

- `feat/raw-line-table-column-restore-prototype`

対象:

- 6 原薬GMPガイドライン 表1
- 7 無菌操作法指針 表1/表2/表3

完了条件:

- 表ごとの列名候補、復元成功行、fallback行がテストで固定される。
- `raw_line` は失わず、復元できない行はwarning付きで残る。
