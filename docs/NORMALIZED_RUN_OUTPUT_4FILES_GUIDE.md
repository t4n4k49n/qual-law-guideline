# NORMALIZED RUN OUTPUT 4FILES GUIDE

## 4ファイル
- `<doc_id>.regdoc_ir.yaml`
- `<doc_id>.parser_profile.yaml`
- `<doc_id>.regdoc_profile.yaml`
- `<doc_id>.meta.yaml`

## regdoc_profile の context_display_policy
`context_display_policy` は選択ノードの表示文脈を宣言する。

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
