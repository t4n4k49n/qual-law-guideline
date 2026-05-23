# RUN: 20260523-130131075_feat-pics-annexes-bundle-specials

## Scope

- Prompt: `out/administrators-memos/20260523.........問題発展型特殊パーサー/107.PICS_combined_annexes特殊構造/codex_pics_annexes_bundle_specials_prompt.md`
- Target document: `pics_pe00917_annexes_20230825_refined_v3_extends_trace`
- Source: `data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt`
- Branch: `feat/pics-annexes-bundle-specials`

## Implemented

- Reused existing Annex 1 table parser results: `pics_annex1_tables`.
- Reused existing Annex 2A table/figure parser results: `pics_annex2a_table1`, `pics_annex2a_flow_figures`.
- Added `pics_annexes_bundle_specials` postprocessor for:
  - Annex 2B Table 1: manufacturing activities table, 7 rows, 7 notes.
  - Annex 20 Figure 1: QRM process figure, informative role, ordered process labels.
- Updated `pics_annexes_default_v3` to:
  - enable the bundle special parser,
  - recognize `ANNEX 20*`,
  - allow `figure` as a structural child under annexes.

## Generated Outputs

- BEFORE bundle: `out/20260523-130131075_feat-pics-annexes-bundle-specials/before_pics_annexes/`
- AFTER bundle: `out/20260523-130131075_feat-pics-annexes-bundle-specials/after_pics_annexes_v3/`
- Goal check JSON: `out/20260523-130131075_feat-pics-annexes-bundle-specials/PICS_ANNEXES_BUNDLE_SPECIALS_REPORT.json`
- Goal check Markdown: `out/20260523-130131075_feat-pics-annexes-bundle-specials/GOAL_CHECK.md`
- Special structure audit JSON: `out/20260523-130131075_feat-pics-annexes-bundle-specials/SPECIAL_STRUCTURE_AUDIT.json`

## Result

- Target structures are now emitted as structured IR nodes, not ordinary text.
- Generated counts after implementation:
  - tables: 8
  - table rows: 48
  - figures: 4
  - notes: 27
- `verify_document`: pass
- Source span coverage: 1.0
- Qualitycheck warning remains for unrelated Annex 20 section 7.2 page-number text.

## Deferred Findings

The promotion goal check still reports 8 unresolved special-structure candidates outside this prompt's target scope:

- Annex 3: `ann3.sec3.si4`, fixed-width radionuclide generators block.
- Annex 7: `ann7.sec16`, form-control style text.
- Annex 14: `ann14.sec10`, `ann14.sec2_2.p2_5`, `ann14.sec1_3`, `ann14.sec2_3`, fixed-width blocks.
- Annex 19: `ann19.sec10.p10_3`, form-control ellipsis.
- Annex 20: `ann20.sec7_2.ii.si14`, form-control/page-number text in section 7.2.

## Validation

- `python -m pytest tests\test_pics_annexes_bundle_specials.py -q`
- `python -m pytest tests\test_pics_annexes_bundle_specials.py tests\test_pics_annex1_tables.py tests\test_pics_annex2a_structures.py tests\test_pics_annexes_refine_v2.py tests\test_pics_annexes_refine_v3_fallback.py tests\test_pics_annexes_full_profile_v1.py tests\test_special_structure_audit.py -q`
- `python -m pytest tests\test_pics_annexes_bundle_specials.py tests\test_special_structure_audit.py -q`
