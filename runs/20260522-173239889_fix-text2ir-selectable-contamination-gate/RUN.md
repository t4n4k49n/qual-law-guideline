# RUN: fix text2ir selectable contamination gate

## Purpose

`runs/20260522-170359710_text2ir-candidate-contamination-audit/IMPLEMENTATION_HANDOFF.md` に従い、PDF抽出由来の表・フォーム・チェック欄・固定幅崩れが通常 selectable `item` / `subitem` として出る問題を共通対策で解消する。

## Branch

- `fix/text2ir-selectable-contamination-gate`

## Scope

- text2ir共通detectorを追加
- `goal_check --mode promotion` / `--mode release` で重大な selectable candidate contamination をfail化
- parser最終段で重大汚染の通常候補を `preformatted` に降格
- WHO LBM 3rd / PIC/S Annex 2A / Annexes refined を代表症例として再生成・確認
- `data/normalized/` は変更しない

## Implementation

- `src/qai_text2ir/contamination.py`
  - 私用領域文字、長いドットリーダー、チェック欄列、固定幅列崩れ、表/フォーム行の共通detectorを追加。
- `src/qai_text2ir/goal_check.py`
  - contamination summaryを出力。
  - severe finding は normal mode でwarning、promotion/release modeでerror。
  - 非severe findingはsummaryに残し、warningノイズにはしない。
- `src/qai_text2ir/text_parser.py`
  - postprocess後、qualitycheck前に重大汚染の通常候補を `preformatted` へ降格。
  - `kind_raw` は `possible_form` / `possible_table` とし、元kindと検出結果を `data` に保持。
- tests
  - goal_check mode別挙動
  - WHO LBM 3rd の `cha8.i5` 近傍代表症例
  - PIC/S Annex 2A の固定幅・私用領域文字混在代表症例

## Validation

```powershell
python -m pytest -q tests\test_text2ir_goal_check.py tests\test_text2ir_who_lbm_3rd.py tests\test_pics_annex2a_preformatted.py
python -m pytest -q tests\test_text2ir_audit_report.py tests\test_table_note_real_samples.py tests\test_table_note_inventory.py tests\test_markdown_table_parsing.py tests\test_normal_note_descendants.py tests\test_pics_annex1_profile_v2.py tests\test_pics_annex11_profile.py tests\test_pics_annex15_profile.py tests\test_pics_annex2a_profile.py tests\test_pics_part1_full_v3.py tests\test_pics_part2_v1.py tests\test_who_lbm_v4_skip_toc_and_annex_heading.py
python -m pytest -q
```

Result:

- targeted: `18 passed`
- broader text2ir/profile: `30 passed`
- full pytest: `171 passed, 1 skipped`

## Regeneration

代表9文書を `out/20260522-173239889_fix-text2ir-selectable-contamination-gate/<doc_id>/` に再生成し、各bundleで `goal_check --mode promotion` を実行した。

Summary:

- `runs/20260522-173239889_fix-text2ir-selectable-contamination-gate/CONTAMINATION_RESOLUTION_SUMMARY.md`
- `runs/20260522-173239889_fix-text2ir-selectable-contamination-gate/contamination_resolution_summary.json`

Key result:

- WHO LBM 3rd severe contamination: `0`
- PIC/S Annex 2A severe contamination: `0`
- PIC/S Annexes refined 内 Annex 2A同等箇所 severe contamination: `0`
- 代表9文書の promotion goal_check: `9/9 pass`
- promotion goal_check errors/warnings: `0`

## Critical Nodes

- `who_lbm_3rd_2004_9241546506`: `cha8.i5`, `cha8.i5.si1`, `cha8.i5.si2` は `preformatted` / `possible_form` に降格。
- `pics_pe00917_annex2a_20230825`: `ann2a.sec2.ib.si1`, `ann2a.sec2.ib.si2`, `ann2a.sec2.ib.si3` は `preformatted` / `possible_table` に降格。
- `pics_pe00917_annexes_20230825_refined_v3_extends_trace`: 同等のAnnex 2Aノードも `preformatted` / `possible_table` に降格。

## Notes

- 個別profile patchではなく、共通detector / parser guard / promotion gateで対応した。
- `findings` は軽微兆候を含む件数で、promotion fail対象は `severe`。
- `data/normalized/` は変更していない。
