# mock-ui課題の具体例

このメモは、`local_notes/TODO.md` に残っているmock-ui関連課題が、実際にはどの表示・設定・IR構造を指しているかを具体化するためのもの。

対象課題:

| ID | 課題 | 一言でいうと |
| --- | --- | --- |
| A | 表示例4のtable系デモ更新 | 「表2行」と言っているが、現行設定は1行しか選んでいない。更新後は1行目＋3行目の非連続選択にする |
| B | 「別表」見出しの連続表示 | `annex` と `table` の両方が似た見出しを持ち、UIで重複して見える |
| C | 表示プロファイルYAML化 | どの祖先・子孫・見出しを出すかのルールが、まだ運用できる形で固まっていない |

---

## A. 表示例4のtable系デモ更新

### 現在の設定

`data/mock_ui/display_examples.yaml` の表示例4は、タイトル上は2行デモを意図している。

```yaml
- id: "example4"
  display_name: "表示例4"
  display_title: "表2行（更新せなあかん）"
  law_folder: "jp_egov_336M50000100002_20260501_507M60000100117"
  selection_nids:
    - "appdx_table1.tbl1.tblh.tblr1"
```

ただし、`selection_nids` は1件だけ。

### 参照先IRの実体

対象NIDは正式IRに存在する。

```yaml
nid: appdx_table1
kind: appendix
num: 別表
text: 別表 標識 大きさ 標識を付ける箇所 ...
children:
  - nid: appdx_table1.tbl1
    kind: table
    heading: 別表
    children:
      - nid: appdx_table1.tbl1.tblh
        kind: table_header
        text: 標識 | 大きさ | 標識を付ける箇所
        children:
          - nid: appdx_table1.tbl1.tblh.tblr1
            kind: table_row
            text: 産業標準化法... | 放射能標識は、半径一〇センチメートル以上... | 貯蔵室の出入口又はその附近
```

この表は1行だけなので、現行の `law_folder` のままでは「2行選択デモ」にならない。

### UIで見せたいこと

2行デモで確認したいのは、次の挙動。

| 観点 | 見たい状態 |
| --- | --- |
| 表ヘッダ | 2行をまとめて1つの表ヘッダの下に出す |
| 祖先表示 | 共通の章/節/表見出しを何度も繰り返さない |
| 選択行 | 選択した2行だけがチェックシート側に出る。連続行ではなく、間の行が飛ばされることも見える |
| Markdown表 | 2行が同じ表としてレンダリングされる |

### 2行デモに向く実データ候補

候補: `jp_pmda_api_gmp_guideline_20011102`

```yaml
law_folder: "jp_pmda_api_gmp_guideline_20011102"
selection_nids:
  - "cha1.sec1_3.tbl1.tblh.tblr1"
  - "cha1.sec1_3.tbl1.tblh.tblr3"
```

この表は「表１：原薬生産に対する本ガイドラインの適用」。1行目と3行目を選ぶことで、2行目が選ばれていないことが人間にも分かりやすい。

| NID | 行の内容 |
| --- | --- |
| `cha1.sec1_3.tbl1.tblh.tblr1` | 化学的合成による原薬 / 原薬出発物質の製造 / 原薬出発物質の工程への導入 / 中間体の製造 / 分離及び精製 / 物理的加工処理及び包装 |
| `cha1.sec1_3.tbl1.tblh.tblr2` | 動物由来の原薬 / ... / 選ばない行 |
| `cha1.sec1_3.tbl1.tblh.tblr3` | 植物から抽出する原薬 / 植物の収集 / 細断及び初期抽出 / 原薬出発物質の工程への導入 / 分離及び精製 / 物理的加工処理及び包装 |

期待表示イメージ:

```markdown
### 表１：原薬生産に対する本ガイドラインの適用

| 生産形態 | STEP 1 | STEP 2 | STEP 3 | STEP 4 | STEP 5 |
| --- | --- | --- | --- | --- | --- |
| 化学的合成による原薬 | 原薬出発物質の製造 | 原薬出発物質の工程への導入 | 中間体の製造 | 分離及び精製 | 物理的加工処理及び包装 |
| 植物から抽出する原薬 | 植物の収集 | 細断及び初期抽出 | 原薬出発物質の工程への導入 | 分離及び精製 | 物理的加工処理及び包装 |
```

ここで「動物由来の原薬」の行が出ないことが重要。連続した1行目・2行目を選ぶより、「選んだものだけが出る」感覚を確認しやすい。

---

## B. 「別表」見出しが連続する表示

### 問題の構造

e-Govの別表では、祖先に `appendix` と `table` が並び、両方が似た見出しになることがある。

```text
document
└─ appendix: num=別表
   └─ table: heading=別表
      └─ table_header: 標識 | 大きさ | 標識を付ける箇所
         └─ table_row: ...
```

このまま祖先を全部表示すると、UI上では次のように見えやすい。

```markdown
別表
別表
標識 | 大きさ | 標識を付ける箇所
産業標準化法... | 放射能標識は... | 貯蔵室の出入口又はその附近
```

これが「別表の嵐」。

### 望ましい見え方

同じ意味の見出しは1回にまとめる。

```markdown
### 別表

| 標識 | 大きさ | 標識を付ける箇所 |
| --- | --- | --- |
| 産業標準化法... | 放射能標識は、半径一〇センチメートル以上... | 貯蔵室の出入口又はその附近 |
```

### 判断ルールの例

| 条件 | 表示 |
| --- | --- |
| `appendix.num` と `table.heading` が同じ | 片方だけ表示 |
| `appendix.heading` があり、`table.heading` も同じ | 片方だけ表示 |
| `table.heading` が具体的な表題で、`appendix.num` は「別表7」など番号のみ | 両方出してよい |
| `table_header.text` がある | 見出し本文としてではなく表ヘッダとして表示 |

---

## C. 表示プロファイルYAML化

### いま存在する設定

`data/mock_ui/profiles/example2_candidate_visibility_default.yaml` には、すでに出し分けルールの原型がある。

```yaml
selectable_kinds:
  - subitem
  - item
  - paragraph
  - statement
  - table_row

grouping_policy:
  - when_kind: table_row
    group_under_kind: table

context_display_policy:
  - when_kind: table_row
    include_ancestors_until_kind: article
    include_headings: true
    include_chapeau_text: true
    include_descendants: true
    include_descendants_of: ancestors
    include_descendants_kinds:
      - note
    include_descendants_max_depth: 3

render_templates: {}
```

ただし、次の点がまだ弱い。

| 弱い点 | 具体例 |
| --- | --- |
| 表示テンプレートが空 | `render_templates: {}` のままなので、別表/table/table_headerの重複抑制を宣言できない |
| 表示例3/4にprofileがない | `custom_yaml_path: ""` なので、table_row用の表示制御を検証しにくい |
| `article` 前提が強い | NIIDの `annex` や海外文書の `chapter/section` では止めどころが変わる |

### 表示プロファイル案

実装方針としては、次のような表現にする。

```yaml
context_display_policy:
  - when_kind: table_row
    group_under_kind: table
    include_ancestors_until_kinds:
      - article
      - section
      - annex
      - appendix
    include_table_header: true
    include_sibling_rows: selected_only
    suppress_duplicate_headings: true

render_templates:
  table_row:
    render_as: markdown_table
    show_table_heading: once
    show_header: true
```

### NIID別表7での具体例

NIIDの別表7は、`annex` と `table` が同じ具体表題を持つ。

```yaml
nid: ann7
kind: annex
num: 別表7
heading: 記帳事項に関する一覧（法第５６条の２３関係）
children:
  - nid: ann7.tbl1
    kind: table
    heading: 記帳事項に関する一覧（法第５６条の２３関係）
    children:
      - nid: ann7.tbl1.tblh_visual
        kind: table_header
        text: category | 省令での記載項目 | 記帳の内容 | 1種病原体等 | 2種病原体等 | 3種病原体等
```

選択例:

```yaml
selection_nids:
  - "ann7.tbl1.tblh_visual.tblr1"
  - "ann7.tbl1.tblh_visual.tblr2"
```

悪い表示:

```markdown
別表7 記帳事項に関する一覧（法第５６条の２３関係）
記帳事項に関する一覧（法第５６条の２３関係）
category | 省令での記載項目 | 記帳の内容 | 1種病原体等 | 2種病原体等 | 3種病原体等
...
```

望ましい表示:

```markdown
### 別表7 記帳事項に関する一覧（法第５６条の２３関係）

| category | 省令での記載項目 | 記帳の内容 | 1種病原体等 | 2種病原体等 | 3種病原体等 |
| --- | --- | --- | --- | --- | --- |
| 病原体等 | 受入れ又は払出しに係る病原体等の種類（毒素にあっては、その種類及び量） | 事業所ごとに受入れ元、払出し先等を記帳（実験室が複数ある場合にはそれら実験室ごとに記帳） | 有 | 有 | 有 |
| 病原体等 | 病原体等の受入れ又は払出しの日時 | 事業所ごとに記帳（同上） | 年月日・時刻 | 年月日 | 年月日 |
```

---

## 次の実装タスク案

### 1. 表示例4を実データに合わせる

採用方針:

```yaml
law_folder: "jp_pmda_api_gmp_guideline_20011102"
selection_nids:
  - "cha1.sec1_3.tbl1.tblh.tblr1"
  - "cha1.sec1_3.tbl1.tblh.tblr3"
```

1行目と3行目を選び、2行目を飛ばす。

### 2. table_row用プロファイルを1つ追加する

例:

```text
data/mock_ui/profiles/table_row_context_default.yaml
```

入れるもの:

- `table_row` は `table` 単位でグループ化する
- `table_header` は表ヘッダとして1回だけ出す
- `appendix/table` または `annex/table` の重複見出しを抑制する
- sibling rowは `selected_only` を基本にする

### 3. 表示例3/4にprofileを紐づける

```yaml
profile:
  mode: "custom"
  custom_yaml_path: "data/mock_ui/profiles/table_row_context_default.yaml"
```

### 4. テストで固定する

見るべきテスト観点:

| 観点 | 期待 |
| --- | --- |
| 表示例4 | 2つのNIDが選択される |
| Markdown表 | 2行が1つの表として出る |
| 見出し | `別表` や同一表題が連続しない |
| profile | `custom_yaml_path` が実効設定に反映される |
