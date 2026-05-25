## まとめ

原薬GMPガイドラインの表1を、RUN内の手作業置換なしでIR上のtableとして保持できるようにしました。共通parserの表検出を緩めず、API GMP専用adapterとして閉じることで、他文書への誤検出リスクを避けながら後続の列復元検討に進める状態にしています。

## 変更内容

- `api_gmp_table1_adapter` を追加
- API GMP専用profileでのみ表1adapterを有効化
- raw TXTの表1ブロックを `table -> table_header -> table_row` として保持
- 表1のraw row保持をテストで固定
- RUN記録、goal_check、special_structure_audit結果を追加

## 確認

- `.\.venv\Scripts\python.exe -m pytest tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_jp_guideline.py tests\test_markdown_table_parsing.py tests\test_table_note_real_samples.py -q`
- `.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\pmda\api_gmp_guideline\source_texts\000156438.txt --parser-profile-id jp_pmda_api_gmp_guideline_v1 --strict`
- `.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --mode normal`
- `.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --mode normal`

## 注意

- 共通の固定幅表検出は変更していません。
- 列復元、灰色部分の復元、セル単位の意味付けは未実施です。
- これらをこのPRに入れない理由はRUNに記録しています。
- `data/normalized/` への昇格は行っていません。

<!-- PR_BODY_FILE: runs/20260525-153057355_feat-api-gmp-table1-adapter-v1/PR.md -->
