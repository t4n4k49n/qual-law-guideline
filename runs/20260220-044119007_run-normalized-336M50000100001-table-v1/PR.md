# 正規化RUN PR: 20260220-044119007_run-normalized-336M50000100001-table-v1

## 目的
- e-Gov XML 336M50000100001_20260501_507M60000100117.xml を現行main（表対応入り parser）で再正規化し、4ファイル出力を検証する。

## 対象法令URL
- https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117

## 変更内容
- uns/20260220-044119007_run-normalized-336M50000100001-table-v1/RUN.md を追加
- out/20260220-044119007_run-normalized-336M50000100001-table-v1/manifest.yaml を追加
- out/20260220-044119007_run-normalized-336M50000100001-table-v1/ に4ファイルを生成

## 検証結果
- erify_document: passed
- egdoc_ir に 	able/table_header/table_row が生成されることを確認（26/26/681）
- egdoc_profile の dq_gmp_checklist で 	able_row selectable・group_under_kind: table・include_descendants_kinds: [note] を確認

## 比較表（人間レビュー用）
| 区分 | 内容 |
|---|---|
| 選択ノード | 	able_row |
| 対象NID | rt37.p2.tbl1.tblh.tblr1 |
| 祖先（人間可読） | 第二章 > 第三十七条 > 第二項 > 	able > 	able_header |
| ヘッダ本文 | 第二十七条 / 医薬品、医薬部外品又は化粧品の製造業の許可証 / 医薬品等外国製造業者の認定証 |
| 行本文（要約） | 様式第十三 / 様式第十九 |
| YAML構造確認 | chapter -> article -> paragraph -> table -> table_header -> table_row |

## 備考
- PR本文とRUN文書では個人環境の絶対パスを避け、%USERPROFILE% 表記を使用。
- data/normalized/ への昇格は承認後に実施し、このPR本文には記載しない。

## まとめ
- 表対応後のパーサで対象法令を再正規化し、表行ノードと文脈表示設定が出力に反映されることを確認した。これによりチェックシート利用時に表レコードを条文同様に選択・文脈表示できる前提が整う。
