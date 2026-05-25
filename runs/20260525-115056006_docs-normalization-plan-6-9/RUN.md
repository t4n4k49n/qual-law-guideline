# RUN

## run_id

`20260525-115056006_docs-normalization-plan-6-9`

## Branch

`docs/normalization-plan-6-9`

## Purpose

指定表の6/7/8/9について、既存 `text2ir` 実装とソースデータの形状を踏まえた正規化計画を文書化する。

## Inputs

- `README.md`
- `local_notes/TODO.md`
- `src/qai_text2ir/`
- `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- `data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt`
- `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- `data/human-readable/mhlw/csv_guideline/00tb6573.html`

## Outputs

- `docs/NORMALIZATION_PLAN_6_9.md`

## Summary

- 日本語 `text2ir` 共通基盤を先行する方針にした。
- 6/7/9は共通基盤後に並列可能と整理した。
- 8は条文本文と別表・付表の混在が重いため最後に回す方針にした。
- 対象外OKは文書除外ではなく、candidate visibilityやレビュー範囲制御で扱う方針にした。

## Verification

- Documentation-only change.
- No code tests were run.
