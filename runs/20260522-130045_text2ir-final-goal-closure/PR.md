## まとめ

EU GMP Chapter 1 を text2ir の最初の promotion candidate として作成しました。代表9文書の監査結果を前提に、構造ギャップが少なくレビューしやすい文書から正式昇格運用へ橋渡しできる状態にしています。

## 変更内容

- EU GMP Chapter 1 の promotion candidate 一式を追加
- candidate配下でpromotion GOAL_CHECKを再実行
- `SAMPLE_COMPARISON.md` に5件の粒度確認を追加
- `PROMOTION_CANDIDATE_REVIEW.md` を追加
- Phase 9EのRUN記録を更新

## 確認

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir runs\20260522-130045_text2ir-final-goal-closure\promotion_candidate\eu_gmp_vol4_chap1_20130131 --doc-id eu_gmp_vol4_chap1_20130131 --mode promotion --format markdown --out runs\20260522-130045_text2ir-final-goal-closure\promotion_candidate\eu_gmp_vol4_chap1_20130131\GOAL_CHECK_RESULT.md
```

結果: `PASS`

`data/normalized/` は変更していません。

<!-- PR_BODY_FILE: runs/20260522-130045_text2ir-final-goal-closure/PR.md -->
