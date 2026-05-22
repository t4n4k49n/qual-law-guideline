# RUN: text2ir glyph/form artifact cleanup

- run_id: `20260522-222947088_fix-text2ir-glyph-form-artifact-cleanup`
- branch: `fix/text2ir-glyph-form-artifact-cleanup`
- purpose: PDF抽出由来の Private Use Area glyph、dot leader、チェックフォーム残骸が text2ir の `.regdoc_ir.yaml` に残る問題を共通処理として閉じる。

## Scope

- コード修正あり。
- `data/normalized/` への昇格なし。
- 代表9文書を `out/20260522-222947088_fix-text2ir-glyph-form-artifact-cleanup/` に再生成。
- 人手確認用に WHO LBM 3rd の再生成済み `regdoc_ir.yaml` を本RUN配下にも複写。

## Implemented

- `src/qai_text2ir/glyph_sanitizer.py`
  - literal PUA検出、codepoint列挙、marker glyph正規化、可読文字列sanitizeを追加。
- `src/qai_text2ir/artifact_classifier.py`
  - dot leader、PUA checkbox、`CHECKED ITEM` / `YES NO N/A` 系フォーム、固定幅フォームを検出。
  - 通常の固定幅表を過剰にフォーム扱いしないよう、単独の `NO` などではフォーム判定しない。
- `src/qai_text2ir/text_parser.py`
  - marker判定前に PUA bullet を通常bullet相当に正規化。
  - postprocessでフォーム残骸を通常本文から分離し、sanitize済み `preformatted` / `kind_raw: form_artifact` として隔離。
  - `text`, `heading`, `kind_raw`, `tags`, `refs`, `data` に literal PUA を残さないよう再帰sanitize。
- `src/qai_text2ir/goal_check.py`
  - promotion/releaseで literal PUA、replacement char、可読本文のsevere form artifact、contamination guard残存、artifact kind selectableを失格化。
- `src/qai_text2ir/artifact_audit.py`
  - `.regdoc_ir.yaml` の glyph/form artifact 監査CLIを追加。
- tests
  - WHO LBM form artifact分離、PIC/S PUA bullet正規化、goal_check promotion失格条件を追加。

## Regeneration

代表9文書を再生成した。

- `eu_gmp_vol4_chap1_20130131`
- `pics_pe00917_annex1_20230825`
- `pics_pe00917_annex11_20230825`
- `pics_pe00917_annex15_20230825`
- `pics_pe00917_annex2a_20230825`
- `pics_pe00917_annexes_20230825_refined_v3_extends_trace`
- `pics_pe00917_part1_20230825`
- `pics_pe00917_part2_20230825`
- `who_lbm_3rd_2004_9241546506`

過去manifestのコマンドを元に再実行したが、PIC/S Annex 1 は既存の single newline 警告で `--strict` が停止するため、代表出力確認では `--strict` だけ外した。これは今回のglyph/form artifact問題とは別系統として扱う。

## Results

- 代表9文書の promotion goal_check: 全件PASS。
- 代表9文書の literal PUA: 0。
- 代表9文書の replacement char: 0。
- 代表9文書の severe visible artifact: 0。
- WHO LBM 3rd の `cha8.i5` 本文は保持。
- WHO LBM 3rd の `cha8.i5.si1` / `cha8.i5.si2` は `form_artifact`, `not_selectable`, `sanitized_layout_artifact` 付きの `preformatted` へ隔離。

## Outputs

- `runs/20260522-222947088_fix-text2ir-glyph-form-artifact-cleanup/TEXT2IR_ARTIFACT_AUDIT.md`
- `runs/20260522-222947088_fix-text2ir-glyph-form-artifact-cleanup/GOAL_CHECK_SUMMARY.md`
- `runs/20260522-222947088_fix-text2ir-glyph-form-artifact-cleanup/TEXT2IR_GLYPH_FORM_CLEANUP_REPORT.md`
- `runs/20260522-222947088_fix-text2ir-glyph-form-artifact-cleanup/who_lbm_3rd_2004_9241546506/who_lbm_3rd_2004_9241546506.regdoc_ir.yaml`

## Verification

- `python -m pytest tests/test_text2ir_glyph_form_cleanup.py tests/test_text2ir_goal_check.py -q`
- `python -m pytest tests/test_text2ir_who_lbm_3rd.py tests/test_pics_annex2a_preformatted.py tests/test_table_note_real_samples.py tests/test_text2ir_audit_report.py -q`
- representative regeneration for 9 docs
- `python -m qai_text2ir.goal_check --mode promotion` for 9 regenerated bundles
- `python -m qai_text2ir.artifact_audit out/20260522-222947088_fix-text2ir-glyph-form-artifact-cleanup`

