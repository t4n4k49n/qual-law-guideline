<!-- PR_BODY_FILE: runs/20260523-115057430_feat-pics-part2-table1/PR.md -->

## まとめ

PIC/S Part II の API製造適用範囲を示す Table 1 を構造化し、本文に混入した固定幅テーブルではなく、製造タイプごとの `table_row` として参照できるようにしました。API Starting Material導入点以降のGMP適用範囲を表行単位で扱えるため、チェックリスト表示と根拠確認の粒度が安定します。

## 変更内容

- Part II Table 1専用の `pics_part2_table1` 正規化を追加
- `pics_part2_default_v1` でのみ有効化
- Table 1を7行の `table_row` と1つの注記 `note` に構造化
- `Increasing GMP requirements` を通常本文ではなくtable annotation noteとして保持
- PDF shadingは復元せず、復元不可であることをtable dataへ明示
- 専用テストとRUN成果物を追加

## 確認結果

- special structure audit: pass
  - generated_tables: 1
  - generated_rows: 7
  - unresolved_special_blocks: 0
- GOAL check: pass
  - warnings: none

## テスト

- `python -m pytest tests/test_pics_part2_table1.py -q`
  - 5 passed
- `python -m pytest tests/test_pics_annex1_tables.py tests/test_pics_annex2a_structures.py tests/test_pics_part2_table1.py -q`
  - 17 passed
- `python -m pytest -q`
  - 192 passed, 1 skipped

## 関連成果物

- `runs/20260523-115057430_feat-pics-part2-table1/RUN.md`
- `runs/20260523-115057430_feat-pics-part2-table1/PICS_PART2_TABLE1_REPORT.md`
- `runs/20260523-115057430_feat-pics-part2-table1/SPECIAL_STRUCTURE_AUDIT.md`
