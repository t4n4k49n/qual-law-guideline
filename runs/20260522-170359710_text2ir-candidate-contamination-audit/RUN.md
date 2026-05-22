# RUN: text2ir candidate contamination audit

## Purpose

WHO LBMで発見された `` / ドットリーダー混入を一般化し、最新text2ir出力の選択可能候補に類似問題がないか確認する。

## Scope

- latest representative 9 bundles
- `out/*review_ui`
- promotion candidates
- phase smoke outputs excluded

## Outputs

- `TEXT2IR_CANDIDATE_CONTAMINATION_AUDIT.md`
- `out/20260522-170359710_text2ir-candidate-contamination-audit/candidate_contamination_audit.json`
- `out/20260522-170359710_text2ir-candidate-contamination-audit/candidate_contamination_findings.tsv`

## Result

- documents scanned: 19
- findings including copied duplicates: 72
- unique finding keys: 36
- severe findings: 18

## Notes

- コード修正は実施していない。
- `data/normalized/` は変更していない。
