<!-- PR_BODY_FILE: runs/20260526-005646660_docs-remaining-normalization-plan-6-9/PR.md -->

## まとめ

6/7/8/9の個別adapter計画が一巡したため、各RUNに残した未達事項を次期開発計画として整理しました。これにより、通常開発で続けるべき作業と、正式な正規化RUNへ進む前に判断すべき作業が分かれ、次のPRを迷わず切れる状態になります。

## 変更内容

- `docs/REMAINING_NORMALIZATION_PLAN_6_9.md` を追加
- 完了済みフェーズF-Iと追加対応の到達点を整理
- 次期開発K-Pを定義
- 次の推奨PRを `feat/table-record-review-6-7` と明記
- RUNに、おさらい・今回入れない課題・検証結果を記録

## 検証

```powershell
git diff --check
```

結果: 問題なし。

```powershell
rg -n "<local-path-pattern>" docs/REMAINING_NORMALIZATION_PLAN_6_9.md runs/20260526-005646660_docs-remaining-normalization-plan-6-9
```

結果: 該当なし。

## 備考

- このPRはドキュメント整備のみです。
- `data/normalized/` への昇格は行っていません。
