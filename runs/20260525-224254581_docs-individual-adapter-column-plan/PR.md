<!-- PR_BODY_FILE: runs/20260525-224254581_docs-individual-adapter-column-plan/PR.md -->

## まとめ

6/7/8/9の個別adapterで残した列復元・意味正規化・ソース補完の対象を棚卸しし、次に着手する順序を明確にしました。保持済みの表から安全に列復元へ進めるものと、先に分類やソース確認が必要なものを分けたため、以降の実装PRで個別最適が混ざりにくくなります。

## 変更内容

- `docs/INDIVIDUAL_ADAPTER_COLUMN_RESTORATION_PLAN.md` を追加
- 6/7/8/9の積み残しを、列復元対象・表別分類対象・ソース補完対象に分類
- 次PRを `feat/raw-line-table-column-restore-prototype` とし、6/7のraw_line tableから始める方針を明記
- RUNに、今回入れない課題と次PRの完了条件を記録

## 検証

```powershell
git diff --check
```

結果: 問題なし

## 補足

- このPRは開発計画PRであり、正式な正規化RUNではありません。
- `data/normalized/` への昇格は行っていません。
- 実際の列復元実装は次PRで扱います。
