# RUN: 20260527-105034029_docs-readiness-10-12-13-rerun

## Purpose

`docs/NORMALIZATION_PLAN_10_12_13.md` に基づき、10 EU GMP、12 PIC/S、13 WHO LBM 3rd の既存GOAL pass文書を現行mainで再生成し、正式な正規化RUNへ進めるためのreadinessを確認する。

## Branch

- `docs/readiness-10-12-13-rerun`

## Inputs

- `README.md`
- `local_notes/TODO.md`
- `local_notes/KNOWLEDGE.md`
- `docs/NORMALIZATION_PLAN_10_12_13.md`
- `runs/20260522-053004_text2ir-goal-gap-longrun/GOAL_CHECK_RESULTS.md`
- `runs/20260522-053004_text2ir-goal-gap-longrun/TEXT2IR_AUDIT_REPORT.md`
- `runs/20260522-053004_text2ir-goal-gap-longrun/text2ir_audit_report.json`

## Actions

- 新規ブランチを作成した。
- `runs/20260527-105034029_docs-readiness-10-12-13-rerun/` と `out/20260527-105034029_docs-readiness-10-12-13-rerun/` を作成した。
- 代表9文書を `qai_text2ir.cli bundle --strict` で現行main再生成した。
- 単体8文書は再生成、GOAL、promotion GOAL、横断auditまで完了した。
- PIC/S Annexes refined は strict fail として記録した。
- `TEXT2IR_AUDIT_REPORT.md` と `text2ir_audit_report.json` を `runs/` にコピーした。
- `READINESS_10_12_13.md` を作成した。

## Outputs

- `out/20260527-105034029_docs-readiness-10-12-13-rerun/`
- `runs/20260527-105034029_docs-readiness-10-12-13-rerun/TEXT2IR_AUDIT_REPORT.md`
- `runs/20260527-105034029_docs-readiness-10-12-13-rerun/text2ir_audit_report.json`
- `runs/20260527-105034029_docs-readiness-10-12-13-rerun/READINESS_10_12_13.md`

## Results

- GOAL pass: 8
- GOAL fail: 1
- promotion GOAL pass: 8
- `meta_family_missing`: resolved for the 8 generated single-document bundles.
- total nodes in passed bundles: 3147
- total tables in passed bundles: 23
- total table rows in passed bundles: 258
- total notes in passed bundles: 37
- total possible_table: 0

## Decision

次の正規化RUNの第一候補は `eu_gmp_vol4_chap1_20130131` とする。第二候補は `pics_pe00917_annex11_20230825`。

PIC/S Annex 1、Annex 2A、Part II、WHO LBM 3rd はreadyだが、表・注記または対象範囲のレビューを挟む。PIC/S Annexes refinedは現行mainでstrict failのため、正式化初手から外す。

## Verification

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle ... --strict
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir <doc_dir> --doc-id <doc_id> --format markdown
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir <doc_dir> --doc-id <doc_id> --format json
.\.venv\Scripts\python.exe -m qai_text2ir.audit_report --run-out-dir out/20260527-105034029_docs-readiness-10-12-13-rerun --format markdown
.\.venv\Scripts\python.exe -m qai_text2ir.audit_report --run-out-dir out/20260527-105034029_docs-readiness-10-12-13-rerun --format json
```

No `data/normalized/` changes were made.
