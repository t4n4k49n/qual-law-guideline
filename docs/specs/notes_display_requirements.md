# 本文注書き表示要件

## 目的
- 表（table_row）向けに導入した子孫表示の仕組みを、通常の条文/本文にも適用する。
- 本文中の `Note/注記/備考/脚注` を `note` ノード化し、選択ノードと同時表示できるようにする。

## 最小仕様
- 注書き開始行（例）
  - `^(?i)(Note|Notes|NB)\b[:：]?\s+`
  - `^(注|注記|備考|※)\s*[:：]?\s+`
  - `^（注）\s*`
- 注書きブロック終端
  - 空行
  - 次の構造マーカー行
- 注書きノード
  - kind: `note`
  - ぶら下げ先: 直前の選択候補ノード（`subitem/item/paragraph/statement/table_row`）

## 表示設定
- `regdoc_profile.context_display_policy` の `include_descendants*` で `note` を対象に含める。
- これにより、選択ノードの祖先表示とあわせて注書き表示を制御できる。
