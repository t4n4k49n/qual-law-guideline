# Structure Reconstruction Check

## Summary

Reviewed EU GMP Vol.4 Chapter 4-9 promotion candidates generated from the approved preparation run.

## Heading Check

Each document has exactly one chapter node. Unnumbered headings are represented as section nodes and were not absorbed into the previous paragraph text.

| doc_id | chapter heading | section count |
|---|---|---:|
| `eu_gmp_vol4_chap4_20110101` | Documentation | 17 |
| `eu_gmp_vol4_chap5_20150123` | Production | 10 |
| `eu_gmp_vol4_chap6_20140328` | Quality Control | 8 |
| `eu_gmp_vol4_chap7_20120628` | Outsourced Activities | 5 |
| `eu_gmp_vol4_chap8_20140813` | Complaints, Quality Defects and Product Recalls | 6 |
| `eu_gmp_vol4_chap9_undated` | SELF INSPECTION | 1 |

Profile guard confirmed that references such as `Chapter 1` and `Chapter 7` in ordinary text are not parsed as structural chapter nodes.

## Whitespace Check

Generated `heading` and `text` fields were scanned for:

- leading/trailing whitespace
- tabs
- embedded newlines
- repeated spaces

Result: `0` issues.

## Tables And Notes

`special_structure_audit` reports no source tables, generated tables, or unresolved special blocks for Chapters 4-9. No merged-cell replication was needed.

Ordinary notes are separated from body text:

- Chapter 4: 1 `note` node
- Chapter 7: 1 `note` node

No table notes were detected.

## Review Sample

`SAMPLE_EXTRACT.md` records a deep Chapter 6 item sample with full ancestor path:

- `root`
- `cha6` / `chapter` / `Quality Control`
- `cha6.sec8` / `section` / `Technical transfer of testing methods`
- `cha6.sec8.p6_39` / `paragraph` / `6.39`
- `cha6.sec8.p6_39.iiv` / `item` / `iv.`
