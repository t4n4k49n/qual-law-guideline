# PIC/S Part II 表見出し・Warning目検確認

## まとめ

PIC/S Part II の正規化RUN前確認として、Table 1とWarningを実ソース画像と照合しました。Table 1 の application step 列は親見出しを含めないと単独で意味が曖昧になるため、IR列名を親見出し込みに修正し、正式候補化前にレビューしやすい形にしました。

## 変更内容

- Part II Table 1 の列名を `Application of this Guide to steps (shown in grey) used in this type of manufacturing` 付きに修正。
- Row 7の `“Classical” Fermentation to produce an API` の引用符を保持。
- Table 1 の列名が完全・一意であることをテストに追加。
- PDFページ画像による目検記録を run artifact として追加。
- promotion goal check と warning確認結果を run artifact として追加。

## 確認結果

- Table 1: 1件、6列、7行、annotation 1件をPDF page 8と照合済み。
- Warning:
  - strict bundle quality warnings: none
  - promotion goal warnings: none
  - IR warning metadata scan: none

## テスト

- `python -m pytest tests\test_pics_part2_table1.py tests\test_pics_part2_v1.py -q`
  - `8 passed`
- `python -m pytest -q`
  - `250 passed, 1 skipped`

## 次工程

このPRをマージ後、PIC/S Part II の正規化RUNに進む。

<!-- PR_BODY_FILE: runs/20260528-201211084_feat-pics-part2-table-warning-review-v1/PR.md -->
