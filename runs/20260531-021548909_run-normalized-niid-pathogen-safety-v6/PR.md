# NIID病原体等安全管理規程 正規化RUN v6

## まとめ

NIID病原体等安全管理規程の正規化候補について、別表4/5の表構造を原表に合わせて再修正しました。別表4では存在しない便宜カテゴリを削除し、大項目だけの行と大項目/小項目を持つ行を区別しています。

## 主な変更

- 別表4から存在しない `位置・構造` カテゴリを削除。
- 別表4の大項目のみの行は `小項目=－` として保持。
- 別表4の `保管施設（庫）` 以降は大項目/小項目形式。ただし `感染動物の飼育設備` と `滅菌設備` は大項目のみ。
- 別表5は全行を大項目/小項目形式で保持。
- `TABLE4_5_RECONSTRUCTION_CHECK.md` で別表4/5をMarkdown表として再構成し、列数整合を確認。

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

詳細は `runs/20260531-021548909_run-normalized-niid-pathogen-safety-v6/STRUCTURE_TABLE_REVIEW.md` に記録しています。
別表4/5の組み上げ確認は `runs/20260531-021548909_run-normalized-niid-pathogen-safety-v6/TABLE4_5_RECONSTRUCTION_CHECK.md` に記録しています。

## 昇格

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_niid_pathogen_safety_management_20240401/` に複写します。

<!-- PR_BODY_FILE: runs/20260531-021548909_run-normalized-niid-pathogen-safety-v6/PR.md -->

