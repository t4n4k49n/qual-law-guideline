## まとめ

6「原薬GMPガイドライン」の正規化候補を作成しました。共通の日本語 `text2ir` 基盤を使いつつ、API GMP固有の冒頭通知・目次・表1の扱いをRUN内に閉じ、`data/normalized/` へはまだ反映していません。

## 対象

- 文書: 原薬GMPのガイドライン
- ソース: `https://www.pmda.go.jp/files/000156438.pdf`
- 原ソースTXT: `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt`
- 整形済み入力: `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/input/000156438_table1_markdown.txt`

## 変更内容

- API GMP専用parser profile `jp_pmda_api_gmp_guideline_v1` を追加
- 表1のみRUN内で1列markdown tableへ整形し、IRではtable rowとして保持
- 正規化候補4ファイルとmanifestを `promotion_candidate/` に生成
- 採用しなかった共通parser拡張案を `ADAPTER_NOTES.md` に記録

## 検証結果

- `pytest`: `41 passed`
- `goal_check --mode promotion`: `PASS`
- `special_structure_audit --mode promotion`: `pass`
- `verify_document`: `pass`

## 深い階層サンプル

本文:

`document/root` → `chapter cha3`（3 従業員） → `paragraph cha3.p3_10`（3.10）

該当テキスト:

`中間体・原薬の生産を実施し監督するために、適切な教育訓練を受け、又は経験を有する適任者を適切な人数配置すること。`

表1:

`document/root` → `chapter cha1`（1 序文） → `paragraph cha1.p1_3`（1.3 適用範囲） → `table cha1.p1_3.tbl1` → `table_row cha1.p1_3.tbl1.tblh1.tblr1`

## 補足

このPRは親PRです。承認後、別ブランチで `promotion_candidate/` から `data/normalized/jp_pmda_api_gmp_guideline_20011102/` への昇格専用PRを作成します。

<!-- PR_BODY_FILE: runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/PR.md -->

