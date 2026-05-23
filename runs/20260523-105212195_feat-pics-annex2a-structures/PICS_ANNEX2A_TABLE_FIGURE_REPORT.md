# PICS ANNEX 2A TABLE / FIGURE REPORT

- doc_id: `pics_pe00917_annex2a_20230825`
- tables: `1`
- table_rows: `6`
- table_notes: `3`
- figures: `3`

## Table 1

Before:
```yaml
nid: ann2a.sec2.ib
kind: item
heading: null
text_sample: "...on those early stages may apply.\n             Annex 2A Manufacture\
  \ of advanced therapy medicinal products for human use\nTable 1. Illustrative guide\
  \ to manufacturing activities within the scope of Annex 2A\n\nExample\n        \
  \                                      Application of this Annex (see note 1)\n\
  Products\n                   Linear DNA\n Gene therapy:                        \
  \   In vitro cell free                                         Formulation,\n  \
  \                 template                                        mRNA purification\n\
  \ mRNA                                    transcription                        \
  \                      filling\n                   preparation\nGene therapy:\n\
  \                   Plasmid               Establishment of MCB,     Vector manufacturing\
  \ and         Formulation,\nin vivo viral\n    ..."
tags: []
```

After:
```yaml
nid: ann2a.sec2.ib.tbl1
kind: table
heading: Table 1. Illustrative guide to manufacturing activities within the scope
  of Annex 2A
columns:
- Example product / product class
- Manufacturing step 1
- Manufacturing step 2
- Manufacturing step 3
- Manufacturing step 4
row_samples:
- - 'Gene therapy: mRNA'
  - Linear DNA template preparation
  - In vitro cell free transcription
  - mRNA purification
  - Formulation, filling
- - 'Gene therapy: in vivo viral vectors'
  - Plasmid manufacturing
  - Establishment of MCB, WCB2
  - Vector manufacturing and purification
  - Formulation, filling
- - 'Gene therapy: in vivo non-viral vectors (naked DNA, lipoplexes, polyplexes, etc.)'
  - Plasmid manufacturing
  - Establishment of bacterial bank2
  - Fermentation and purification
  - Formulation, filling
note_count: 3
shading_reconstructed: false
shading_note: PDF shading is not reliably represented in the text layer.
```

## Figure 1

Before:
```yaml
nid: ann2a.sec2.ib
kind: item
heading: null
text_sample: "...cts for human use\nThe following are some non-exhaustive examples\
  \ in the application of GMP to the manufacture of ATMP.\n\nFigure 1: Example of\
  \ gene therapy mRNA                     Figure 2: Example of in vivo viral vector\
  \ gene\n          ATMP manufacturing                                         therapy\
  \ ATMP manufacturing\n Linear DNA template         ATMP Manufacturing          \
  \        Plasmid                ATMP Manufacturing\n     preparation           \
  \                                    Manufacturing\n                           \
  \      Transcription                                           Establishing MCB\
  \ or\nPlasmid DNA construct                    ↓                 Plasmid DNA construct\
  \                 WCB\n      preparation                 Purification          \
  \         preparation                        ↓\n  ..."
tags: []
```

After:
```yaml
nid: ann2a.sec2.ib.fig1
kind: figure
heading: 'Figure 1: Example of gene therapy mRNA ATMP manufacturing'
parse_confidence: split_from_side_by_side_caption
columns:
- label: linear DNA template path
  step_count: 9
  first_steps:
  - Linear DNA template preparation
  - Plasmid DNA construct preparation
  - Transfer of Plasmid DNA to starter colony (e.g. E. coli)
- label: ATMP manufacturing
  step_count: 7
  first_steps:
  - Transcription
  - Purification
  - Harvest
```

## Figure 2

Before:
```yaml
nid: ann2a.sec2.ib
kind: item
heading: null
text_sample: "...cts for human use\nThe following are some non-exhaustive examples\
  \ in the application of GMP to the manufacture of ATMP.\n\nFigure 1: Example of\
  \ gene therapy mRNA                     Figure 2: Example of in vivo viral vector\
  \ gene\n          ATMP manufacturing                                         therapy\
  \ ATMP manufacturing\n Linear DNA template         ATMP Manufacturing          \
  \        Plasmid                ATMP Manufacturing\n     preparation           \
  \                                    Manufacturing\n                           \
  \      Transcription                                           Establishing MCB\
  \ or\nPlasmid DNA construct                    ↓                 Plasmid DNA construct\
  \                 WCB\n      preparation                 Purification          \
  \         preparation                        ↓\n  ..."
tags: []
```

After:
```yaml
nid: ann2a.sec2.ib.fig2
kind: figure
heading: 'Figure 2: Example of in vivo viral vector gene therapy ATMP manufacturing'
parse_confidence: split_from_side_by_side_caption
columns:
- label: plasmid manufacturing
  step_count: 6
  first_steps:
  - Plasmid Manufacturing
  - Plasmid DNA construct preparation
  - Transfer of Plasmid DNA to starter colony (e.g. E. coli)
- label: ATMP manufacturing
  step_count: 11
  first_steps:
  - Establishing MCB or WCB
  - Thawing
  - Transfection
```

## Figure 3

Before:
```yaml
nid: ann2a.sec2.ib.si2
kind: subitem
heading: null
text_sample: "...                        application of GMP.\n\nAnnex 2A Manufacture\
  \ of advanced therapy medicinal products for human use\n\nFigure 3: Example of autologous\
  \ CAR-T therapy ATMP manufacturing\n    Plasmid Manufacturing             Viral\
  \ Vector Product             ATMP Manufacturing\n                              \
  \           Manufacturing\n     Plasmid DNA construct          Establishing MCB\
  \ or WCB         Donation or procurement of\n          preparation             \
  \                ↓                        patient cells\n                ↓     \
  \                       Thawing                              ↓\n   Transfer of Plasmid\
  \ DNA to                     ↓                        Transduction\n         starter\
  \ colony                    Transfection                           ↓\n         \
  \ (e.g. E. coli)                          ..."
tags: []
```

After:
```yaml
nid: ann2a.sec2.ib.fig3
kind: figure
heading: 'Figure 3: Example of autologous CAR-T therapy ATMP manufacturing'
parse_confidence: explicit_caption
columns:
- label: plasmid manufacturing
  step_count: 5
  first_steps:
  - Plasmid DNA construct preparation
  - Transfer of Plasmid DNA to starter colony (e.g. E. coli)
  - Expansion
- label: viral vector product manufacturing
  step_count: 9
  first_steps:
  - Establishing MCB or WCB
  - Thawing
  - Transfection
- label: ATMP manufacturing
  step_count: 8
  first_steps:
  - Donation or procurement of patient cells
  - Transduction
  - Expansion
```
