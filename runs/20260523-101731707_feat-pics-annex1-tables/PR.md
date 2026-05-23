<!-- PR_BODY_FILE: runs/20260523-101731707_feat-pics-annex1-tables/PR.md -->

## まとめ

PIC/S Annex 1 の Table 1-6 を専用正規化で構造化し、DQ GMPチェックリストで表行を選択・参照できる粒度に整えました。これにより、清浄度グレード別の粒子数・微生物限度・作業例が本文混入や固定幅テキストではなく、`table_row` と注記として安定して扱えます。

## 変更内容

- Annex 1 Table 1-6 専用の `pics_annex1_tables` 正規化を追加
- `pics_annex1_default_v2` でのみ有効化
- 複合Annexの subtree refine でも Annex 1 子プロファイルの表正規化を適用
- Table 1/2/5/6 の grade A-D、測定単位、脚注/注記を保持
- Table 3/4 の grade-operation 表を本文段落から分離
- 専用テストとRUN成果物を追加

## 確認結果

- Annex 1 special structure audit: pass
  - source_tables: 6
  - generated_tables: 6
  - generated_rows: 35
  - unresolved_special_blocks: 0
- Annex 1 GOAL check: pass
- 複合Annex GOAL check: pass
- 複合Annex special structure audit: warn
  - Annex 1 Table 1-6 は構造化済み
  - 残る unresolved は Annex 2A/2B/3/7/14/19 と figure 系で、今回対象外

## テスト

- `python -m pytest tests/test_pics_annex1_tables.py tests/test_pics_annexes_refine_v3_fallback.py tests/test_pics_annexes_refine_v2.py -q`
  - 12 passed
- `python -m pytest -q`
  - 183 passed, 1 skipped

## 関連成果物

- `runs/20260523-101731707_feat-pics-annex1-tables/RUN.md`
- `runs/20260523-101731707_feat-pics-annex1-tables/PICS_ANNEX1_TABLES_REPORT.md`
- `runs/20260523-101731707_feat-pics-annex1-tables/SPECIAL_STRUCTURE_AUDIT.md`
- `runs/20260523-101731707_feat-pics-annex1-tables/COMBINED_ANNEXES_SPECIAL_STRUCTURE_AUDIT.md`
