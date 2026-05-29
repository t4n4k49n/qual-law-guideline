# Structure/Table Review

対象: `jp_pmda_aseptic_processing_guideline_20110420`

## Body Structure Review

### 2章 用語定義

| nid | kind | heading | text starts with |
|---|---|---|---|
| `cha2.sec2_1` | section | アイソレータ(isolator) | 環境及び職員の直接介入から |
| `cha2.sec2_2` | section | アクセス制限バリアシステム（RABS:Restricted Access Barrier System） | グローブを備えた |

確認結果:
- `2.1` / `2.2` は chapter text に畳み込まれていない。
- `用語：説明` の形式は heading と text に分離している。

### 3.1 品質システム一般要求事項

| nid | kind | kind_raw | text starts with |
|---|---|---|---|
| `cha3.sec3_1.i1` | item | `1）` | 全般 |
| `cha3.sec3_1.i2` | item | `2）` | 適用範囲 |
| `cha3.sec3_1.i7` | item | `7）` | 予測的バリデーション及び工程管理の定期照査 |

確認結果:
- `cha3.sec3_1.text` には `1） 全般` 以降を畳み込んでいない。
- `cha3.sec3_1.i7` は `設計・運用`、`工程管理プログラム` に正規化済み。
- `SAMPLE_EXTRACT.md` で `root -> cha3 -> cha3.sec3_1 -> cha3.sec3_1.i7` の祖先経路を確認した。

### 15.4 OCR 揺れ

source text の `1５. ４ 保守・管理` は `cha15.sec15_4` として確認した。

確認結果:
- `cha15.sec15_4.heading` は `保守・管理`。
- 誤った `cha15.sec15_3.i15` は生成されていない。

### 本文空白正規化

確認結果:
- `設計・運 用` / `設計・運\n\n用` は残っていない。
- `プロ グラム` は残っていない。
- `デッド レグ` は `デッドレグ` に正規化済み。
- `枝管 内径` は `枝管内径` に正規化済み。
- ASCII 英数字間の空白は維持している。

## Table Review

### 表1 清浄区域の分類

- table nid: `cha7.sec7_1.tbl1`
- table_row: 4 rows
- reconstruction: `visual_reviewed`

結合ヘッダ:

| label | covered columns |
|---|---|
| 名称 | `area_group`, `area_name` |
| 最大許容微粒子数（個／m3） | `non_operational_0_5um`, `non_operational_5_0um`, `operational_0_5um`, `operational_5_0um` |
| 非作業時 | `non_operational_0_5um`, `non_operational_5_0um` |
| 作業時 | `operational_0_5um`, `operational_5_0um` |

### 表2 微生物管理に係る環境モニタリングの頻度

- table nid: `cha11.sec11_3.tbl2`
- table_row: 4 rows
- reconstruction: `visual_reviewed`

結合ヘッダ:

| label | covered columns |
|---|---|
| 表面付着微生物 | `surface_attached_equipment_walls`, `surface_attached_gloves_garment` |

確認結果:
- C/D の「製品や容器が環境に曝露される区域」と「その他の区域」は別 table_row。
- item 分割後も raw table text は `cha11.sec11_3.i8` に残っていない。

### 表3 環境微生物の許容基準（作業時）

- table nid: `cha11.sec11_3.tbl3`
- table_row: 4 rows
- reconstruction: `visual_reviewed`

結合ヘッダ:

| label | covered columns |
|---|---|
| 空中微生物 | `airborne_microorganisms_cfu_m3`, `settle_plate_cfu_plate` |
| 表面付着微生物 | `contact_plate_cfu_24_30cm2`, `gloves_cfu_5_fingers` |

確認結果:
- `leaf_labels` と `unit_labels` により、下位見出しと単位を保持。
- possible table / preformatted の残骸は残っていない。

## Audit Summary

- nodes: 1116
- section: 114
- item: 630
- table: 3
- table_row: 12
- unresolved_special_blocks: 0
