# 深い階層サンプル抽出

- source: `runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/promotion_candidate/us_cfr_title21_part11_20251027/us_cfr_title21_part11_20251027.regdoc_ir.yaml`
- target_nid: `part11.subptc.sec11_200.pa.i1.sii`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `part11` | `part` | `PART` | `ELECTRONIC RECORDS; ELECTRONIC SIGNATURES` |
| 3 | `part11.subptc` | `subpart` | `Subpart` | `Electronic Signatures` |
| 4 | `part11.subptc.sec11_200` | `section` | `§` | `Electronic signature components and controls.` |
| 5 | `part11.subptc.sec11_200.pa` | `paragraph` | `(a)` | `Electronic signatures that are not based upon biometrics shall:` |
| 6 | `part11.subptc.sec11_200.pa.i1` | `item` | `(1)` | `Employ at least two distinct identification components such as an identification code and password.` |
| 7 | `part11.subptc.sec11_200.pa.i1.sii` | `subitem` | `(i)` | `When an individual executes a series of signings during a single, continuous period of controlled system access, the first signing shall be executed using all electronic signature components; subsequent signings shall be executed using at least one electronic signature component that is only executable by, and designed to be used only by, the individual.` |
