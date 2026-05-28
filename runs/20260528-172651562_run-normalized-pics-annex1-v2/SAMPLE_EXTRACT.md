# 深い階層サンプル抽出

- source: `runs/20260528-172651562_run-normalized-pics-annex1-v2/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_ir.yaml`
- target_nid: `ann1.sec8.tbl4.tblh.tblr12`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann1` | `annex` | `ANNEX` | `MANUFACTURE OF STERILE MEDICINAL PRODUCTS` |
| 3 | `ann1.sec8` | `section` | `8` | `Production and Specific Technologies` |
| 4 | `ann1.sec8.tbl4` | `table` | `table` | `Table 4: Examples of operations and grades for aseptic preparation and processing operations` |
| 5 | `ann1.sec8.tbl4.tblh` | `table_header` | `table_header` | `Grade | Operation` |
| 6 | `ann1.sec8.tbl4.tblh.tblr12` | `table_row` | `table_row` | `Grade D | Cleaning of equipment.` |
