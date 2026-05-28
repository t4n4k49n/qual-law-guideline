# PIC/S Annex 2A 表見出し・Warning目検確認

## まとめ

PIC/S Annex 2A の正規化RUN前確認として、表・Figure・Warningを実ソース画像と照合しました。Table 1 の4つの application 列は親見出しを含めないと単独で意味が曖昧になるため、IR列名を親見出し込みに修正し、正規化候補としてレビューしやすい形にしました。

## 変更内容

- Annex 2A Table 1 の列名を `Application of this Annex (see note 1)` 付きに修正。
- Table 1 の列名が完全・一意であることをテストに追加。
- PDFページ画像による目検記録を run artifact として追加。
- promotion goal check と warning確認結果を run artifact として追加。

## 確認結果

- Table 1: 1件、5列、6行、table note 3件をPDF page 77と照合済み。
- Figure: 3件をPDF page 78-79と照合済み。
- Warning:
  - strict bundle quality warnings: none
  - promotion goal warnings: none
  - IR warning metadata scan: none

## テスト

- `python -m pytest tests\test_pics_annex2a_structures.py tests\test_pics_annex2a_profile.py tests\test_pics_annex2a_preformatted.py tests\test_pics_annexes_bundle_specials.py -q`
  - `13 passed`
- `python -m pytest -q`
  - `249 passed, 1 skipped`

## 次工程

このPRをマージ後、PIC/S Annex 2A の正規化RUNに進む。

<!-- PR_BODY_FILE: runs/20260528-191035093_feat-pics-annex2a-table-warning-review-v1/PR.md -->
