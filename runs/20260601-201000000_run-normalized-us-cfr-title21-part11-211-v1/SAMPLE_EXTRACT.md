# 深い階層サンプル

このRUNでは 21 CFR Part 11 / Part 211 の両方から深い階層を抽出した。

## 21 CFR Part 11

target_nid: `part11.subptc.sec11_200.pa.i1.sii`

| 階層 | nid | kind | text / heading |
|---:|---|---|---|
| 1 | `root` | `document` |  |
| 2 | `part11` | `part` | `ELECTRONIC RECORDS; ELECTRONIC SIGNATURES` |
| 3 | `part11.subptc` | `subpart` | `Electronic Signatures` |
| 4 | `part11.subptc.sec11_200` | `section` | `Electronic signature components and controls.` |
| 5 | `part11.subptc.sec11_200.pa` | `paragraph` | `Electronic signatures that are not based upon biometrics shall:` |
| 6 | `part11.subptc.sec11_200.pa.i1` | `item` | `Employ at least two distinct identification components such as an identification code and password.` |
| 7 | `part11.subptc.sec11_200.pa.i1.sii` | `subitem` | `When an individual executes a series of signings during a single, continuous period of controlled system access, the first signing shall be executed using all electronic signature components; subsequent signings shall be executed using at least one electronic signature component that is only executable by, and designed to be used only by, the individual.` |

## 21 CFR Part 211

target_nid: `part211.subptc.sec211_42.pc.i10.sivi`

| 階層 | nid | kind | text / heading |
|---:|---|---|---|
| 1 | `root` | `document` |  |
| 2 | `part211` | `part` | `CURRENT GOOD MANUFACTURING PRACTICE FOR FINISHED PHARMACEUTICALS` |
| 3 | `part211.subptc` | `subpart` | `Buildings and Facilities` |
| 4 | `part211.subptc.sec211_42` | `section` | `Design and construction features.` |
| 5 | `part211.subptc.sec211_42.pc` | `paragraph` | `Operations shall be performed within specifically defined areas of adequate size. There shall be separate or defined areas or such other control systems for the firm's operations as are necessary to prevent contamination or mixups during the course of the following procedures:` |
| 6 | `part211.subptc.sec211_42.pc.i10` | `item` | `Aseptic processing, which includes as appropriate:` |
| 7 | `part211.subptc.sec211_42.pc.i10.sivi` | `subitem` | `A system for maintaining any equipment used to control the aseptic conditions.` |

## 確認観点

- Part 11: `(a)(1)(i)` が paragraph/item/subitem として保持される。
- Part 211: `§ 211.42(c)(10)(vi)` が item配下のsubitemとして保持される。
- Part 211: `§ 211.67(b)(6)` 後の `(c)` は section直下の paragraph に戻ることをテスト済み。
