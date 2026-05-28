# 深い階層サンプル抽出

- source: `runs/20260528-182258295_run-normalized-pics-annex1-v3/promotion_candidate/pics_pe00917_annex1_20230825.regdoc_ir.yaml`
- target_nid: `ann1.sec4.p4_27.tbl1.tblh`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann1` | `annex` | `ANNEX` | `MANUFACTURE OF STERILE MEDICINAL PRODUCTS` |
| 3 | `ann1.sec4` | `section` | `4` | `Premises` |
| 4 | `ann1.sec4.p4_27` | `paragraph` | `4.27` | `For cleanroom classification, the total of particles equal to or greater than 0.5 and 5 µm should be measured. This measurement should be performed both at rest and in simulated operations in accordance with the limits specified in Table 1.` |
| 5 | `ann1.sec4.p4_27.tbl1` | `table` | `table` | `Table 1: Maximum permitted total particle concentration for classification` |
| 6 | `ann1.sec4.p4_27.tbl1.tblh` | `table_header` | `table_header` | `Grade | Maximum limits for total particle >= 0.5 µm/m3 at rest | Maximum limits for total particle >= 0.5 µm/m3 in operation | Maximum limits for total particle >= 5 µm/m3 at rest | Maximum limits for total particle >= 5 µm/m3 in operation` |
