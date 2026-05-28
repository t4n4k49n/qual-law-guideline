# PIC/S Part I 表・Warning事前確認

## まとめ

PIC/S Part Iの正規化RUN前に、表・Warning・Note周りを点検しました。本文中に構造化すべきTable/Figureは見つからず、正規化候補化の主なリスクだったChapter 7冒頭Noteの誤帰属を修正しています。これにより、次の正規化RUNでPart Iを正式候補としてレビューしやすい状態になります。

## 変更内容

- Part I profileで、ページ上部の混在ケースrunning headerを除去。
- Note抽出時に、前章の古いparagraphへ誤ってNoteをぶら下げないよう修正。
- Chapter 7冒頭Noteの帰属を検証するregression testを追加。
- 事前確認RUNの記録とサンプルを追加。

## 確認結果

| 確認 | 結果 |
|---|---|
| strict bundle generation | pass |
| promotion goal check | pass |
| promotion goal warnings | none |
| special structure audit | pass |
| source tables | 0 |
| source figures | 0 |
| generated tables | 0 |
| generated rows | 0 |
| generated figures | 0 |
| unresolved special blocks | 0 |
| IR warning metadata scan | none |
| focused tests | `9 passed` |
| full test suite | `251 passed, 1 skipped` |

## 修正した問題

修正前は、Chapter 7直前のrunning header `Chapter 7     Outsourced activities` が `cha6.p6_41.text` に混入し、Chapter 7冒頭のNoteが `cha6.p6_41.not1` として前章のparagraphに誤帰属していました。

修正後は、`cha6.p6_41` からrunning headerが消え、当該Noteは `cha7.not1` としてChapter 7配下に配置されます。

## レビュー資料

- `runs/20260529-033231419_feat-pics-part1-table-warning-review-v1/RUN.md`
- `runs/20260529-033231419_feat-pics-part1-table-warning-review-v1/TABLE_WARNING_REVIEW.md`
- `runs/20260529-033231419_feat-pics-part1-table-warning-review-v1/SAMPLE_EXTRACT.md`

<!-- PR_BODY_FILE: runs/20260529-033231419_feat-pics-part1-table-warning-review-v1/PR.md -->
