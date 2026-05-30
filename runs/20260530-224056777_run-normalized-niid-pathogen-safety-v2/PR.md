# NIID病原体等安全管理規程 正規化RUN v2

## まとめ

NIID病原体等安全管理規程の正規化候補を作り直しました。v1では付表1-2、付表1-3などの番号付き項目が本文に潰れており、レビュー記録も不十分だったため、番号付き項目、表、heading、不要な本文連結を対象に再監査しています。

## 主な変更

- 付表1-2、付表1-3、別表6、別表9の番号付き項目を item ノードとして保持。
- 別表4、別表5、別表8の raw-hold 表で、`0.01％` や `1分` が item 化されないように修正。
- `註：` を note として扱い、本文に混ぜない。
- 別表1の導入文を heading ではなく text として復元。
- `。。`、本文内番号連結、raw-hold表の誤構造化を監査対象に追加。

## 検証

| 項目 | 結果 |
| --- | --- |
| goal check | PASS |
| special structure audit | PASS |
| structure check | PASS |
| focused tests | `8 passed` |
| full tests | `257 passed, 1 skipped` |
| 個人環境パス検査 | PASS |

## 目検レビュー

詳細は `runs/20260530-224056777_run-normalized-niid-pathogen-safety-v2/STRUCTURE_TABLE_REVIEW.md` に記録しています。
深い階層サンプルは `runs/20260530-224056777_run-normalized-niid-pathogen-safety-v2/SAMPLE_EXTRACT.md` に抽出しています。

重要確認点:
- 付表1-2: item 1-8
- 付表1-3: item 1-4
- 別表6: item 1-11
- 別表9: item 1-5
- 表ノード: 付表2、付表3、付表4、別表7、別表10
- raw-hold: 別表4、別表5、別表8

## 昇格

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_niid_pathogen_safety_management_20240401/` に複写します。

<!-- PR_BODY_FILE: runs/20260530-224056777_run-normalized-niid-pathogen-safety-v2/PR.md -->
