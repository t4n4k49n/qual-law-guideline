# 深い階層サンプル抽出

- source: `runs/20260601-163000000_run-normalized-eu-gmp-vol4-chap4-9-v1/promotion_candidate/eu_gmp_vol4_chap6_20140328/eu_gmp_vol4_chap6_20140328.regdoc_ir.yaml`
- target_nid: `cha6.sec8.p6_39.iiv`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha6` | `chapter` | `Chapter` | `Quality Control` |
| 3 | `cha6.sec8` | `section` |  | `Technical transfer of testing methods` |
| 4 | `cha6.sec8.p6_39` | `paragraph` | `6.39` | `The transfer protocol should include, but not be limited to, the following parameters:` |
| 5 | `cha6.sec8.p6_39.iiv` | `item` | `iv.` | `Identification of any special transport and storage conditions of test items;` |
