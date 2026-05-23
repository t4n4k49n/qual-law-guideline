# RUN: 20260523-093052469_feat-special-structure-global-gate

## 目的

text2ir 出力に残った表・図・フォーム・チェックリスト系の特殊構造を全体監査し、promotion/release 時に未解決なら通過させないゲートを追加する。

## 入力

- 指示: `out/administrators-memos/20260523.........問題発展型特殊パーサー/102.全体特殊構造ゲート/codex_special_structure_global_gate_prompt.md`
- 候補レビュー: `out/administrators-memos/20260523.........問題発展型特殊パーサー/101.特殊パーサー候補レビュー/special_parser_candidates_review.md`
- 実監査対象:
  - `data/human-readable/who/WHO_LBM_3rd.txt`
  - `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`
  - `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt`
  - `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt`

## 実装

- `src/qai_text2ir/special_structure_audit.py` を追加。
  - source 側の `Table N` / `Figure N` / `CHECKED ITEM` / `YES NO N/A COMMENTS` / 固定幅候補を検出。
  - IR 側の `table` / `table_header` / `table_row` / `figure` / `preformatted` / `note` を集計。
  - `possible_table` / `possible_form` / `possible_plaintext_table_not_structured` と、通常ノード内に残った表・図・チェックリスト・フォーム痕跡を未解決ブロックとして列挙。
  - `SPECIAL_STRUCTURE_AUDIT.json` と `SPECIAL_STRUCTURE_AUDIT.md` を出力。
- `src/qai_text2ir/goal_check.py` を更新。
  - 通常モードでは未解決特殊構造を warning。
  - `promotion` / `release` モードでは `special_structure_unresolved` error として失敗。
- `tests/test_special_structure_audit.py` を追加。
  - WHO LBM 3rd / PIC/S Annex 1 / PIC/S Annex 2A / PIC/S Part II 相当の fixture 名で、表・図・チェックリストが通常テキストに残るケースを回帰テスト化。

## 生成物

- `runs/20260523-093052469_feat-special-structure-global-gate/SPECIAL_STRUCTURE_AUDIT.json`
- `runs/20260523-093052469_feat-special-structure-global-gate/SPECIAL_STRUCTURE_AUDIT.md`
- `out/20260523-093052469_feat-special-structure-global-gate/bundles/`
- `out/20260523-093052469_feat-special-structure-global-gate/SPECIAL_STRUCTURE_AUDIT.json`
- `out/20260523-093052469_feat-special-structure-global-gate/SPECIAL_STRUCTURE_AUDIT.md`

## 監査結果

現行 text2ir 出力に対する全体特殊構造監査は `warn`。promotion/release では同じ未解決ブロックが gate 失敗になる。

| doc_id | source_tables | source_figures | generated_tables | generated_rows | generated_figures | unresolved_special_blocks | status |
|---|---:|---:|---:|---:|---:|---:|---|
| pics_annex1 | 6 | 0 | 0 | 0 | 0 | 14 | warn |
| pics_annex2a | 1 | 2 | 0 | 0 | 0 | 8 | warn |
| pics_part2 | 2 | 0 | 0 | 0 | 0 | 3 | warn |
| who_lbm_3rd | 18 | 12 | 0 | 0 | 0 | 43 | warn |

詳細は `SPECIAL_STRUCTURE_AUDIT.md` を参照。

## 実行コマンド

```powershell
git switch -c feat/special-structure-global-gate
$env:PYTHONPATH='src'; python -m qai_text2ir.cli --input data\human-readable\who\WHO_LBM_3rd.txt --out-dir out\20260523-093052469_feat-special-structure-global-gate\bundles\who_lbm_3rd --doc-id who_lbm_3rd --title "WHO Laboratory Biosafety Manual 3rd" --short-title "WHO LBM 3rd" --jurisdiction WHO --language en --family WHO_LBM --who-publication-id WHO_CDS_CSR_LYO_2004_11 --source-url https://iris.who.int/handle/10665/42981 --retrieved-at 2026-05-23
$env:PYTHONPATH='src'; python -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt --out-dir out\20260523-093052469_feat-special-structure-global-gate\bundles\pics_annex1 --doc-id pics_annex1 --title "PIC/S Annex 1" --short-title "PIC/S Annex 1" --jurisdiction PIC/S --language en --family PIC/S --pics-doc-id PE009-17_ANNEX1 --parser-profile src\qai_text2ir\profiles\pics_annex1_default_v2.yaml --source-url https://picscheme.org --retrieved-at 2026-05-23
$env:PYTHONPATH='src'; python -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_annex2a_2023-08-25_en.txt --out-dir out\20260523-093052469_feat-special-structure-global-gate\bundles\pics_annex2a --doc-id pics_annex2a --title "PIC/S Annex 2A" --short-title "PIC/S Annex 2A" --jurisdiction PIC/S --language en --family PIC/S --pics-doc-id PE009-17_ANNEX2A --parser-profile src\qai_text2ir\profiles\pics_annex2a_default_v1.yaml --source-url https://picscheme.org --retrieved-at 2026-05-23
$env:PYTHONPATH='src'; python -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_part2_2023-08-25_en.txt --out-dir out\20260523-093052469_feat-special-structure-global-gate\bundles\pics_part2 --doc-id pics_part2 --title "PIC/S Part II" --short-title "PIC/S Part II" --jurisdiction PIC/S --language en --family PIC/S --pics-doc-id PE009-17_PART2 --parser-profile src\qai_text2ir\profiles\pics_part2_default_v1.yaml --source-url https://picscheme.org --retrieved-at 2026-05-23
$env:PYTHONPATH='src'; python -m qai_text2ir.special_structure_audit --run-out-dir out\20260523-093052469_feat-special-structure-global-gate\bundles --mode normal --out-dir out\20260523-093052469_feat-special-structure-global-gate
python -m pytest tests/test_special_structure_audit.py -q
python -m pytest tests/test_text2ir_audit_report.py tests/test_text2ir_goal_check.py tests/test_table_note_inventory.py tests/test_special_structure_audit.py -q
python -m pytest -q
```

## 検証結果

- `python -m pytest tests/test_special_structure_audit.py -q`: 6 passed
- `python -m pytest tests/test_text2ir_audit_report.py tests/test_text2ir_goal_check.py tests/test_table_note_inventory.py tests/test_special_structure_audit.py -q`: 18 passed
- `python -m pytest -q`: 175 passed, 1 skipped
