# RUN

run_id: 20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211
branch: test/text2ir-cfr-realfile-rerun-20260211
started_at: 2026-02-11 02:19 (JST)

## 目的（1文）
- `(c)` の alpha/roman 競合問題を発見した時と同条件で text2ir 実行を再現し、現行mainで同結果を確認する。

## Done Definition（完了条件）
- [x] コマンド1回で再現できる
- [x] out/<run_id>/ に成果物がタイムスタンプ付きで生成される（上書きなし）
- [x] TODO.md が更新され、次にやることが上から追える

## 重要：文字化け回避（UTF-8遵守）
- テキストは UTF-8（BOMなし）、改行はLF

## 手順（やった順）
1) ブランチ `test/text2ir-cfr-realfile-rerun-20260211` を作成
2) `runs/<run_id>/` と `out/<run_id>/` を作成
3) 発見時と同入力・同オプションで `python -m qai_text2ir.cli` を実行
4) 実行ログと出力YAMLを確認

## 実行コマンド（コピペで再現できる形）
- `python -m qai_text2ir.cli --input "%USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\human-readable\\11.CFR\\CFR_PART11_SubpartA.txt" --out-dir "out/20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211" --doc-id us_cfr_part11_realcheck --title "21 CFR Part 11" --short-title "CFR Part 11" --cfr-title 21 --cfr-part 11 --source-url "https://www.ecfr.gov/current/title-21/part-11" --retrieved-at "2026-02-10" --emit-only all`

## 結果（事実ベース）
- 何ができた：
  - 同条件 rerun を実行し、`out/20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211/` に4ファイル生成
  - 実行ログで `(c)(d)(i)(l)(m)` はすべて `chosen=paren_alpha` を確認
  - `sec11_1.pc/pd/pi/pl/pm` が存在し、旧誤分類ノードは検出されなかった
- 何ができなかった：
  - なし
- 数値（処理時間/件数/フレーム数など）：
  - 生成物: 4ファイル
  - `regdoc_ir.yaml` サイズ: 24,816 bytes

## 生成物（上書き禁止）
- `out/20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211/us_cfr_part11_realcheck.regdoc_ir.yaml`
- `out/20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211/us_cfr_part11_realcheck.meta.yaml`
- `out/20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211/us_cfr_part11_realcheck.parser_profile.yaml`
- `out/20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211/us_cfr_part11_realcheck.regdoc_profile.yaml`
- `runs/20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211/text2ir_realfile_rerun.log`

## 影響範囲（変更点）
- 変更ファイル：
  - `runs/20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211/RUN.md`
  - `TODO.md`
- ふるまいの変更：
  - なし（検証runのみ）

## ロールバック
- `git switch main`
- `git branch -D test/text2ir-cfr-realfile-rerun-20260211`（不要時）

## つまずき・学び
- 事象：
  - `python -m qai_text2ir.cli bundle ...` 形式だと引数エラーになる
- 原因：
  - 現CLIは `bundle` サブコマンド不要（root command が bundle 相当）
- 対策：
  - `python -m qai_text2ir.cli --input ...` 形式で実行
- 次回への注意：
  - 再現runは実行コマンドを `RUN.md` へ固定記録する

## KNOWLEDGE候補（昇格するなら）
- text2ir CLI の実行形式（サブコマンド不要）を運用知見として残す価値あり

## 次のTODO（1〜3個）
- [ ] 必要なら `out/<run_id>/` の比較差分を `runs/<run_id>/` に抜粋保存する
- [ ] 再現runをCIで自動化するか判断する
