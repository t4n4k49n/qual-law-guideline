<!-- PR_BODY_FILE: docs/pr_bodies/pr-archive-annex11-v1-and-review-annex1.md -->

## まとめ

PIC/S Annex 11 の旧v1 RUNを削除せずアーカイブし、PIC/S Annex 1 を正式な正規化RUNへ進める前提確認を完了しました。Annex 1では表・注記の構造化を確認する過程でページフッター混入を発見して修正したため、次の正規化RUNを余分なアーカイブ処理なしに進めやすくしています。

## 変更内容

- `runs/ARCHIVE_20260527-153334008_run-normalized-pics-annex11-v1/` に旧PIC/S Annex 11 v1 RUNを保管
- `runs/20260528-102010880_review-pics-annex1-table-note/` にAnnex 1表・注記レビューRUNを追加
- Annex 1 table parserのページフッター判定を修正
- Annex 1 table/note/table_row payloadへページフッターが混入しないことをテストで固定

## 主な判断

- PIC/S Annex 11 v1は、修正版v2が既に昇格済みのためアーカイブ扱いにする
- PIC/S Annex 1は、修正後の通常確認RUNでpromotion goalがPASSしており、次に正式な正規化RUNへ進めてよい
- 今回の `out/` は確認用であり、正式昇格元には使わない。次の正規化RUNで `runs/<run_id>/promotion_candidate/` を新たに作成する

## 検証

- `.\.venv\Scripts\python.exe -m pytest tests/test_pics_annex1_tables.py -q`
- `.\.venv\Scripts\python.exe -m pytest tests/test_pics_annex1_tables.py tests/test_text2ir_profiles_pics.py tests/test_pics_annexes_bundle_specials.py -q`
- `.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out/20260528-102010880_review-pics-annex1-table-note/pics_pe00917_annex1_20230825_after_footer_fix --doc-id pics_pe00917_annex1_20230825 --mode promotion --format markdown`
- `Select-String -Path out/20260528-102010880_review-pics-annex1-table-note/pics_pe00917_annex1_20230825_after_footer_fix/pics_pe00917_annex1_20230825.regdoc_ir.yaml -Pattern "PE 009-17|25 August 2023"`: 0件
