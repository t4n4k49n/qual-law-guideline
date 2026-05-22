# GOAL CHECK SUMMARY

## Command Summary

- Regenerated 9 representative text2ir bundles under `out/20260522-230843653_fix-text2ir-form-artifact-visibility/`.
- Ran `goal_check --mode promotion` for all 9 bundles.
- Ran artifact visibility audit for default-visible IR nodes and candidate-export-equivalent rows.
- Ran full test suite.

## Promotion Gate

| doc_id | promotion | literal PUA | default-visible leakage | candidate leakage | form artifacts |
|---|---|---:|---:|---:|---:|
| `eu_gmp_vol4_chap1_20130131` | PASS | 0 | 0 | 0 | 0 |
| `pics_pe00917_annex11_20230825` | PASS | 0 | 0 | 0 | 0 |
| `pics_pe00917_annex15_20230825` | PASS | 0 | 0 | 0 | 0 |
| `pics_pe00917_annex1_20230825` | PASS | 0 | 0 | 0 | 0 |
| `pics_pe00917_annex2a_20230825` | PASS | 0 | 0 | 0 | 0 |
| `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | PASS | 0 | 0 | 0 | 0 |
| `pics_pe00917_part1_20230825` | PASS | 0 | 0 | 0 | 0 |
| `pics_pe00917_part2_20230825` | PASS | 0 | 0 | 0 | 0 |
| `who_lbm_3rd_2004_9241546506` | PASS | 0 | 0 | 0 | 3 |

## Tests

```text
python -m pytest -q
171 passed, 1 skipped
```

## Final Self Review

- [x] Literal PUA glyph is zero in representative regdoc_ir YAML files.
- [x] `form_artifact` / `not_selectable` nodes are not shown in default review UI candidate visibility.
- [x] DQ/GMP checklist candidate export equivalent contains no form artifact rows.
- [x] WHO LBM `Information on sign accurate and current | [ ] [ ] [ ]` is not visible in default review UI.
- [x] WHO LBM `Sign legible and not defaced | [ ] [ ] [ ]` is not visible in default review UI.
- [x] WHO LBM Table 5-7 giant form body is not stored as long visible `text`.
- [x] `form_artifact.text` is short summary only and does not contain checkbox clusters.
- [x] WHO LBM prose before Table 5 is preserved.
- [x] `Laboratory biosecurity` is preserved in the regression fixture.
- [x] Promotion `goal_check` fails if default-visible form leakage returns.
- [x] Tests cover sanitizer behavior through parser output, visibility filtering, WHO LBM fixture, promotion gate, and false positives at candidate visibility level.
- [x] Representative docs regenerate and pass the strengthened promotion gate.

## Remaining Risk

This run does not create a separate explicit `--include-artifacts` UI section. It enforces the default side: artifacts are retained in IR for traceability but hidden from normal review/candidate surfaces.
