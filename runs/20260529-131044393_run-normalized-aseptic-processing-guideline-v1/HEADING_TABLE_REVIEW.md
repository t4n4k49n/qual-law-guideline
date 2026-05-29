# Heading/Table Review

対象: `jp_pmda_aseptic_processing_guideline_20110420`

## Heading Review

深い階層サンプルとして `cha7.sec7_1.p7_1_1` を抽出し、祖先経路を確認した。

| level | nid | kind | heading/text |
|---:|---|---|---|
| 1 | `root` | document | document root |
| 2 | `cha7` | chapter | 無菌医薬品に係る製品の作業所 |
| 3 | `cha7.sec7_1` | section | 清浄度レベルによる作業所の分類 |
| 4 | `cha7.sec7_1.p7_1_1` | paragraph | 重要区域（グレード A） |

確認結果:
- 章・節・細目番号の親子関係は崩れていない。
- 条文上部の見出しがある箇所は `heading` に入り、見出しがない細目は `heading: null` のまま本文を保持している。
- 表1は `cha7.sec7_1` 配下で、`cha7.sec7_1.p7_1_1` の前に配置されている。

## Table Review

### 表1 清浄区域の分類

- table nid: `cha7.sec7_1.tbl1`
- table_header nid: `cha7.sec7_1.tbl1.tblh`
- table_row: 4 rows
- notes: 2 notes
- reconstruction: `visual_reviewed`

結合ヘッダ:

| label | covered columns |
|---|---|
| 名称 | `area_group`, `area_name` |
| 最大許容微粒子数（個／m3） | `non_operational_0_5um`, `non_operational_5_0um`, `operational_0_5um`, `operational_5_0um` |
| 非作業時 | `non_operational_0_5um`, `non_operational_5_0um` |
| 作業時 | `operational_0_5um`, `operational_5_0um` |

確認結果:
- PDF上の結合ヘッダを `header_structure.spanning_headers` に保持している。
- 「無菌操作区域」は重要区域・直接支援区域に複製し、「その他の支援区域」はグレードC/Dに複製している。
- グレードDの「作業形態による注2）」は作業時2列に入っている。

### 表2 微生物管理に係る環境モニタリングの頻度

- table nid: `cha11.sec11_3.tbl2`
- table_header nid: `cha11.sec11_3.tbl2.tblh`
- table_row: 4 rows
- reconstruction: `visual_reviewed`

結合ヘッダ:

| label | covered columns |
|---|---|
| 表面付着微生物 | `surface_attached_equipment_walls`, `surface_attached_gloves_garment` |

確認結果:
- C/D の「製品や容器が環境に曝露される区域」と「その他の区域」は別 table_row として分離している。
- 「表面付着微生物」の結合ヘッダは装置・手袋の2列に保持している。

### 表3 環境微生物の許容基準（作業時）

- table nid: `cha11.sec11_3.tbl3`
- table_header nid: `cha11.sec11_3.tbl3.tblh`
- table_row: 4 rows
- notes: 2 notes
- reconstruction: `visual_reviewed`

結合ヘッダ:

| label | covered columns |
|---|---|
| 空中微生物 | `airborne_microorganisms_cfu_m3`, `settle_plate_cfu_plate` |
| 表面付着微生物 | `contact_plate_cfu_24_30cm2`, `gloves_cfu_5_fingers` |

確認結果:
- `leaf_labels` と `unit_labels` により、浮遊菌・落下菌・コンタクトプレート・手袋の下位見出しと単位を保持している。
- A/B/C/D の4行を table_row として保持している。
- 注1/注2は table note として保持している。

## Summary

- generated_tables: 3
- generated_rows: 12
- table_header: 3
- unresolved_special_blocks: 0
- table_row selectable: true
