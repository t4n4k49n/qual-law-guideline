# 深い階層サンプル抽出

- source: `runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_ir.yaml`
- target_nid: `ann1.sec9.p9_30.tbl6.tblh.tblr1`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann1` | `annex` | `ANNEX` | `MANUFACTURE OF STERILE MEDICINAL PRODUCTS` |
| 3 | `ann1.sec9` | `section` | `9` | `Environmental & process monitoring` |
| 4 | `ann1.sec9.p9_30` | `paragraph` | `9.30` | `Action limits for viable particle contamination are shown in Table 6.` |
| 5 | `ann1.sec9.p9_30.tbl6` | `table` | `table` | `Table 6: Maximum action limits for viable particle contamination` |
| 6 | `ann1.sec9.p9_30.tbl6.tblh` | `table_header` | `table_header` | `Grade | Air sample CFU/m3 | Settle plates (diameter 90 mm) CFU/4 hours (a) | Contact plates (diameter 55 mm) CFU/plate (b) | Glove print, including 5 fingers on both hands CFU/glove` |
| 7 | `ann1.sec9.p9_30.tbl6.tblh.tblr1` | `table_row` | `table_row` | `A | No growth (c) | No growth (c) | No growth (c) | No growth (c)` |
