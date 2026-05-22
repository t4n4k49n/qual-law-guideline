# WHO LBM Chapter 8 Survey Table Report

## 結論

WHO LBM 3rd Chapter 8 の Table 5-7 は、通常本文ではなく survey/checklist table として処理する必要がある。

今回の実装では、対象文書 `who_lbm_3rd_2004_9241546506` の Table 5-7 だけを専用 parser で抽出し、`table` -> `table_header` -> `table_row` に構造化した。

## 対象外にしたもの

次の情報は form control / form scaffolding として human-visible text から除外した。

- `Location`
- `Date`
- `Person in charge of laboratory`
- `CHECKED ITEM (ENTER DATE OF CHECK)`
- `YES` / `NO` / `N/A` / `COMMENTS`
- checkbox/control/private-use glyph
- dot leaders
- signature fields
- `Brand:` / `Type:` / `Serial no.:`

## 残したもの

次の情報は source content として残した。

- table caption
- table-internal section heading
- checklist item row text

## Row Count

| Table | Heading | Rows |
|---|---|---:|
| 5 | Table 5. Basic Laboratory – Biosafety Level 1: laboratory safety survey | 81 |
| 6 | Table 6. Basic laboratory – Biosafety Level 2: laboratory safety survey. | 37 |
| 7 | Table 7. Containment laboratory – Biosafety Level 3: laboratory safety survey. | 15 |
| Total |  | 133 |

## Section Count

| Table | Section | Rows |
|---|---|---:|
| 5 | Laboratory | 3 |
| 5 | Laboratory design | 6 |
| 5 | Gas cylinders | 4 |
| 5 | Chemicals | 8 |
| 5 | Refrigerators/freezers/cold rooms | 4 |
| 5 | Electrical equipment | 10 |
| 5 | Personal protective equipment | 6 |
| 5 | Waste management | 7 |
| 5 | Occupational health and safety programmes available | 6 |
| 5 | General engineering controls | 8 |
| 5 | General practices and procedures | 7 |
| 5 | General laboratory housekeeping | 4 |
| 5 | Fire protection | 6 |
| 5 | Heated constant temperature baths | 2 |
| 6 | Biological safety cabinet (BSC) | 7 |
| 6 | Laboratory | 6 |
| 6 | Decontamination | 4 |
| 6 | Handling of contaminated waste | 6 |
| 6 | Personal protection | 6 |
| 6 | Practices | 7 |
| 6 | Facility | 1 |
| 7 | Facility | 5 |
| 7 | Personal protection | 3 |
| 7 | Hand protection | 1 |
| 7 | Respiratory protection | 1 |
| 7 | Practices | 5 |

## Golden Rows

| Expected row | NID |
|---|---|
| No trash on floor | `cha8.tbl5.tblh8.tblr6` |
| Microwave oven(s) clearly labelled “No Food Preparation, Laboratory Use Only” | `cha8.tbl5.tblh11.tblr2` |
| Information on sign accurate and current | `cha8.tbl6.tblh2.tblr4` |
| Sign legible and not defaced | `cha8.tbl6.tblh2.tblr5` |

## Forbidden Text Audit

Regenerated WHO LBM IR では以下の検出件数がすべて 0。

| Pattern | Hits |
|---|---:|
| `\x01` | 0 |
| `` | 0 |
| long dot leaders | 0 |
| `CHECKED ITEM (ENTER DATE OF CHECK)` | 0 |
| `YES NO N/A COMMENTS` | 0 |
| `Location Date` | 0 |
| `Person in charge of laboratory` | 0 |
| `Safety surveyor` | 0 |
| `Date survey completed` | 0 |
| `Brand:` | 0 |
| `Type:` | 0 |
| `Serial no.:` | 0 |
| `cha8.i5.si*` | 0 |

## UI Review

処理後の YAML を `out/who_lbm_3rd_review_ui/` に複写済み。起動中の review UI で同フォルダを参照して確認できる。

## 残リスク

この実装は WHO LBM 3rd Chapter 8 Table 5-7 に限定した special parser であり、一般的なPDFフォーム復元器ではない。将来の別文書・別版WHO LBMに同型の survey table が出た場合は、今回の parser を拡張対象として評価する必要がある。
