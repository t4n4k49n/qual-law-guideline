# NORMALIZED RUN OUTPUT 4FILES GUIDE

## 4ファイル
- `<doc_id>.regdoc_ir.yaml`
- `<doc_id>.parser_profile.yaml`
- `<doc_id>.regdoc_profile.yaml`
- `<doc_id>.meta.yaml`

## regdoc_profile の主要設定
`dq_gmp_checklist` では、左候補（表示/選択）と右表示文脈を分離して扱う。

### 候補表示・選択
- `candidate_visibility`: 左候補一覧に出す/出さないを制御
  - `allow_rules` (`list[dict]`): 1件以上ある場合は一致ノードのみ表示（OR）
  - `deny_rules` (`list[dict]`): 一致ノードを非表示（`deny` 優先）
- `selectable_kinds`: 左候補一覧でチェック可能な kind を制御

### 表示文脈
- `grouping_policy`
- `context_display_policy`

### 既存主要キー
- `when_kind`
- `include_ancestors_until_kind`
- `include_headings`
- `include_chapeau_text`

### 追加キー（後方互換の拡張）
- `include_descendants` (`bool`)
- `include_descendants_of` (`selected` | `ancestors` | `both`)
- `include_descendants_kinds` (`list[str] | null`)
- `include_descendants_max_depth` (`int`)

## 表（Markdown table）での利用例
`table_row` 選択時に、祖先として table title/header、子孫として note を表示する設定例:

```yaml
profiles:
  dq_gmp_checklist:
    candidate_visibility:
      allow_rules: []
      deny_rules: []
    selectable_kinds: [subitem, item, paragraph, statement, table_row]
    grouping_policy:
      - when_kind: table_row
        group_under_kind: table
    context_display_policy:
      - when_kind: table_row
        include_ancestors_until_kind: chapter
        include_headings: true
        include_chapeau_text: true
        include_descendants: true
        include_descendants_of: ancestors
        include_descendants_kinds: [note]
        include_descendants_max_depth: 3
```

## 条文/本文ノードでの注書き表示例
`subitem` や `paragraph` の子に `note` がある場合、選択時に同時表示できる。

```yaml
profiles:
  dq_gmp_checklist:
    candidate_visibility:
      allow_rules: []
      deny_rules:
        - kind: annex
        - under_kind: annex
    context_display_policy:
      - when_kind: subitem
        include_ancestors_until_kind: chapter
        include_headings: true
        include_chapeau_text: true
        include_descendants: true
        include_descendants_of: selected
        include_descendants_kinds: [note]
        include_descendants_max_depth: 2
```
