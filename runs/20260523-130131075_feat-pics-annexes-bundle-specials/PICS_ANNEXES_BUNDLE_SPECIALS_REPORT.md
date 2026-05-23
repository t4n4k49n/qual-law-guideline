# PICS Annexes Bundle Specials Report

## Summary

PIC/S Annexes combined document now reuses the existing Annex 1 and Annex 2A special parsers, and adds scoped handling for the newly identified Annex 2B Table 1 and Annex 20 Figure 1 structures.

## Reused Parsers

| Area | Parser | Result |
|---|---|---|
| Annex 1 Tables 1-6 | `pics_annex1_tables` | Preserved |
| Annex 2A Table 1 | `pics_annex2a_table1` | Preserved |
| Annex 2A Figures 1-3 | `pics_annex2a_flow_figures` | Preserved |

## Newly Structured Targets

| Target | Parser | IR result |
|---|---|---|
| Annex 2B Table 1 | `pics_annexes_bundle_specials` | `table` with 6 columns, 7 `table_row` children, 7 `note` children |
| Annex 20 Figure 1 | `pics_annexes_bundle_specials` | `figure` with informative role and ordered QRM process labels |

## AFTER Metrics

| Metric | Value |
|---|---:|
| `verify_document` | pass |
| Source span coverage | 1.0 |
| Annex nodes | 20 |
| Tables | 8 |
| Table rows | 48 |
| Figures | 4 |
| Notes | 27 |

## Gate Status

The full promotion goal check remains `FAIL` because 8 unresolved special-structure candidates remain outside this prompt's target scope. The target structures from this prompt are not present in the unresolved list after the latest regeneration.

## Remaining Candidates

| Node | Trigger | Resolution |
|---|---|---|
| `ann3.sec3.si4` | fixed-width block in ordinary text | targeted parser |
| `ann7.sec16` | form-control text in ordinary text | profile rule |
| `ann14.sec10` | fixed-width block in ordinary text | targeted parser |
| `ann14.sec2_2.p2_5` | fixed-width block in ordinary text | targeted parser |
| `ann14.sec1_3` | fixed-width block in ordinary text | targeted parser |
| `ann14.sec2_3` | fixed-width block in ordinary text | targeted parser |
| `ann19.sec10.p10_3` | form-control text in ordinary text | profile rule |
| `ann20.sec7_2.ii.si14` | form-control text in ordinary text | profile rule |

## Notes

- Annex 2B source shading is not recoverable from the text layer, so `shading_reconstructed: false` and an explicit `shading_note` are attached to the table data.
- `ANNEX 20*` is now recognized as an annex marker, which allows Annex 20 Figure 1 to be normalized in the combined Annexes document.
