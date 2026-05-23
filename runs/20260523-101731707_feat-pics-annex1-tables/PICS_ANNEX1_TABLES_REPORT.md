# PICS ANNEX 1 TABLES REPORT

- doc_id: `pics_pe00917_annex1_20230825`
- tables: 6
- table_rows: 35
- notes: 15

| table | rows | notes | heading |
|---:|---:|---:|---|
| 1 | 4 | 2 | Table 1: Maximum permitted total particle concentration for classification |
| 2 | 4 | 5 | Table 2: Maximum permitted microbial contamination level during qualification |
| 3 | 4 | 0 | Table 3: Examples of operations and grades for terminally sterilised preparation and processing operations |
| 4 | 15 | 0 | Table 4: Examples of operations and grades for aseptic preparation and processing operations |
| 5 | 4 | 3 | Table 5: Maximum permitted total particle concentration for monitoring. |
| 6 | 4 | 5 | Table 6: Maximum action limits for viable particle contamination |

## Before / After Examples

### Table 1

Before:
```yaml
nid: ann1.sec4.p4_27.pre1
kind: preformatted
kind_raw: possible_table
sample: |
  Table 1: Maximum permitted total particle concentration for classification
  Maximum limits for total particle       Maximum limits for total particle
  Grade                ≥ 0.5 µm/m3                               ≥ 5 µm/m3
```

After:
```yaml
nid: ann1.sec4.p4_27.tbl1
kind: table
heading: Table 1: Maximum permitted total particle concentration for classification
row_samples:
  - A | 3 520 | 3 520 | Not specified (a) | Not specified (a)
  - B | 3 520 | 352 000 | Not specified (a) | 2 930
  - C | 352 000 | 3 520 000 | 2 930 | 29 300
note_count: 2
```

### Table 2

Before:
```yaml
nid: ann1.sec4.p4_31.pre1
kind: preformatted
kind_raw: possible_table
sample: |
  Table 2: Maximum permitted microbial contamination level during qualification
  Settle plates          Contact plates
  Grade            Air sample                    (diameter 90 mm)           (diameter 55
  CFU/m3                        CFU/4 hours (a)          mm) CFU/plate
  A                                           No growth
  B                     10                            5                         5
  C                    100                           50                        25
  D             
```

After:
```yaml
nid: ann1.sec4.p4_31.tbl2
kind: table
heading: Table 2: Maximum permitted microbial contamination level during qualification
row_samples:
  - A | No growth | No growth | No growth
  - B | 10 | 5 | 5
  - C | 100 | 50 | 25
note_count: 5
```

### Table 3

Before:
```yaml
nid: ann1.sec8.p8_6
kind: paragraph
kind_raw: 8.6
sample: |
  Examples of operations to be carried out in the various grades are given in Table 3.
  
  Table 3: Examples of operations and grades for terminally sterilised preparation and processing operations
        Grade A    -     Filling of products, when unusually at risk.
        Grade C    -     Preparation of solutions, when unusually at risk.
                   -     Filling of products.
        Grade D    -     Preparation of solutions and components for subsequent filling.
  ASEPTIC PREPARATION AND PROCESSING
```

After:
```yaml
nid: ann1.sec8.tbl3
kind: table
heading: Table 3: Examples of operations and grades for terminally sterilised preparation and processing operations
row_samples:
  - Grade A | Filling of products, when unusually at risk.
  - Grade C | Preparation of solutions, when unusually at risk.
  - Grade C | Filling of products.
note_count: 0
```

### Table 4

Before:
```yaml
nid: ann1.sec8.p8_10
kind: paragraph
kind_raw: 8.10
sample: |
  Examples of operations to be carried out in the various environmental grades are given in Table 4.
  
  Table 4:   Examples of operations and grades for aseptic preparation and processing operations
              -   Aseptic assembly of filling equipment.
              -   Connections made under aseptic conditions (where sterilised product contact
                  surfaces are exposed) that are post the final sterilising grade filter. These
                  connections should be sterilised by steam-in-pla
```

After:
```yaml
nid: ann1.sec8.tbl4
kind: table
heading: Table 4: Examples of operations and grades for aseptic preparation and processing operations
row_samples:
  - Grade A | Aseptic assembly of filling equipment.
  - Grade A | Connections made under aseptic conditions (where sterilised product contact surfaces are exposed) that are post the final sterilising grade filter. These connections should be sterilised by steam-in-place whenever possible.
  - Grade A | Aseptic compounding and mixing.
note_count: 0
```

### Table 5

Before:
```yaml
nid: ann1.sec9.p9_15.pre1
kind: preformatted
kind_raw: possible_table
sample: |
  Table 5: Maximum permitted total particle concentration for monitoring.
  Maximum limits for total particle          Maximum limits for total particle
  Grade                  ≥ 0.5 μm/m3                                  ≥ 5 μm/m3
  at rest          in operation             at rest           in operation
  A              3 520                3 520                  29                    29
  B              3 520               352 000                 29                  2 930
  C             352 000          
```

After:
```yaml
nid: ann1.sec9.p9_15.tbl5
kind: table
heading: Table 5: Maximum permitted total particle concentration for monitoring.
row_samples:
  - A | 3 520 | 3 520 | 29 | 29
  - B | 3 520 | 352 000 | 29 | 2 930
  - C | 352 000 | 3 520 000 | 2 930 | 29 300
note_count: 3
```

### Table 6

Before:
```yaml
nid: ann1.sec9.p9_30.pre1
kind: preformatted
kind_raw: possible_table
sample: |
  Table 6: Maximum action limits for viable particle contamination
  Settle plates           Contact plates         Glove print,
  Grade          Air sample        (diam. 90 mm)           (diam. 55mm),     Including 5 fingers on
  CFU /m3           CFU /4 hours(a)         CFU / plate(b)         both hands
```

After:
```yaml
nid: ann1.sec9.p9_30.tbl6
kind: table
heading: Table 6: Maximum action limits for viable particle contamination
row_samples:
  - A | No growth (c) | No growth (c) | No growth (c) | No growth (c)
  - B | 10 | 5 | 5 | 5
  - C | 100 | 50 | 25 | -
note_count: 5
```

