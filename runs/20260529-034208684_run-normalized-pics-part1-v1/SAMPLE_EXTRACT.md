# 深い階層サンプル抽出

- source: `runs/20260529-034208684_run-normalized-pics-part1-v1/promotion_candidate/pics_pe00917_part1_20230825.regdoc_ir.yaml`
- target_nid: `cha1.p1_8.iiii.si5`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha1` | `chapter` | `CHAPTER` | `PHARMACEUTICAL QUALITY SYSTEM` |
| 3 | `cha1.p1_8` | `paragraph` | `1.8` |  |
| 4 | `cha1.p1_8.iiii` | `item` | `(iii)` | `All necessary facilities for GMP are provided including:` |
| 5 | `cha1.p1_8.iiii.si5` | `subitem` | `` | `Approved procedures and instructions, in accordance with the                  Pharmaceutical Quality System;` |
