# WHO LBM General Tables Report

## Summary

- doc_id: `who_lbm_3rd_2004_9241546506`
- source: `data/human-readable/who/WHO_LBM_3rd.txt`
- output bundle: `out/20260523-123752346_feat-who-lbm-general-tables/after_who_lbm_v3`
- promotion gate: `PASS`
- unresolved special structures: `0`

## General WHO Tables

The `who_lbm_general_tables` parser normalized these 12 non-Chapter 8 table targets:

| Table | Caption | Status |
|---:|---|---|
| 1 | Classification of infective microorganisms by risk group | structured |
| 2 | Relation of risk groups to biosafety levels, practices and equipment | structured |
| 3 | Summary of biosafety level requirements | structured |
| 4 | Animal facility containment levels: summary of practices and safety equipment | structured |
| 8 | Selection of a biological safety cabinet (BSC), by type of protection needed | structured |
| 9 | Differences between Class I, II and III biological safety cabinets (BSCs) | structured |
| 10 | Biosafety equipment | structured |
| 11 | Personal protective equipment | structured |
| 12 | Recommended dilutions of chlorine-releasing compounds | structured |
| 13 | General rules for chemical incompatibilities | structured |
| 14 | Storage of compressed and liquefied gases | structured |
| 15 | Types and uses of fire extinguishers | structured |

## Chapter 8 Survey Tables

Chapter 8 survey/checklist tables remain handled by the dedicated `who_lbm_chap8_survey` parser:

| Table | Caption | Parser |
|---:|---|---|
| 5 | Basic Laboratory - Biosafety Level 1: laboratory safety survey | `who_lbm_chap8_survey` |
| 6 | Basic laboratory - Biosafety Level 2: laboratory safety survey | `who_lbm_chap8_survey` |
| 7 | Containment laboratory - Biosafety Level 3: laboratory safety survey | `who_lbm_chap8_survey` |

## Figures

The parser generated 12 `figure` nodes for Figure 1-12. Captions are no longer embedded in ordinary chapter/item text, and figure-like text-layer blocks such as Figure 10 are represented through the figure node payload.

## Gate Results

| Metric | Value |
|---|---:|
| generated tables | 15 |
| generated table rows | 210 |
| generated figures | 12 |
| generated preformatted nodes | 0 |
| source table captions | 18 |
| source figure captions | 12 |
| unresolved special blocks | 0 |

## Notes

- Source table captions are 18 because the source includes Table 1-15 plus three Chapter 8 survey tables.
- The promotion gate reports `Errors: none` and `Warnings: none`.

