# WHO LBM 3rd normalized run v9

- run_id: `20260601-004103866_run-normalized-who-lbm-3rd-v9`
- branch: `run/normalized-who-lbm-3rd-v9`
- target: `who_lbm_3rd_2004_9241546506`
- source URL: `https://www.who.int/publications/i/item/9241546506`
- input: `data/human-readable/who/WHO_LBM_3rd.txt`
- promotion candidate: `runs/20260601-004103866_run-normalized-who-lbm-3rd-v9/promotion_candidate/`
- normalized promotion: not performed in this parent PR

## Context

PR #242 merged the WHO LBM-specific fix for inline table ordering. This normalized run regenerates the WHO LBM 3rd candidate from current `main` after that fix.

The previous rejected candidate placed text between tables in the wrong visible order. This run therefore checks table/text reassembly explicitly, especially Chapter 1 Table 1, Table 2, and Table 3.

## Generation

```powershell
$env:PYTHONPATH='src'
python -m qai_text2ir.cli bundle --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir runs/20260601-004103866_run-normalized-who-lbm-3rd-v9/promotion_candidate --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory Biosafety Manual, 3rd ed." --short-title "WHO LBM 3rd" --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at 2026-05-23 --jurisdiction WHO --language en --family WHO_LBM --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml --strict --write-manifest --overwrite-manifest
```

Generated files:

- `promotion_candidate/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`
- `promotion_candidate/who_lbm_3rd_2004_9241546506.parser_profile.yaml`
- `promotion_candidate/who_lbm_3rd_2004_9241546506.regdoc_profile.yaml`
- `promotion_candidate/who_lbm_3rd_2004_9241546506.meta.yaml`
- `promotion_candidate/manifest.yaml`

`manifest.yaml` was adjusted to remove the local absolute script path and to use this run_id.

## Environment

- Python: `3.11.6`
- PyYAML: `6.0.2`
- typer: `0.24.0`
- lxml: `6.0.2`
- parser profile: `who_lbm_3rd_default_v4`
- IR schema: `qai.regdoc_ir.v4`

`core.hooksPath` was configured with `.githooks`. The helper script resolves this workspace to its real path and hits Git safe.directory protection, so the same setting was applied from the working tree with `git -c safe.directory=E:/GitHub/qual-law-guideline config core.hooksPath .githooks`.

## Validation

- `python -m pytest tests/test_who_lbm_general_tables.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_v3_skip_blocks.py tests/test_who_lbm_v2_drop_toc_and_annex_dedupe.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_chap8_survey_parser.py tests/test_text2ir_who_lbm_3rd.py -q`
  - `32 passed`
- `python -m qai_text2ir.goal_check --mode promotion`
  - `PASS`
  - nodes: `2023`
  - source span coverage: `1.0`
  - warnings: `none`
- `python -m qai_text2ir.special_structure_audit --mode promotion`
  - `pass`
  - source_tables: `18`
  - generated_tables: `18`
  - generated_rows: `1017`
  - generated_figures: `12`
  - unresolved_special_blocks: `0`
- `python tools/check_ir_structure.py runs/20260601-004103866_run-normalized-who-lbm-3rd-v9/promotion_candidate`
  - `[OK] no structure problems found`
- `rg -n "C:\\Users\\|\t|[ ]$" runs/20260601-004103866_run-normalized-who-lbm-3rd-v9`
  - no matches

Artifacts:

- `GOAL_CHECK.md`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `TABLE_RECONSTRUCTION_CHECK.md`
- `SAMPLE_EXTRACT.md`

## Manual and reconstruction checks

Confirmed in `TABLE_RECONSTRUCTION_CHECK.md`:

- `cha1.sec1.text` stops before Table 1.
- Chapter 1 child order is:
  - `cha1.sec1.tbl1`
  - `cha1.sec1.stmt1`
  - `cha1.sec1.tbl2`
  - `cha1.sec1.i1`
  - `cha1.sec1.i2`
  - `cha1.sec1.i3`
  - `cha1.sec1.i4`
  - `cha1.sec1.stmt2`
  - `cha1.sec1.tbl3`
  - `cha1.sec1.stmt3`
- `Laboratory facilities are designated as basic ...` is after Table 1.
- `The assignment of an agent ...` is after Table 2 and before Table 3.
- `Thus, the assignment ...` is after Table 3.
- No parent node has reversed source-line order among `table` / `statement` / `item` / `subitem` / `figure` children.
- Table A4-2:
  - row count: `22`
  - first row: `Faulty design or construction |  | `
  - merged-cell/note-sensitive rows for domestic refrigerator and flame photometer are present.
- Table A5-1:
  - row count: `701`
  - first row starts with `Acetaldehyde`
  - Index text such as `alarms 21, 60` is not mixed into A5 table rows.
- Unnumbered headings are present:
  - `Access`
  - `Personal protection`
  - `Infectious materials`
  - `Chemicals and radioactive substances`
- Known line-break/space-sensitive phrases are present:
  - `The Laboratory biosafety manual has`
  - `Wear gloves to protect skin against chemical effects of detergents`

## Deep sample

Extracted by:

```powershell
python tools/extract_ir_sample.py --ir runs/20260601-004103866_run-normalized-who-lbm-3rd-v9/promotion_candidate/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml --nid ann5.tbla5_1.tblh.tblr1 --output runs/20260601-004103866_run-normalized-who-lbm-3rd-v9/SAMPLE_EXTRACT.md
```

Target path:

- `root` document
- `ann5` annex: `Chemicals: hazards and precautions`
- `ann5.tbla5_1` table: `Table A5-1. Chemicals: hazards and precautions`
- `ann5.tbla5_1.tblh` table_header: `Chemical | Physical properties | Health hazards | Fire hazards | Safety precautions | Incompatible chemicals / other hazards`
- `ann5.tbla5_1.tblh.tblr1` table_row: `Acetaldehyde | Colourless liquid or | Mild eye and | Extremely flammable; | No open flames, no | Can form explosive`

## Notes

- This is the parent review PR only.
- `data/normalized/` was not changed.
- Promotion to `data/normalized/` must be done in a child PR after parent approval.
