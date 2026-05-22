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

## Policy Correction

初版では、文書別の範囲調整を主対応に見せる記述が前面に出ていた。これは今回の本質である text2ir 共通の候補汚染問題を弱めるため不適切だった。

本RUNの結論は、個別profile修正ではなく、text2ir共通側で selectable candidate contamination を検出・分類・抑止し、promotion gate で止めることである。WHO LBM 3rd と PIC/S Annex 2A は個別対応対象ではなく、共通対策の代表症例・回帰対象として扱う。
