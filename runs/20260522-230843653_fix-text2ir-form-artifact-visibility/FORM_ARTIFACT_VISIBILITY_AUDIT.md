# FORM ARTIFACT VISIBILITY AUDIT

## Finding

The original user-visible failure was that WHO LBM form rows appeared as ordinary review text, for example:

```text
preformatted: Information on sign accurate and current | [ ] [ ] [ ]
preformatted: Sign legible and not defaced | [ ] [ ] [ ]
preformatted: Table 5. Basic Laboratory ... CHECKED ITEM ... [ ] [ ] [ ]
```

This run treats that as a visibility failure, not as a cosmetic glyph problem.

## After Audit

| doc_id | literal PUA nodes | default-visible form leakage | candidate export leakage | form_artifact nodes | long form_artifact.text |
|---|---:|---:|---:|---:|---:|
| `eu_gmp_vol4_chap1_20130131` | 0 | 0 | 0 | 0 | 0 |
| `pics_pe00917_annex11_20230825` | 0 | 0 | 0 | 0 | 0 |
| `pics_pe00917_annex15_20230825` | 0 | 0 | 0 | 0 | 0 |
| `pics_pe00917_annex1_20230825` | 0 | 0 | 0 | 0 | 0 |
| `pics_pe00917_annex2a_20230825` | 0 | 0 | 0 | 0 | 0 |
| `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | 0 | 0 | 0 | 0 | 0 |
| `pics_pe00917_part1_20230825` | 0 | 0 | 0 | 0 | 0 |
| `pics_pe00917_part2_20230825` | 0 | 0 | 0 | 0 | 0 |
| `who_lbm_3rd_2004_9241546506` | 0 | 0 | 0 | 3 | 0 |

## WHO LBM Detail

The regenerated WHO LBM bundle keeps three form artifacts as hidden reference nodes:

| nid | kind | kind_raw | text |
|---|---|---|---|
| `cha8.i5.si1` | `preformatted` | `form_artifact` | `Reference form artifact: Information on sign accurate and current. Hidden from default checklist/review display.` |
| `cha8.i5.si2` | `preformatted` | `form_artifact` | `Reference form artifact: Sign legible and not defaced. Hidden from default checklist/review display.` |
| `cha8.i5.art1` | `preformatted` | `form_artifact` | `Reference form artifact: Table 5. Basic Laboratory - Biosafety Level 1: laboratory safety survey Location. Hidden from default checklist/review display.` |

Each has:

- `tags: [form_artifact, not_selectable, reference_only, sanitized_layout_artifact]`
- `visibility.default_review: hidden`
- `visibility.dq_gmp_checklist: hidden`
- `visibility.search_default: hidden`

`cha8.i5.art1` retains the raw Table 5-7 form block only in `data.raw_text_escaped`; `Laboratory biosecurity` is not included in that raw artifact payload.

## Interpretation

- The problematic form rows are no longer default-visible candidates.
- The review UI folders under `out/*_review_ui/` were refreshed with the regenerated YAML.
- Raw trace text is retained only as non-default-rendered artifact payload.
