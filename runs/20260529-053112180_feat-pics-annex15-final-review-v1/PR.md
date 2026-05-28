## まとめ

PIC/S PE 009-17 Annex 15 の正規化RUN前に、目検最終チェックと校正を行いました。Table/Warning由来の未解決構造がないことを確認し、見出し誤結合を1件修正したため、次の正規化RUNでレビュー差し戻しになりやすい論点を先に減らしています。

## 変更内容

- Annex 15の `5. PROCESS VALIDATION` に続く `General` が見出しへ誤結合される問題を修正
- `merge_structural_heading_continuations` に `deny_next_regexes` を追加し、プロファイル側でTitle Case小見出しを除外可能にした
- Annex 15プロファイルの回帰テストを追加
- 目検結果、特殊構造監査、昇格チェック、深い階層サンプルをRUN成果物として保存

## 確認結果

| 項目 | 結果 |
|---|---|
| Annex 15 focused tests | `4 passed` |
| Full pytest | `252 passed, 1 skipped` |
| promotion goal check | PASS |
| special structure audit | PASS |
| Table/Warning scan | unresolved none |

## 成果物

- `runs/20260529-053112180_feat-pics-annex15-final-review-v1/RUN.md`
- `runs/20260529-053112180_feat-pics-annex15-final-review-v1/FINAL_REVIEW.md`
- `runs/20260529-053112180_feat-pics-annex15-final-review-v1/SAMPLE_EXTRACT.md`
- `runs/20260529-053112180_feat-pics-annex15-final-review-v1/GOAL_CHECK_PROMOTION.md`
- `runs/20260529-053112180_feat-pics-annex15-final-review-v1/SPECIAL_STRUCTURE_AUDIT.md`

<!-- PR_BODY_FILE: runs/20260529-053112180_feat-pics-annex15-final-review-v1/PR.md -->
