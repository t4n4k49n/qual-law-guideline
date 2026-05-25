# 6/7 table record review inventory

| 文書 | table | records | 候補粒度 | table_row昇格 | 保留raw rows | 残課題 |
| --- | --- | ---: | --- | --- | --- | --- |
| 原薬GMPガイドライン | `cha1.p1_3.tbl1` | 7 | reconstructed_record | deferred | 1, 2, 26 | PDF gray-area layout not represented in text source |
| 無菌操作法指針 | `cha7.p7_1.tbl1` | 4 | reconstructed_record | deferred | 1, 2, 3, 4, 5, 7, 8 | multi-level headers and note references need review before replacing raw table_rows |
| 無菌操作法指針 | `cha11.p11_3.tbl2` | 4 | reconstructed_record | deferred | 1, 2, 3 | C/D condition rows are reconstructed but candidate display granularity still needs confirmation |
| 無菌操作法指針 | `cha11.p11_3.tbl3` | 4 | reconstructed_record | deferred | 1, 2, 3 | table notes are preserved but exact note-to-cell references are not fixed |

## Columns

### cha1.p1_3.tbl1

`production_type`, `early_stage_1`, `early_stage_2`, `middle_stage`, `late_stage`, `final_stage`

### cha7.p7_1.tbl1

`area`, `cleanliness_level`, `non_operational_0_5um`, `non_operational_5_0um`, `operational_0_5um`, `operational_5_0um`

### cha11.p11_3.tbl2

`grade`, `area_condition`, `airborne_particles`, `airborne_microorganisms`, `surface_attached_equipment_walls`, `surface_attached_gloves_garment`

### cha11.p11_3.tbl3

`grade`, `airborne_microorganisms_cfu_m3`, `settle_plate_cfu_plate`, `contact_plate_cfu_24_30cm2`, `gloves_cfu_5_fingers`
