# RUN: 20260526-100829653_feat-niid-visual-table-review-v1

## 目的

8「病原体等安全管理規程」のNIID付表・別表について、PDFページ画像を根拠にした視覚レビュー復元を開始する。

このRUNはParser/adapter開発後の視覚レビュー復元であり、正式な正規化RUNではない。`data/normalized/` への昇格は行わない。

## 対象

- source PDF: `data/human-readable/niid/pathogen_safety_management/Kanrikitei3_20240401.pdf`
- 対象ページ:
  - PDF page 24: `付表2`
  - PDF page 25: `付表3`
  - PDF page 26: `付表4`
  - PDF page 34: `別表7`
  - PDF page 37: `別表10`

## 実施内容

- 対象PDFページをPNG画像として `source_pages/` に保存した。
- `付表3` を視覚レビューで復元し、BSL結合ヘッダ、`換気`、`オートクレーブ` の親子関係を記録した。
- `付表4` を視覚レビューで復元し、ABSLごとの複数行セルを1 recordに統合した。
- 復元結果を `visual_reconstruction.json` と `visual_reconstruction.md` に記録した。

## 成果

| annex | PDF page | status | records |
| --- | ---: | --- | ---: |
| 付表2 | 24 | source image preserved |  |
| 付表3 | 25 | visual reconstructed | 15 |
| 付表4 | 26 | visual reconstructed | 4 |
| 別表7 | 34 | source image preserved |  |
| 別表10 | 37 | source image preserved |  |

## 判断

- `付表3` はPDFテキストレイヤーでは `換気` と `オートクレーブ` の親項目を安全に復元できないため、画像上の罫線と字下げを根拠に親子関係を付けた。
- `付表4` はテキスト改行ではなく罫線で区切られた行高がrecord境界であり、各ABSL行を1 recordとして扱う。
- `付表2`, `別表7`, `別表10` は画像を同梱し、次PRで同じ方式により復元する。

## 検証

ドキュメント・画像成果物のみの変更。コード・テストは変更していない。
