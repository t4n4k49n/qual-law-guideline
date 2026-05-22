# TABLE NOTE INVENTORY

代表9文書の入力テキスト側の表・注記候補と、text2ir出力側の表・注記保持状況を比較した。

| 文書 | input table captions | input notes | input fixed-width rows | output table | output table_row | output note | output possible_table | remaining_gap |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| EU GMP Vol.4 Chapter 1 | 0 | 48 | 0 | 0 | 0 | 0 | 0 | none |
| PIC/S Annex 1 | 6 | 14 | 684 | 0 | 0 | 9 | 4 | table_rows_pending |
| PIC/S Annex 11 | 0 | 0 | 46 | 0 | 0 | 0 | 0 | none |
| PIC/S Annex 15 | 0 | 0 | 164 | 0 | 0 | 0 | 0 | none |
| PIC/S Annex 2A | 3 | 75 | 269 | 0 | 0 | 2 | 0 | none |
| PIC/S Annexes refined | 17 | 132 | 2726 | 0 | 0 | 11 | 4 | table_rows_pending |
| PIC/S Part I | 2 | 117 | 381 | 0 | 0 | 2 | 0 | none |
| PIC/S Part II | 6 | 4 | 610 | 0 | 0 | 0 | 0 | none |
| WHO LBM 3rd | 21 | 9 | 1392 | 0 | 0 | 1 | 1 | table_rows_pending |

## Notes

- `possible_table` は、表候補として黙殺せず保持したが、列揃いが安全でないため `table_row` へ分解していないもの。
- input側の検出は候補数であり、PDF由来テキストの崩れや脚注風の箇条書きを含むため、正本上の表数・注記数と完全一致するものではない。
