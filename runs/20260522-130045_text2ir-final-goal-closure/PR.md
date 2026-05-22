## まとめ

text2ir最終GOAL閉鎖に向けて、代表9文書の監査、EU GMP Chapter 1のpromotion candidate作成、CFR/XML入口と複合入口の設計分離まで実施しました。正式昇格へ進める候補と、後続RUNへ分けるべき入口課題を分け、レビュー可能な状態にしています。

## 変更内容

- `qai_text2ir` のmeta family / promotion GOAL_CHECK / audit_reportを強化
- 表・注記候補を黙殺しない保守的保持を追加
- 代表9文書を再生成・監査
- EU GMP Chapter 1 の promotion candidate 一式を追加
- `docs/CFR_XML_ADAPTER_DESIGN.md` を追加
- `docs/TEXT2IR_COMPOSITE_ENTRY_DESIGN.md` を追加
- `NEXT_REVIEW_REQUEST.md` を追加

## 確認

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_audit_report.py tests\test_text2ir_goal_check.py tests\test_table_note_real_samples.py tests\test_table_note_inventory.py
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir runs\20260522-130045_text2ir-final-goal-closure\promotion_candidate\eu_gmp_vol4_chap1_20130131 --doc-id eu_gmp_vol4_chap1_20130131 --mode promotion
```

結果:

- related tests: `17 passed`
- EU GMP Chapter 1 promotion GOAL_CHECK: `PASS`
- representative 9 docs: normal GOAL_CHECK `9/9 pass`, promotion GOAL_CHECK `9/9 pass`

`data/normalized/` は変更していません。

<!-- PR_BODY_FILE: runs/20260522-130045_text2ir-final-goal-closure/PR.md -->
