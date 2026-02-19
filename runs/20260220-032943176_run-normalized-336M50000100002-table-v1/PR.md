# 正規化RUN PR: 20260220-032943176_run-normalized-336M50000100002-table-v1

## 目的
- e-Gov XML `336M50000100002_20260501_507M60000100117.xml` を現行main（表対応入り parser）で再正規化し、4ファイル出力を検証する。

## 対象法令URL
- https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117

## 変更内容
- `runs/20260220-032943176_run-normalized-336M50000100002-table-v1/RUN.md` を追加
- `out/20260220-032943176_run-normalized-336M50000100002-table-v1/manifest.yaml` を追加
- `out/20260220-032943176_run-normalized-336M50000100002-table-v1/` に4ファイルを生成

## 検証結果
- `verify_document`: passed
- `regdoc_ir` に `table/table_header/table_row` が生成されることを確認
- `regdoc_profile` に `table_row` selectable と `include_descendants_kinds: [note]` を確認

## 比較表（人間レビュー用）
| 区分 | 内容 |
|---|---|
| 人間可読（祖先含む） | 別表 > （table heading: 別表） > ヘッダ: 標識 \| 大きさ \| 標識を付ける箇所 > 行: 産業標準化法... |
| YAML断片（対象NID） | `appdx_table1.tbl1.tblh.tblr1` |

## 備考
- PR本文とRUN文書では個人環境の絶対パスを避け、`%USERPROFILE%` 表記を使用。
- `data/normalized/` への昇格は承認後に実施し、このPR本文には記載しない。

## まとめ
- 表対応後のパーサで対象法令を再正規化し、表行ノードと文脈表示設定が出力に反映されることを確認した。これによりチェックシート利用時に表レコードを条文同様に選択・文脈表示できる前提が整う。
