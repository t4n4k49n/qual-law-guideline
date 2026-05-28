# RUN: PIC/S Part I table / warning review

- run_id: `20260529-033231419_feat-pics-part1-table-warning-review-v1`
- branch: `feat-pics-part1-table-warning-review-v1`
- target: `pics_pe00917_part1_20230825`
- input: `data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt`
- parser profile: `src/qai_text2ir/profiles/pics_part1_default_v3.yaml`
- output bundle before fix: `out/20260529-033231419_feat-pics-part1-table-warning-review-v1/pics_pe00917_part1_20230825/`
- output bundle after fix: `out/20260529-033231419_feat-pics-part1-table-warning-review-v1/pics_pe00917_part1_20230825_after_fix/`

## Purpose

PIC/S Part I normalized run preparation. Confirm table and warning handling before creating a strict normalized run, and fix any parser/profile issues found by review.

## Finding

Part I has no body tables or figures requiring table reconstruction. The only `Table` occurrences in source are table-of-contents lines, and the only figure-like text is the prose phrase `organisation chart`.

The review did find one Note/context issue:

- Source lines 2520-2525 contain the page footer/header and `CHAPTER 7`.
- Source lines 2540-2544 contain the Chapter 7 principle note.
- Before the fix, line 2521 `Chapter 7     Outsourced activities` remained in `cha6.p6_41.text`.
- Before the fix, the Chapter 7 note was attached as `cha6.p6_41.not1`.

## Corrective Action

- Updated `src/qai_text2ir/profiles/pics_part1_default_v3.yaml` to drop standalone mixed-case running headers such as `Chapter 7     Outsourced activities`.
- Updated note extraction in `src/qai_text2ir/text_parser.py` so a stale `last_attachable_node` is used only when it is still in the current parser stack.
- Added a regression test proving that a note immediately after a chapter transition attaches to the new chapter, not the previous paragraph.

## Checks

- Generated Part I bundle with `--strict`: pass.
- Promotion goal check after fix: pass.
- Promotion goal warnings after fix: none.
- Special structure audit after fix: pass.
- Source tables: 0.
- Source figures: 0.
- Generated tables: 0.
- Generated rows: 0.
- Generated figures: 0.
- Unresolved special blocks: 0.
- IR warning metadata scan after fix: none.
- Part I focused tests: `9 passed`.
- Full test suite: `251 passed, 1 skipped`.

## Note Review Result

- Note count: 2.
- `cha4.p4_20.not1`: correctly attached to paragraph `4.20`.
- `cha7.not1`: correctly attached to Chapter 7 after the fix.
- `cha6.p6_41`: no longer contains the Chapter 7 running header after the fix.

## Review Sample

- Sample file: `runs/20260529-033231419_feat-pics-part1-table-warning-review-v1/SAMPLE_EXTRACT.md`
- Target nid: `cha7.not1`
- Reason: confirms the corrected Chapter 7 note attachment.

## Next

After this PR is merged, create a normalized run for PIC/S Part I.
