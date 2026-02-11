# RUN

run_id: 20260211-162349749_feat-cfr-note-lines-separation
branch: feat/cfr-note-lines-separation
started_at: 2026-02-11 16:23 (JST)

## 目的（1文）
- CFR限定で注記行（FR引用 / Authority / Source）を本文から分離し、`note` ノードとして保持する。

## Done Definition（完了条件）
- [x] `us_cfr_default_v1` で注記行を marker として認識できる
- [x] 注記行が本文末端ノードに混入しない
- [x] 既存text2irテストと新規回帰テストが通る

## 手順（やった順）
1) `PART11/PART211` 実例から非marker行を抽出し、参照用ファイルを run に保存
2) `us_cfr_default_v1.yaml` に注記marker（`note_fr`, `note_authority_source`）を追加
3) `section.children` に `note` を追加
4) `text_parser` で `note/history` を `informative` 扱いに変更
5) CFR注記分離の回帰テストと fixture を追加
6) 関連テストを実行

## 実行コマンド
- `python -m pytest -q tests/test_text2ir_bundle.py tests/test_text2ir_profiles_pics.py tests/test_text2ir_marker_disambiguation.py tests/test_text2ir_cfr_notes.py`

## 結果（事実ベース）
- 何ができた：
  - CFR注記行を `note` として構造分離
  - `note` の role/normativity を informative/None に統一
  - 回帰テストを追加し、注記混入防止を自動検証
- 数値：
  - pytest: `8 passed`

## 生成物（共有）
- `runs/20260211-162349749_feat-cfr-note-lines-separation/PART11_non_marker_lines.txt`
- `runs/20260211-162349749_feat-cfr-note-lines-separation/PART211_non_marker_lines.txt`

## 変更ファイル
- `src/qai_text2ir/profiles/us_cfr_default_v1.yaml`
- `src/qai_text2ir/text_parser.py`
- `tests/fixtures/CFR_PART11_with_notes.txt`
- `tests/test_text2ir_cfr_notes.py`
- `runs/20260211-162349749_feat-cfr-note-lines-separation/PART11_non_marker_lines.txt`
- `runs/20260211-162349749_feat-cfr-note-lines-separation/PART211_non_marker_lines.txt`
- `runs/20260211-162349749_feat-cfr-note-lines-separation/RUN.md`
