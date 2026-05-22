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
