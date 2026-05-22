# text2ir form artifact visibility fix

## Run

- run_id: `20260522-230843653_fix-text2ir-form-artifact-visibility`
- branch: `fix/text2ir-form-artifact-visibility`
- scope: `text2ir` common artifact detection, default visibility, promotion gate, tests, and regenerated review outputs
- status: implementation and verification completed locally; PR pending

## Purpose

`WHO LBM 3rd` の Table 5-7 周辺で、PDF抽出由来の記入式フォーム残骸が、通常候補・通常本文のように review UI に見えていた問題を閉じる。個別NID削除やWHO専用profile逃げではなく、`form_artifact` を共通の参照用artifactとして扱い、default review / DQ候補 / promotion gate から除外する。

## Main Changes

- Added common glyph sanitizer for literal private-use glyph handling.
- Added common form artifact classifier.
- Added mock UI artifact visibility rules.
- `text_parser` now separates form artifacts from visible prose, stores short `form_artifact.text`, and moves raw detail to `data.raw_text_escaped` with hidden visibility.
- `goal_check --mode promotion` now fails on:
  - literal private-use glyphs
  - replacement characters
  - default-visible form leakage
  - long `form_artifact.text`
  - selectable artifact kinds
- Mock review candidate visibility now hides artifact-like nodes even if the raw kind is otherwise allowed.

## Generated Outputs

- Regenerated representative bundles:
  - `out/20260522-230843653_fix-text2ir-form-artifact-visibility/eu_gmp_vol4_chap1_20130131/`
  - `out/20260522-230843653_fix-text2ir-form-artifact-visibility/pics_pe00917_annex11_20230825/`
  - `out/20260522-230843653_fix-text2ir-form-artifact-visibility/pics_pe00917_annex15_20230825/`
  - `out/20260522-230843653_fix-text2ir-form-artifact-visibility/pics_pe00917_annex1_20230825/`
  - `out/20260522-230843653_fix-text2ir-form-artifact-visibility/pics_pe00917_annex2a_20230825/`
  - `out/20260522-230843653_fix-text2ir-form-artifact-visibility/pics_pe00917_annexes_20230825_refined_v3_extends_trace/`
  - `out/20260522-230843653_fix-text2ir-form-artifact-visibility/pics_pe00917_part1_20230825/`
  - `out/20260522-230843653_fix-text2ir-form-artifact-visibility/pics_pe00917_part2_20230825/`
  - `out/20260522-230843653_fix-text2ir-form-artifact-visibility/who_lbm_3rd_2004_9241546506/`
- Updated local review UI folders under `out/*_review_ui/` with regenerated YAML copies.

## Verification

- `python -m pytest -q`
  - result: `171 passed, 1 skipped`
- Representative 9 document regeneration:
  - result: all completed
- `python -m qai_text2ir.goal_check --mode promotion`
  - result: all 9 representative bundles passed
- Artifact visibility audit:
  - literal PUA node count: `0` for all 9 bundles
  - default-visible form leakage: `0` for all 9 bundles
  - candidate export leakage: `0` for all 9 bundles
  - WHO LBM form artifacts: `3`
  - WHO LBM long `form_artifact.text`: `0`

## Notes

- Full IR may still contain raw form text inside `data.raw_text_escaped` for traceability. It is not default visible and is excluded from the default candidate list.
- The previous PR #149 code was not reused by cherry-pick. This branch reimplemented the fix from the current main state after #149 was discarded.
