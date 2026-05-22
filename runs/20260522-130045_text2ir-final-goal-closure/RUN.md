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
