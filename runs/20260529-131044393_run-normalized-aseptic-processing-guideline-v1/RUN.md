# RUN

- run_id: `20260529-131044393_run-normalized-aseptic-processing-guideline-v1`
- branch: `run/normalized-aseptic-processing-guideline-v1`
- base_commit: `f1190136b2568fbc9fc0caec9806197d72280c71`
- target: 無菌操作法による無菌医薬品の製造に関する指針
- doc_id: `jp_pmda_aseptic_processing_guideline_20110420`
- source_pdf: `https://www.pmda.go.jp/files/000206144.pdf`
- source_text: `data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt`
- promotion_candidate: `runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/promotion_candidate/`

## Purpose

PR #220 で承認された無菌操作法指針の heading/table 目検修正を反映し、`data/normalized/` 昇格前の親PR用 promotion candidate を作成する。

この親PRでは `data/normalized/` を変更しない。正式版への複写は親PR承認後の子PRで実施する。

## Command

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt --out-dir runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/promotion_candidate --doc-id jp_pmda_aseptic_processing_guideline_20110420 --title "無菌操作法による無菌医薬品の製造に関する指針" --short-title "無菌操作法指針" --doc-type guideline --source-url https://www.pmda.go.jp/files/000206144.pdf --source-format pdf --retrieved-at 2026-02-18 --parser-profile src/qai_text2ir/profiles/jp_pmda_aseptic_processing_guideline_v1.yaml --jurisdiction JP --language ja --family JP_GUIDELINE --strict --write-manifest --overwrite-manifest
```

## Environment

- python_executable: `.venv\Scripts\python.exe`
- python_version: `3.11.6`
- lxml: `6.0.2`
- PyYAML: `6.0.3`
- typer: `0.24.0`
- tool_version: not set

## Outputs

- `promotion_candidate/jp_pmda_aseptic_processing_guideline_20110420.regdoc_ir.yaml`
- `promotion_candidate/jp_pmda_aseptic_processing_guideline_20110420.parser_profile.yaml`
- `promotion_candidate/jp_pmda_aseptic_processing_guideline_20110420.regdoc_profile.yaml`
- `promotion_candidate/jp_pmda_aseptic_processing_guideline_20110420.meta.yaml`
- `promotion_candidate/manifest.yaml`
- `GOAL_CHECK.md`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `SAMPLE_EXTRACT.md`
- `HEADING_TABLE_REVIEW.md`

## Validation

- `qai_text2ir.goal_check`: PASS
  - schema: `qai.regdoc_ir.v4`
  - nodes: 436
  - source span coverage: 1.0
  - table: 3
  - table_header: 3
  - table_row: 12
- `qai_text2ir.special_structure_audit`: PASS
  - generated_tables: 3
  - generated_rows: 12
  - unresolved_special_blocks: 0
- focused tests: `7 passed`
- full tests: `253 passed, 1 skipped`

## Manual Review Notes

- Heading:
  - 章見出し、節見出し、深い項目番号の親子関係を `SAMPLE_EXTRACT.md` で確認した。
  - 例: `root -> cha7 -> cha7.sec7_1 -> cha7.sec7_1.p7_1_1`
- Tables:
  - 表1、表2、表3を候補IR上で確認した。
  - 各表の `header_structure.spanning_headers` に結合ヘッダを保持した。
  - 各表のデータ行は `table_row` に昇格し、DQ GMP checklist の selectable kind に含まれる。
  - table notes は note node として保持し、note-to-cell link は deferred とした。

## Promotion Status

- Parent PR stage only.
- `data/normalized/` is intentionally unchanged in this run.
