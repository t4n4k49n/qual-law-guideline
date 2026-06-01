# 深い階層サンプル抽出

- source: `runs/20260601-100409006_run-normalized-eu-gmp-vol4-chap3-v1/promotion_candidate/eu_gmp_vol4_chap3_20150123.regdoc_ir.yaml`
- target_nid: `cha3.sec4.p3_6.iiii`
- method: IR YAMLを確認し、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha3` | `chapter` | `Chapter` | `Premises and Equipment` |
| 3 | `cha3.sec4` | `section` |  | `Production Area` |
| 4 | `cha3.sec4.p3_6` | `paragraph` | `3.6` | `Cross-contamination should be prevented for all products by appropriate design and operation of manufacturing facilities. The measures to prevent cross-contamination should be commensurate with the risks. Quality Risk Management principles should be used to assess and control the risks. Depending of the level of risk, it may be necessary to dedicate premises and equipment for manufacturing and/or packaging operations to control the risk presented by some medicinal products. Dedicated facilities are required for manufacturing when a medicinal product presents a risk because:` |
| 5 | `cha3.sec4.p3_6.iiii` | `item` | `iii.` | `relevant residue limits, derived from the toxicological evaluation, cannot be satisfactorily determined by a validated analytical method.` |
