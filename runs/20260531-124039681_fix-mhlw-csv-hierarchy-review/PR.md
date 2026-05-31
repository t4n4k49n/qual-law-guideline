# MHLW CSVガイドラインの本文階層を修正

## まとめ

CSVガイドライン本文の階層復元で、原文上は `④ 基本的な考え方` の配下にある中黒項目が兄弟ノードになっていた問題を修正した。正規化RUNの前段として、本文構造の取り違えを parser/profile/test 側で固定し、後続の正規化候補レビューで同じ見落としが再発しない状態にする。

## 変更内容

- CSV profile で中黒 `・` / `●` を `point` として扱うよう変更。
- CSV profile の structure に `subitem -> point` を追加。
- `section_decimal` のマーカー残部を `heading` に分離できる parser option を追加。
- 実HTML由来のテストで、`cha3.i1.si4` 配下に5つの `point` が入ることを確認。

## これは正規化RUNではない

- `runs/<run_id>/promotion_candidate/` は作成していない。
- `data/normalized/` は変更していない。
- 変更対象は parser/profile/test と、通常RUNの記録のみ。

## 検証

- `pytest tests/test_text2ir_csv_guideline.py tests/test_mhlw_csv_annex2_tables.py tests/test_mhlw_csv_annexes.py tests/test_mhlw_csv_annex_source_recovery.py tests/test_candidate_visibility_profiles_6_9.py -q`: `17 passed`

## 目検チェック

`runs/20260531-124039681_fix-mhlw-csv-hierarchy-review/CSV_HIERARCHY_CHECK.md` に、指摘箇所の修正後ツリーを記録した。

<!-- PR_BODY_FILE: runs/20260531-124039681_fix-mhlw-csv-hierarchy-review/PR.md -->
