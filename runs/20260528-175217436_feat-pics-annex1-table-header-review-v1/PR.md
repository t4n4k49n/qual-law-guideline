<!-- PR_BODY_FILE: runs/20260528-175217436_feat-pics-annex1-table-header-review-v1/PR.md -->

## まとめ

PIC/S Annex 1のTable 1/5について、二段ヘッダの親セルを含めた単独可読な列名へ修正しました。これにより、IRの`table_header.text`と`data.columns`だけを見ても、各列がどの粒径・状態の上限値を表すか判定できます。

## 変更内容

- Table 1/5の列名に上段結合ヘッダ `Maximum limits for total particle ...` を含めるよう修正
- `table_header.text` と `table_header.data.columns` の完全列名をテストで固定
- 列名が重複しないことをテストで固定
- RUN開始時に `runs/<run_id>/` と `out/<run_id>/` を同名で作成する運用を明記

## 確認

- `python -m pytest tests\test_pics_annex1_tables.py -q`
- 検証用bundleを `out/20260528-175217436_feat-pics-annex1-table-header-review-v1/` に生成
- 生成IRのTable 1/5ヘッダが完全列名になっていることを確認
