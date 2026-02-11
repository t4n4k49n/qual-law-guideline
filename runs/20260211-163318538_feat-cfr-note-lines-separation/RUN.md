# RUN

run_id: 20260211-163318538_feat-cfr-note-lines-separation
branch: feat/cfr-note-lines-separation
started_at: 2026-02-11 16:33 (JST)

## 目的（1文）
- CFR実データ2ファイル（PART11/PART211）で text2ir を実行し、4 YAML 出力と注記分離の実動作を確認する。

## Done Definition（完了条件）
- [x] 2入力それぞれで 4 YAML（計8ファイル）が生成される
- [x] 実行ログが runs に保存される
- [x] PART11 で `note` ノード化を確認する

## 入力
- `%USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\human-readable\\11.CFR\\Un-fomatted\\PART11.txt`
- `%USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\human-readable\\11.CFR\\Un-fomatted\\PART211.txt`

## 実行コマンド
- `python -m qai_text2ir.cli --input <PART11.txt> --out-dir out/20260211-163318538_feat-cfr-note-lines-separation --doc-id us_cfr_part11_unformatted_notecheck --title "21 CFR Part 11" --short-title "CFR Part 11" --cfr-title 21 --cfr-part 11 --source-url "https://www.ecfr.gov/current/title-21/part-11" --retrieved-at "2026-02-11" --emit-only all`
- `python -m qai_text2ir.cli --input <PART211.txt> --out-dir out/20260211-163318538_feat-cfr-note-lines-separation --doc-id us_cfr_part211_unformatted_notecheck --title "21 CFR Part 211" --short-title "CFR Part 211" --cfr-title 21 --cfr-part 211 --source-url "https://www.ecfr.gov/current/title-21/part-211" --retrieved-at "2026-02-11" --emit-only all`

## 結果（事実ベース）
- 何ができた：
  - `out/20260211-163318538_feat-cfr-note-lines-separation/` に 8ファイル生成
  - PART11 で `kind: note` ノードを確認
  - PART211 は今回の注記ルール（FR角括弧/Authority/Source）に該当行なし
- 何ができなかった：
  - PART211での `note` ノード生成（入力側に該当行が無いため）

## 生成物
- `out/20260211-163318538_feat-cfr-note-lines-separation/us_cfr_part11_unformatted_notecheck.regdoc_ir.yaml`
- `out/20260211-163318538_feat-cfr-note-lines-separation/us_cfr_part11_unformatted_notecheck.meta.yaml`
- `out/20260211-163318538_feat-cfr-note-lines-separation/us_cfr_part11_unformatted_notecheck.parser_profile.yaml`
- `out/20260211-163318538_feat-cfr-note-lines-separation/us_cfr_part11_unformatted_notecheck.regdoc_profile.yaml`
- `out/20260211-163318538_feat-cfr-note-lines-separation/us_cfr_part211_unformatted_notecheck.regdoc_ir.yaml`
- `out/20260211-163318538_feat-cfr-note-lines-separation/us_cfr_part211_unformatted_notecheck.meta.yaml`
- `out/20260211-163318538_feat-cfr-note-lines-separation/us_cfr_part211_unformatted_notecheck.parser_profile.yaml`
- `out/20260211-163318538_feat-cfr-note-lines-separation/us_cfr_part211_unformatted_notecheck.regdoc_profile.yaml`
- `runs/20260211-163318538_feat-cfr-note-lines-separation/text2ir_part11.log`
- `runs/20260211-163318538_feat-cfr-note-lines-separation/text2ir_part211.log`
