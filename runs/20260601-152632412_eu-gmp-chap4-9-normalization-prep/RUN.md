# EU GMP Vol.4 Chapter 4-9 Normalization Preparation

- run_id: `20260601-152632412_eu-gmp-chap4-9-normalization-prep`
- branch: `feat/eu-gmp-chap4-9-normalization-prep`
- scope: EU GMP Vol.4 Chapter 4-9 normalization preparation
- status: prepared

## Inputs

| chapter | source text | trial doc_id | source URL |
|---:|---|---|---|
| 4 | `data/human-readable/eu_gmp/vol4/source_texts/chapter4_01-2011_en.txt` | `eu_gmp_vol4_chap4_20110101` | `https://health.ec.europa.eu/document/download/104b3eb8-81a7-4858-9419-cb06562adb66_en?filename=chapter4_01-2011_en.pdf` |
| 5 | `data/human-readable/eu_gmp/vol4/source_texts/chapter_5.txt` | `eu_gmp_vol4_chap5_20150123` | `https://health.ec.europa.eu/document/download/4a1fdb4f-6f6f-49c4-b264-8056e5bbe078_en?filename=chapter_5.pdf` |
| 6 | `data/human-readable/eu_gmp/vol4/source_texts/2014-11_vol4_chapter_6.txt` | `eu_gmp_vol4_chap6_20140328` | `https://health.ec.europa.eu/document/download/c74c8720-27bf-4252-808f-d65a206a90bb_en?filename=2014-11_vol4_chapter_6.pdf` |
| 7 | `data/human-readable/eu_gmp/vol4/source_texts/vol4-chap7_2012-06_en.txt` | `eu_gmp_vol4_chap7_20120628` | `https://health.ec.europa.eu/document/download/58b5106a-cf6f-4352-9dca-1caf5d27d97e_en?filename=vol4-chap7_2012-06_en.pdf` |
| 8 | `data/human-readable/eu_gmp/vol4/source_texts/2014-08_gmp_chap8.txt` | `eu_gmp_vol4_chap8_20140813` | `https://health.ec.europa.eu/document/download/b1eb2292-cb0d-4e3f-aea9-e3fe79faf6e3_en?filename=2014-08_gmp_chap8.pdf` |
| 9 | `data/human-readable/eu_gmp/vol4/source_texts/cap9_en.txt` | `eu_gmp_vol4_chap9_undated` | `https://health.ec.europa.eu/document/download/07195808-d02e-4d7a-b8f4-f84a83278b62_en?filename=cap9_en.pdf` |

Note: Chapter 9 source text does not expose a source date in the local text, so the preparation doc_id uses `undated`. Confirm the official date before a normalized RUN promotion candidate is finalized.

## Preparation Output

- Parser profile: `src/qai_text2ir/profiles/eu_gmp_chap4_9_default_v1.yaml`
- Profile coverage test: `tests/test_text2ir_eu_gmp_chap1.py::test_eu_gmp_chapter4_to_9_profile_preparation_samples`
- Trial candidates:
  - `runs/20260601-152632412_eu-gmp-chap4-9-normalization-prep/trial_candidates_r2/`
- Audit logs:
  - `runs/20260601-152632412_eu-gmp-chap4-9-normalization-prep/audit_r2/`

`trial_candidates_r2/` and `audit_r2/` are the reviewed outputs after suppressing heading false positives found during manual heading inspection.

## Required Checks

- Unnumbered headings:
  - Added Chapter 4-9 unnumbered section markers for `Principle`, `General`, Chapter 4 documentation subsections, Chapter 5 production subsections, Chapter 6 QC subsections, Chapter 7 contract subsections, and Chapter 8 complaint/recall subsections.
  - Restricted chapter marker matching to `Chapter 4`-`Chapter 9` plus the Chapter 9 uppercase source heading, preventing references such as `Chapter 1` and `Chapter 7` from becoming structural chapters.
  - Manually listed chapter/section headings from `trial_candidates_r2`; no heading was absorbed into the prior section text.
- Whitespace cleanup:
  - Verified generated `heading` and `text` fields have no leading/trailing whitespace, tabs, embedded newlines, or repeated spaces.
  - Added profile drops for known source header/footer and Chapter 5 footnote-body noise.
- Tables and merged cells:
  - `special_structure_audit` reports source tables `0`, generated tables `0`, and unresolved blocks `0` for Chapters 4-9.
  - No merged-cell replication was needed in this preparation set.
- Table notes and ordinary notes:
  - No table notes were detected.
  - Ordinary notes are represented as `note` nodes: Chapter 4 has 1, Chapter 7 has 1.

## Validation

```powershell
$env:PYTHONPATH='src'; python -m pytest tests/test_text2ir_eu_gmp_chap1.py -q
```

Result: `9 passed`.

For each Chapter 4-9 trial candidate under `trial_candidates_r2/`:

```powershell
$env:PYTHONPATH='src'; python -m qai_text2ir.goal_check --bundle-dir <bundle> --doc-id <doc_id> --mode promotion --format markdown --out <audit>
$env:PYTHONPATH='src'; python -m qai_text2ir.special_structure_audit --bundle-dir <bundle> --doc-id <doc_id> --mode promotion --format markdown --out <audit>
python tools/check_ir_structure.py <bundle>
```

Result:

- `goal_check`: PASS for all 6 trial candidates.
- `special_structure_audit`: pass for all 6 trial candidates.
- `check_ir_structure`: OK for all 6 trial candidates.

## Next

- Use this preparation profile and `trial_candidates_r2/` as the starting point for the actual normalized RUN parent PR.
- Before final promotion candidate creation, confirm Chapter 9 date/source identity and decide the final doc_id.
