# 深い階層サンプル抽出

- source: `runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/promotion_candidate/eu_gmp_vol4_chap2_20140328.regdoc_ir.yaml`
- target_nid: `cha2.sec3.p2_9.ixiii`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha2` | `chapter` | `Chapter` | `Personnel` |
| 3 | `cha2.sec3` | `section` |  | `Key Personnel` |
| 4 | `cha2.sec3.p2_9` | `paragraph` | `2.9` | `The heads of Production, Quality Control and where relevant, Head of Quality Assurance or Head of Quality Unit, generally have some shared, or jointly exercised, responsibilities relating to quality including in particular the design, effective implementation, monitoring and maintenance of the quality management system. These may include, subject to any national regulations:` |
| 5 | `cha2.sec3.p2_9.ixiii` | `item` | `xiii.` | `Ensuring that a timely and effective communication and escalation process exists to raise quality issues to the appropriate levels of management.` |
