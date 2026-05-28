# PIC/S Annex 1 table visual reconstruction

This file records the visual review used to normalize table cell structure in PIC/S Annex 1. The source images are rendered from `data/human-readable/pics/source_docs/pe009-17_annexes_docview_8881.pdf`.

## Table 1

- Source image: `source_pages/annex1_tables_p19_20-020.png`
- Header: two grouped particle-size headers, each spanning `at rest` and `in operation`.
- Grade D: both `in operation` values wrap over two visual lines but remain one logical cell each.
- Result: four grade records A-D, with grouped headers retained in IR metadata.

## Table 2

- Source image: `source_pages/annex1_tables_p21-021.png`
- Grade A: one `No growth` cell spans Air sample, Settle plates, and Contact plates.
- Result: the merged cell is expanded to all three normalized method columns and marked as an expanded column span.

## Table 3

- Source image: `source_pages/annex1_tables_p30_31-031.png`
- Grade C: one grade cell spans two operation rows.
- Result: the row span is expanded into two Grade C records.

## Table 4

- Source image: `source_pages/annex1_tables_p32-032.png`
- Grade A: one grade cell spans eight operation rows.
- Grade B: one grade cell spans two operation rows.
- Grade C: one grade cell maps to one operation row.
- Grade D: one grade cell spans four operation rows.
- Result: text-extraction grade drift was corrected from visual row spans. In particular, `Background support for grade A` is Grade B, and `Cleaning of equipment` plus `Handling of components...` are Grade D.

## Table 5

- Source image: `source_pages/annex1_tables_p56_59-058.png`
- Header: two grouped particle-size headers, each spanning `at rest` and `in operation`.
- Grade D: both `in operation` values wrap over two visual lines but remain one logical cell each.
- Result: four grade records A-D, with grouped headers retained in IR metadata.

## Table 6

- Source image: `source_pages/annex1_tables_p60-060.png`
- Grade A: one `No growth(c)` cell spans Air sample, Settle plates, Contact plates, and Glove print.
- Result: the merged cell is expanded to all four normalized method columns and marked as an expanded column span.
