# NIID病原体等安全管理規程 正規化RUN v5

## まとめ

NIID病原体等安全管理規程の正規化候補について、別表4/5の左端階層とカテゴリ割当を再修正しました。表として組み上げた場合に列がずれないことを、IR上のセル数とMarkdown表の列数で検査しています。

## 主な変更

- 別表4/5の左側を `大区分 / 中区分 / 基準` の3列に変更。
- 別表4の `実験室` 行、`実験室内` 行を追加。
- 別表5の `複数名での作業`、`安全キャビネット内での適切な使用` を `使用の基準` に修正。
- `TABLE4_5_RECONSTRUCTION_CHECK.md` で別表4/5をMarkdown表として全行再構成し、列数整合を確認。

## 検証

| 項目 | 結果 |
| --- | --- |
| goal check | PASS |
| special structure audit | PASS |
| structure check | PASS |
| focused tests | `13 passed` |
| full tests | `257 passed, 1 skipped` |
| 個人環境パス検査 | PASS |

## 目検レビュー

詳細は `runs/20260531-000950321_run-normalized-niid-pathogen-safety-v5/STRUCTURE_TABLE_REVIEW.md` に記録しています。
別表4/5の組み上げ確認は `runs/20260531-000950321_run-normalized-niid-pathogen-safety-v5/TABLE4_5_RECONSTRUCTION_CHECK.md` に記録しています。

## 昇格

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_niid_pathogen_safety_management_20240401/` に複写します。

<!-- PR_BODY_FILE: runs/20260531-000950321_run-normalized-niid-pathogen-safety-v5/PR.md -->

