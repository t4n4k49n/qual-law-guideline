# RUN

run_id: 20260211-190200082_feat-cfr-v2-quality-fixes
branch: feat/cfr-v2-quality-fixes
started_at: 2026-02-11 19:02 (JST)

## 目的（1文）
- CFR Part 11 text2ir の品質問題（Subpart構造化、kind_raw、source_spans重複、heading/chapeau分離、meta path）を解消する。

## Done Definition（完了条件）
- [x] us_cfr_default_v2 profile 追加
- [x] profile_loader 既定をv2へ切替（v1フォールバック）
- [x] text_parser 改修反映
- [x] cli meta入力パスの安全化
- [x] テスト追加/更新と実行

## 実装
- `src/qai_text2ir/profiles/us_cfr_default_v2.yaml` を新規追加
  - `id: us_cfr_default_v2`
  - `root/part/subpart` に `note` 許容を追加
  - `root.children` を `[part, subpart, section, note]` へ拡張
- `src/qai_text2ir/profile_loader.py`
  - 既定で US_CFR は v2 優先、v2 不在時は v1 フォールバック
- `src/qai_text2ir/text_parser.py`
  - source_label を parser_profile 優先化
  - MarkerMatch に raw_token 追加、paragraph/item/subitem の kind_raw を動的化
  - source_spans 重複排除、末尾空白除去、軽いハイフネーション結合
  - 親不在の構造マーカーを root 配下へ安全収容（warning）
  - section の heading/chapeau 分離、part/subpart heading の先頭ダッシュ除去
- `src/qai_text2ir/cli.py`
  - meta generation.inputs.path の既定を相対優先、不可時 basename に変更
- テスト更新/追加
  - `tests/test_text2ir_bundle.py`（既定profile id を v2 化、meta path非絶対を確認）
  - `tests/test_text2ir_cfr_quality_v2.py`（受入条件を包括検証）

## テスト
- 実行: `python -m pytest -q`
- 結果: `22 passed, 1 skipped`

## 実データ再生成（PART11）
- 入力: `%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\human-readable\11.CFR\Un-fomatted\PART11.txt`
- コマンド:
  - `python -m qai_text2ir.cli --input "...\PART11.txt" --out-dir "out/20260211-190200082_feat-cfr-v2-quality-fixes" --doc-id us_cfr_part11_v2_qualitycheck --title "21 CFR Part 11" --short-title "CFR Part 11" --cfr-title 21 --cfr-part 11 --source-url "https://www.ecfr.gov/current/title-21/part-11" --retrieved-at "2026-02-11" --emit-only all`
- 出力:
  - `out/20260211-190200082_feat-cfr-v2-quality-fixes/us_cfr_part11_v2_qualitycheck.regdoc_ir.yaml`
  - `out/20260211-190200082_feat-cfr-v2-quality-fixes/us_cfr_part11_v2_qualitycheck.meta.yaml`
  - `out/20260211-190200082_feat-cfr-v2-quality-fixes/us_cfr_part11_v2_qualitycheck.parser_profile.yaml`
  - `out/20260211-190200082_feat-cfr-v2-quality-fixes/us_cfr_part11_v2_qualitycheck.regdoc_profile.yaml`
  - `runs/20260211-190200082_feat-cfr-v2-quality-fixes/text2ir_part11.log`

## 確認結果（受入条件対応）
- Subpart A/B/C の subpart ノード化を確認（heading: General Provisions / Electronic Records / Electronic Signatures）
- node.text への `Subpart B—Electronic Records` / `Subpart C—Electronic Signatures` 混入なし
- paragraph/item/subitem の kind_raw が `(b)`/`(2)`/`(ii)` と一致
- source_spans の同一 `(source_label, locator)` 重複なし
- §11.300 の heading は `Controls for identification codes/passwords.`、本文は section.text に分離
- meta generation.inputs[0].path は `PART11.txt`（絶対パス非出力）
