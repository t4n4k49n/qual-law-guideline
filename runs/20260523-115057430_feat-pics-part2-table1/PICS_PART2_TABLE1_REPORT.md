# PICS PART II TABLE 1 REPORT

- doc_id: `pics_pe00917_part2_20230825`
- table: `Table 1: Application of this Guide to API Manufacturing`
- rows: `7`
- notes: `1`

## Before

```yaml
nid: cha1.sec1_2
kind: section
heading: Scope
text_sample: "...s GMP Guide does not apply to steps prior to the introduction of\
  \ the defined \"API Starting Material\".\n                                     \
  \                                                Introduction\nTable 1:    Application\
  \ of this Guide to API Manufacturing\n\nType of\n                            Application\
  \ of this Guide to steps (shown in grey) used in this type of\nManufacturing\n \
  \                                                       manufacturing\n  Chemical\
  \           Production of      Introduction of   Production of     Isolation and\
  \   Physical\n  Manufacturing      the API            the API           Intermediate(s)\
  \   purification    processing,\n                     Starting           Starting\
  \                                            and packaging\n                   \
  \  Material           Material into\n                                        process\n\
  \  API derived        Collection of      Cutting,          Introduction of   Isolation\
  \ and   Physical\n  from animal        organ, fluid,..."
tags: []
```

## After

```yaml
nid: cha1.sec1_2.tbl1
kind: table
heading: 'Table 1: Application of this Guide to API Manufacturing'
columns:
- Type of Manufacturing
- Step 1
- Step 2
- Step 3
- Step 4
- Step 5
row_count: 7
row_samples:
- - Chemical Manufacturing
  - Production of the API Starting Material
  - Introduction of the API Starting Material into process
  - Production of Intermediate(s)
  - Isolation and purification
  - Physical processing, and packaging
- - API derived from animal sources
  - Collection of organ, fluid, or tissue
  - Cutting, mixing, and/or initial processing
  - Introduction of the API Starting Material into process
  - Isolation and purification
  - Physical processing, and packaging
- - API extracted from plant sources
  - Collection of plant
  - Cutting and initial extraction(s)
  - Introduction of the API Starting Material into process
  - Isolation and purification
  - Physical processing, and packaging
notes:
- Increasing GMP requirements
shading_reconstructed: false
note: Grey shading in the source PDF may not be recoverable from text layer.
```
