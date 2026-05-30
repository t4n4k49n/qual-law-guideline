# NIID病原体等安全管理規程 正規化RUN v4

## まとめ

NIID病原体等安全管理規程の正規化候補を、表全件の目検レビュー前提で作り直しました。前候補では別表4、別表5、別表8を raw-hold として扱っており、表の正規化として不十分だったため、全表を table/table_header/table_row として確認できる形に改めています。

## 主な変更

- 付表2の table heading が途中で切れていた問題を修正。
- 別表4、別表5、別表8を raw text ではなく visual reviewed table として復元。
- 付表2、付表3、付表4、別表4、別表5、別表7、別表8、別表10を全て表レビュー対象として記録。
- 付表1-2、付表1-3、別表6、別表9の番号付き項目分割を維持。
- `註：`、孤立 `。`、`。。`、本文内番号連結、表中数値の誤item化を監査。

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

詳細は `runs/20260530-233420456_run-normalized-niid-pathogen-safety-v4/STRUCTURE_TABLE_REVIEW.md` に記録しています。
深い階層サンプルは `runs/20260530-233420456_run-normalized-niid-pathogen-safety-v4/SAMPLE_EXTRACT.md` に抽出しています。

## 昇格

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_niid_pathogen_safety_management_20240401/` に複写します。

<!-- PR_BODY_FILE: runs/20260530-233420456_run-normalized-niid-pathogen-safety-v4/PR.md -->

