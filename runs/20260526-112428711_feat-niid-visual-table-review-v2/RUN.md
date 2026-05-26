# RUN: 20260526-112428711_feat-niid-visual-table-review-v2

## 目的

8「病原体等安全管理規程」のNIID付表・別表について、v1でsource imageとして残した `付表2`, `別表7`, `別表10` を視覚レビューで復元する。

このRUNはParser/adapter開発後の視覚レビュー復元であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- source PDF: `data/human-readable/niid/pathogen_safety_management/Kanrikitei3_20240401.pdf`
- 対象ページ:
  - PDF page 24: `付表2`
  - PDF page 34: `別表7`
  - PDF page 37: `別表10`

## 実施内容

- 対象PDFページのPNG画像を `source_pages/` に同梱した。
- `付表2` を視覚レビューで復元し、リスク群1から4までの4 recordに整理した。
- `別表7` を視覚レビューで復元し、左端カテゴリの結合セルを `category` として保持しながら18 recordに整理した。
- `別表10` を視覚レビューで復元し、左端カテゴリの結合セルを `category` として保持しながら13 recordに整理した。
- 復元結果を `visual_reconstruction.json` と `visual_reconstruction.md` に記録した。

## 成果

| annex | PDF page | status | records |
| --- | ---: | --- | ---: |
| 付表2 | 24 | visual reconstructed | 4 |
| 別表7 | 34 | visual reconstructed | 18 |
| 別表10 | 37 | visual reconstructed | 13 |

## 判断

- `付表2` は複数行に折り返されたセルを、罫線で区切られた1行=1 recordとして統合した。
- `別表7` は左端の `病原体等`, `ヒト`, `施設`, `教育` を結合カテゴリとして扱い、各recordへ展開した。
- `別表10` は左端カテゴリのrowspanをrecordへ展開し、右端の該当条項はセル内列挙として保持した。
- v1/v2の視覚レビューにより、視覚処理対象として残していた `付表2`, `付表3`, `付表4`, `別表7`, `別表10` は一通り表record化した。

## 残課題

- このRUNはレビュー成果であり、正式版昇格は未実施。
- 次に正規化RUNへ進む場合は、v1/v2の `visual_reconstruction.json` を昇格候補の入力として扱い、既存parser/adapter出力との突合を行う。

## 検証

- `visual_reconstruction.json` のJSON妥当性を確認する。
- ドキュメント・画像成果物のみの変更。コード・テストは変更しない。
