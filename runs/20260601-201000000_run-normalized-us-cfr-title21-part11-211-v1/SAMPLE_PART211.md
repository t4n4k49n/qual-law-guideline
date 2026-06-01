# 深い階層サンプル抽出

- source: `runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/promotion_candidate/us_cfr_title21_part211_20251027/us_cfr_title21_part211_20251027.regdoc_ir.yaml`
- target_nid: `part211.subptc.sec211_42.pc.i10.sivi`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `part211` | `part` | `PART` | `CURRENT GOOD MANUFACTURING PRACTICE FOR FINISHED PHARMACEUTICALS` |
| 3 | `part211.subptc` | `subpart` | `Subpart` | `Buildings and Facilities` |
| 4 | `part211.subptc.sec211_42` | `section` | `§` | `Design and construction features.` |
| 5 | `part211.subptc.sec211_42.pc` | `paragraph` | `(c)` | `Operations shall be performed within specifically defined areas of adequate size. There shall be separate or defined areas or such other control systems for the firm's operations as are necessary to prevent contamination or mixups during the course of the following procedures:` |
| 6 | `part211.subptc.sec211_42.pc.i10` | `item` | `(10)` | `Aseptic processing, which includes as appropriate:` |
| 7 | `part211.subptc.sec211_42.pc.i10.sivi` | `subitem` | `(vi)` | `A system for maintaining any equipment used to control the aseptic conditions.` |
