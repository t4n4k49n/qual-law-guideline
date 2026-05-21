# TABLE_NOTE_DESCENDANT_REVIEW

## 結論

表・注記・子孫表示の仕組みは、コードとfixtureテスト上は実装済み。ただし今回の代表9文書の再生成では `table`, `table_row`, `note`, `preformatted` がすべて0件だったため、代表文書の正式化判断としては「実データ到達確認未了」とする。

## 重点確認

| 確認項目 | 現状 | 判定 | 必要対応 |
|---|---|---|---|
| 1. 表のレコードを選択可能なアイテムとして扱えるか | `selectable_kinds` に `table_row` が含まれる。fixtureではtable_row候補化を確認 | 実装済み、代表文書では未確認 | 表を含む実入力で再生成確認 |
| 2. 表タイトル・表ヘッダを親・先祖相当として表示できるか | `table -> table_header -> table_row` 構造と `context_display_policy` がある | 実装済み、代表文書では未確認 | table fixture相当の実データサンプルを追加 |
| 3. 表下注記・通常注記を子・子孫相当として表示できるか | `include_descendants*` とnote fixtureがある | 実装済み、代表文書では未確認 | 実文書の注記をnote化できる入力/profile確認 |
| 4. 条文系ノードでも後続子孫をprofileで表示対象にできるか | subitem/item/paragraph/statement向けに `include_descendants` 設定あり | 実装済み | 代表文書でnoteが発生するケースを作って確認 |
| 5. `regdoc_profile` だけで制御できるか | 表示制御はprofileで可能。ノード生成は入力形状とparser/profileに依存 | 一部可能 | ノード生成はprofileまたは前処理、表示制御はregdoc_profileで分担 |

## 判断

- 表示制御のために今すぐ大きなtext2ir共通更改へ入る必要は薄い。
- ただし「実データに表・注記がない」のか「入力テキスト化で失われた」のかは未確認であり、正式化前にサンプル確認が必要。
- 複雑表やPDF崩れ表は共通parserへ押し込まず、Markdown化前処理または拡張部品候補として扱う。
