# 深い階層サンプル抽出

- source: `runs/20260529-022734132_run-normalized-pics-part2-v1/promotion_candidate/pics_pe00917_part2_20230825.regdoc_ir.yaml`
- target_nid: `cha1.sec1_2.tbl1.tblh.tblr7`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha1` | `chapter` | `1.` | `INTRODUCTION` |
| 3 | `cha1.sec1_2` | `section` | `1.2` |  |
| 4 | `cha1.sec1_2.tbl1` | `table` | `table` |  |
| 5 | `cha1.sec1_2.tbl1.tblh` | `table_header` | `table_header` | `Type of Manufacturing | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 1 | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 2 | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 3 | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 4 | Application of this Guide to steps (shown in grey) used in this type of manufacturing step 5` |
| 6 | `cha1.sec1_2.tbl1.tblh.tblr7` | `table_row` | `table_row` | `“Classical” Fermentation to produce an API | Establishment of cell bank | Maintenance of the cell bank | Introduction of the cells into fermentation | Isolation and purification | Physical processing, and packaging` |
