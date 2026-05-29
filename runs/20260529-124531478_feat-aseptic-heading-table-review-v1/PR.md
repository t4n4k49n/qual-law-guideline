# 無菌操作法指針 heading/table 目検修正

## まとめ

無菌操作法指針の正規化前レビューとして、heading階層と表1/2/3の結合セルを修正しました。表はraw行ではなく、PDF目検に基づくデータ行として扱えるようになり、見出し階層も `7.1 -> 7.1.1` のように文脈を保持できる状態になります。

## 背景

前段のadapterでは、無菌操作法指針の表1/2/3をtable nodeとして保持できていましたが、正式な正規化RUNへ進めるには不足がありました。

- 表1/2/3がraw row中心で、結合ヘッダと複数行セルの復元はmetadata止まり。
- `7.1` と `7.1.1` のような親子headingがchapter直下の兄弟になっていた。
- 表1がsource上の位置より後ろにappendされ、親section側に表注記が重複していた。

## 変更内容

- `x.y` headingを原則 `section`、`x.y.z` をchild `paragraph` として扱うように調整。
- Chapter 2の用語定義 `2.1` から `2.52` はglossary-style definitionとして `paragraph` のまま維持。
- 表1/2/3をPDF目検済みの復元行として `table_row` に昇格。
- 結合ヘッダを `header_structure.spanning_headers` に保持。
- 表1を `7.1` 配下のsource順に配置し、`7.1.1` より前に出力。
- 表1の重複親noteを除去し、table noteとして保持。

## 確認

- GOAL check: pass
- Special structure audit: pass
- Generated table rows: `12`
- Unresolved special blocks: `0`
- Focused tests: `7 passed`
- Full tests: `253 passed, 1 skipped`

## 注意

このPRは正規化RUNではありません。無菌操作法指針のheading/table目検修正です。

このPR承認・マージ後に、改めて正規化RUNをfreshに作成します。

<!-- PR_BODY_FILE: runs/20260529-124531478_feat-aseptic-heading-table-review-v1/PR.md -->
