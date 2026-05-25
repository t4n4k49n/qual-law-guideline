## まとめ

無菌操作法指針で未解決だった固定幅表候補3件を確認し、いずれも表として扱うべき候補と判断して、専用adapterでraw row tableとして分離しました。共通parserの固定幅表検出は緩めず、PMDA無菌操作法指針の既知captionと章節に閉じることで、他文書への誤検出リスクを避けています。

## 変更内容

- `aseptic_processing_table_adapter` を追加
- 無菌操作法指針profileでのみ表候補adapterを有効化
- 表1、表2、表3を `table -> table_header -> table_row` として保持
- 既存の `preformatted possible_table` だった表3をtable nodeへ置換
- 候補ごとの判断、正規化度、今回入れない課題をRUNに記録
- goal_check / special_structure_audit結果を追加

## 確認

- `.\.venv\Scripts\python.exe -m pytest tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_goal_check.py tests\test_special_structure_audit.py -q`
- `.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\pmda\aseptic_processing_guideline\source_texts\000206144.txt --parser-profile-id jp_pmda_aseptic_processing_guideline_v1 --strict`
- `.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --mode normal`
- `.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --mode normal`

## 注意

- 共通の固定幅表検出は変更していません。
- 列復元、複数行セルの再結合、ヘッダ階層の意味付けは未実施です。
- これらをこのPRに入れない理由はRUNに記録しています。
- `data/normalized/` への昇格は行っていません。

<!-- PR_BODY_FILE: runs/20260525-160439120_feat-aseptic-processing-table-candidates-v1/PR.md -->
