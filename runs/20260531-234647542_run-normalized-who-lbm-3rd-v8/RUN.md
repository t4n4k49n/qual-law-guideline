# WHO LBM 3rd normalized run v8

- run_id: `20260531-234647542_run-normalized-who-lbm-3rd-v8`
- branch: `run/normalized-who-lbm-3rd-v8`
- doc_id: `who_lbm_3rd_2004_9241546506`
- source: `data/human-readable/who/WHO_LBM_3rd.txt`
- source_url: `https://www.who.int/publications/i/item/9241546506`
- parser_profile: `src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml`

## 実行内容

WHO Laboratory Biosafety Manual, 3rd ed. の正規化候補を `runs/20260531-234647542_run-normalized-who-lbm-3rd-v8/promotion_candidate/` に生成した。

このRUNは親PR用であり、`data/normalized/` への昇格は含めない。

## 生成コマンド

```powershell
$env:PYTHONPATH='src'; python -m qai_text2ir.cli bundle --input data/human-readable/who/WHO_LBM_3rd.txt --out-dir runs/20260531-234647542_run-normalized-who-lbm-3rd-v8/promotion_candidate --doc-id who_lbm_3rd_2004_9241546506 --title "WHO Laboratory Biosafety Manual, 3rd ed." --short-title "WHO LBM 3rd" --doc-type guideline --source-url "https://www.who.int/publications/i/item/9241546506" --source-format pdf --retrieved-at 2026-05-23 --jurisdiction WHO --language en --family WHO_LBM --parser-profile src/qai_text2ir/profiles/who_lbm_3rd_default_v4.yaml --strict --write-manifest --overwrite-manifest
```

## 検証結果

- `python -m pytest tests/test_who_lbm_general_tables.py tests/test_who_lbm_v4_skip_toc_and_annex_heading.py tests/test_who_lbm_v3_skip_blocks.py tests/test_who_lbm_v2_drop_toc_and_annex_dedupe.py tests/test_who_lbm_heading_merge.py tests/test_who_lbm_chap8_survey_parser.py tests/test_text2ir_who_lbm_3rd.py -q`
  - `31 passed`
- `qai_text2ir.goal_check --mode promotion`
  - `PASS`
  - schema: `qai.regdoc_ir.v4`
  - nodes: `2009`
  - source span coverage: `1.0`
  - warnings: `none`
- `qai_text2ir.special_structure_audit --mode promotion`
  - `pass`
  - source_tables: `18`
  - generated_tables: `18`
  - generated_rows: `1017`
  - generated_figures: `12`
  - unresolved_special_blocks: `0`
- `python tools/check_ir_structure.py runs/20260531-234647542_run-normalized-who-lbm-3rd-v8/promotion_candidate`
  - `[OK] no structure problems found`

## 目検・再結合チェック

`TABLE_RECONSTRUCTION_CHECK.md` に、表・heading・不要空白の二重チェック結果を記録した。

- Table A4-2 row count: `22`
- Table A4-2 `Faulty design or construction`: `PASS`
- Table A4-2 `Explosion in domestic-`: `Dangerous chemical not` / `• Store low-flashpoint solvents` で復元
- Table A4-2 `Fire in flame`: `Incorrect reassembly of` / `• Train and supervise staff.` で復元
- Table A5-1 row count: `701`
- Table A5-1 `Acetaldehyde`: `Can form explosive` を保持
- Table A5-1 に索引 `alarms 21, 60` の巻き込みなし
- Chapter 9 `The Laboratory biosafety manual has` を保持し、`The  has` はなし
- `Access` / `Personal protection` / `Infectious materials` / `Chemicals and radioactive substances` heading を確認
- 個人環境の絶対パス、tab、行末スペースなし

## レビュー成果物

- `GOAL_CHECK.md`
- `SPECIAL_STRUCTURE_AUDIT.md`
- `SAMPLE_EXTRACT.md`
- `TABLE_RECONSTRUCTION_CHECK.md`

## 昇格

親PR承認後にのみ、子PRで `promotion_candidate/` から `data/normalized/who_lbm_3rd_2004_9241546506/` へ複写する。
