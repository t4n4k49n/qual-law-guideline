# RUN: text2ir final GOAL gap closure

## Purpose

前回RUN `20260522-053004_text2ir-goal-gap-longrun` で残ったGAPを閉じ、`qai_text2ir` を正式候補として扱える品質へ近づける。

## Scope

- Phase 9A: `meta.doc.family` と promotion向けGOAL_CHECKの強化。
- Phase 9B以降: 表・注記の本番入力反映、profile課題サンプル確認、代表9文書再生成、promotion candidate作成、CFR/複合入口設計。

## Guardrails

- `data/normalized/` は変更しない。
- text2ir本体に文書名ベタ書きロジックを入れない。
- 個人環境絶対パスをRUN/PR/報告書に残さない。
- 未コミットの `.gitignore` 変更は今回スコープ外として触らない。

## Phase 9A

Branch:

- `feature/text2ir-final-goal-closure-phase9a`

Implemented:

- `qai_text2ir.cli` が `meta.doc.family` を出力するようにした。
- family解決優先順位を `--family` > `parser_profile.applies_to.family` > `source_label` にした。
- `qai_text2ir.goal_check` に `--mode normal|promotion|release` を追加した。
- promotion/release modeでは `meta.doc.family` 欠落をerrorにした。
- parser profile summaryの `has_markers` が `marker_types` も見るようにした。

Validation:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_goal_check.py
```

Result:

- `8 passed`

## Phase 9B

Branch:

- `feature/text2ir-final-goal-closure-phase9b`

Implemented:

- `qai_text2ir.table_note_inventory` を追加。
- 固定幅表のcaption検出を `Table 1 Maximum...` 形式にも対応。
- 安全に列数が揃う固定幅表は `table/table_header/table_row` 化。
- 不安定な固定幅表は `preformatted` / `kind_raw=possible_table` / `possible_plaintext_table_not_structured` として保持。
- table直後のnoteを `note` として保持。
- 表・注記を持つ代表profileで `detect_plaintext_tables` / `extract_notes` を有効化。
- skip block処理内の内側ループが外側行indexを上書きしていた不具合を修正。

Validation:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_table_note_real_samples.py tests\test_table_note_inventory.py tests\test_markdown_table_parsing.py tests\test_text2ir_goal_check.py
.\.venv\Scripts\python.exe -m qai_text2ir.cli --input data\human-readable\pics\pe009-17_annex1_2023-08-25_en.txt --out-dir out\20260522-130045_text2ir-final-goal-closure\phase9b_smoke_annex1_v3 --doc-id phase9b_smoke_annex1 --title "Phase9B Annex1 Smoke" --short-title "Annex1 Smoke" --doc-type guideline --source-format pdf --retrieved-at 2026-02-18 --jurisdiction INTL --language en --family PICS --parser-profile src\qai_text2ir\profiles\pics_annex1_default_v2.yaml --qualitycheck --strict --write-manifest --overwrite-manifest --emit-only all
```

Result:

- related tests: `20 passed`
- Annex 1 smoke regeneration: strict exit 0
- Annex 1 smoke observed counts: `preformatted=4`, `note=9`

## Phase 9C

Branch:

- `feature/text2ir-final-goal-closure-phase9c`

Implemented:

- profile課題のサンプル比較レポート `PROFILE_SAMPLE_COMPARISON.md` を作成。
- Annex 15 / Annex 11 / Annex 2A / Part II / WHO LBM 3rd の代表課題を確認。

Validation:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_pics_annex15_profile.py tests\test_pics_annex11_profile.py tests\test_pics_annex2a_profile.py tests\test_pics_part2_v1.py tests\test_text2ir_who_lbm_3rd.py
```

Result:

- `12 passed`

## Phase 9D

Branch:

- `feature/text2ir-final-goal-closure-phase9d`

Implemented:

- 代表9文書を現行profileで再生成した。
- 各文書の `goal_check_result.json` と `GOAL_CHECK_RESULT.md` を `out/20260522-130045_text2ir-final-goal-closure/<doc_id>/` に作成した。
- `qai_text2ir.audit_report` に promotion GOAL_CHECK、`meta.doc.family`、`possible_table`、残GAP分類を追加した。
- 代表9文書の監査結果を `TEXT2IR_AUDIT_REPORT.md/json` に作成した。
- 入力側の表・注記候補数と出力側の保持状況を `TABLE_NOTE_INVENTORY.md/json` に作成した。
- 代表9文書の最終GAP状態を `TEXT2IR_FINAL_GAP_STATUS.md` にまとめた。

Validation:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_audit_report.py tests\test_text2ir_goal_check.py
```

Result:

- `10 passed`

Audit result:

- normal GOAL_CHECK: `9/9 pass`
- promotion GOAL_CHECK: `9/9 pass`
- `meta.doc.family`: `9/9 present`
- remaining_gap: `none=6`, `table_rows_pending=3`

## Phase 9E

Branch:

- `feature/text2ir-final-goal-closure-phase9e`

Implemented:

- EU GMP Chapter 1 を最初の promotion candidate として作成した。
- `out/20260522-130045_text2ir-final-goal-closure/eu_gmp_vol4_chap1_20130131/` から4ファイル、manifest、GOAL_CHECK結果を複製した。
- promotion candidate上で `goal_check --mode promotion` を再実行した。
- `SAMPLE_COMPARISON.md` に5件の確認サンプルを作成した。
- `PROMOTION_CANDIDATE_REVIEW.md` をcandidate配下とRUN直下に作成した。
- `manifest.yaml` のコマンド表記から個人環境絶対パスを除去した。

Validation:

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir runs\20260522-130045_text2ir-final-goal-closure\promotion_candidate\eu_gmp_vol4_chap1_20130131 --doc-id eu_gmp_vol4_chap1_20130131 --mode promotion --format markdown --out runs\20260522-130045_text2ir-final-goal-closure\promotion_candidate\eu_gmp_vol4_chap1_20130131\GOAL_CHECK_RESULT.md
```

Result:

- promotion GOAL_CHECK: `PASS`
- `data/normalized/`: unchanged
