# 深い階層サンプル抽出

- source: `runs/20260527-133746129_run-normalized-eu-gmp-vol4-chap1-v1/promotion_candidate/eu_gmp_vol4_chap1_20130131.regdoc_ir.yaml`
- target_nid: `cha1.p1_8.iiii.si3`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha1` | `chapter` | `Chapter` | `Pharmaceutical Quality System` |
| 3 | `cha1.p1_8` | `paragraph` | `1.8` |  |
| 4 | `cha1.p1_8.iiii` | `item` | `(iii)` | `All necessary facilities for GMP are provided including:` |
| 5 | `cha1.p1_8.iiii.si3` | `subitem` | `•` | `Suitable equipment and services;` |
