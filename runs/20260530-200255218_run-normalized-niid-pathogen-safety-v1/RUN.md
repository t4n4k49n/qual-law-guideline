# RUN 20260530-200255218_run-normalized-niid-pathogen-safety-v1

## Purpose

Create the parent normalized-run review candidate for `jp_niid_pathogen_safety_management_20240401`.

This run follows `docs/NORMALIZED_RUN_PLAYBOOK.md`. It changes only the promotion candidate and review artifacts; `data/normalized/` remains unchanged until parent PR approval.

## Source

- source text: `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- source PDF: `https://www.niid.go.jp/niid/images/cepr/kanrikitei/Kanrikitei3_20240401.pdf`
- doc_id: `jp_niid_pathogen_safety_management_20240401`
- promotion_candidate: `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/promotion_candidate/`

## Parser Fixes

- Added full NIID parser profile to keep body chapters and annexes in one document.
- Added full candidate visibility profile; it preserves excluded chapters in IR while hiding `cha1`, `cha5`, and `cha6` from checklist candidates.
- Enabled Japanese prose normalization for display `heading`/`text` fields.
- Removed parser-created table row item artifacts after NIID annex table promotion.
- Filled visually wrapped headings for `付表2` and `付表4`.

## Command

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt --out-dir runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/promotion_candidate --doc-id jp_niid_pathogen_safety_management_20240401 --title "国立感染症研究所病原体等安全管理規程" --short-title "NIID病原体等安全管理規程" --doc-type regulation --source-url https://www.niid.go.jp/niid/images/cepr/kanrikitei/Kanrikitei3_20240401.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_niid_pathogen_safety_management_full_v1.yaml --candidate-visibility-profile src/qai_text2ir/candidate_visibility_profiles/jp_niid_pathogen_safety_management_full_visibility_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

## Environment

- python_executable: `.venv\Scripts\python.exe`
- python_version: `3.11.6`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- tool_version: not set

## Validation

- `qai_text2ir.goal_check`: PASS
  - schema: `qai.regdoc_ir.v4`
  - nodes: 324
  - source span coverage: 1.0
  - chapter: 6
  - annex: 16
  - table: 5
  - table_row: 54
- `qai_text2ir.special_structure_audit`: PASS
  - generated_tables: 5
  - generated_rows: 54
  - unresolved_special_blocks: 0
- `tools/check_ir_structure.py`: PASS
- focused tests: `11 passed`
- display prose scan: Japanese-letter internal spaces, literal `\n`/CR artifacts, and page marker lines all 0.

## Manual Review Notes

- Root chapters are `1` through `6` once each; TOC-derived duplicates are absent.
- Root annexes preserve all 16 expected markers from `別表1` through `別表10` and `付表1-1` through `付表4`.
- `付表2`, `付表3`, `付表4`, `別表7`, and `別表10` are promoted to visual-reviewed `table_row` records.
- Raw fixed-width extraction remains in metadata fields such as `raw_lines` and `original_text_before_table_adapter` for traceability; these are not display text.
- `付表2` and `付表4` headings were checked for wrapped title continuation and normalized to full titles.

## Review Artifacts

- Goal check: `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/GOAL_CHECK.md`
- Special structure audit: `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/SPECIAL_STRUCTURE_AUDIT.md`
- Structure/table review: `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/STRUCTURE_TABLE_REVIEW.md`
- Deep sample: `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/SAMPLE_EXTRACT.md`

## Promotion Boundary

This parent PR changes only parser/profile code, the run promotion candidate, and review artifacts. It does not copy files to `data/normalized/`.

After this parent PR is approved and merged, create a child promotion PR that copies the four candidate files from `promotion_candidate/` to `data/normalized/jp_niid_pathogen_safety_management_20240401/`.

## Promotion Preparation

- Parent PR: `#223`
- Parent merge commit: `925652b6dfc6e383479cf125934f77395fdd0502`
- Promotion branch: `promote/niid-pathogen-safety-v1`
- Promotion source: `runs/20260530-200255218_run-normalized-niid-pathogen-safety-v1/promotion_candidate/`
- Destination: `data/normalized/jp_niid_pathogen_safety_management_20240401/`
- Copied files:
  - `jp_niid_pathogen_safety_management_20240401.regdoc_ir.yaml`
  - `jp_niid_pathogen_safety_management_20240401.parser_profile.yaml`
  - `jp_niid_pathogen_safety_management_20240401.regdoc_profile.yaml`
  - `jp_niid_pathogen_safety_management_20240401.meta.yaml`
- SHA-256 match between `promotion_candidate/` and `data/normalized/`: confirmed.
- Promotion goal check on `data/normalized/jp_niid_pathogen_safety_management_20240401/`: pass. `manifest.yaml` is not copied to `data/normalized/` by design.
- IR structure check on `data/normalized/jp_niid_pathogen_safety_management_20240401/`: pass.
