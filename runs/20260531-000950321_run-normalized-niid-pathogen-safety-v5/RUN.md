# RUN: NIID病原体等安全管理規程 正規化RUN v5

## 目的

別表4/5の左端階層とカテゴリ割当を再修正し、Markdown表として組み上げた場合の列数整合まで確認する。

## 入力

- source text: `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- source PDF: `https://www.niid.go.jp/niid/images/cepr/kanrikitei/Kanrikitei3_20240401.pdf`
- doc_id: `jp_niid_pathogen_safety_management_20240401`

## 修正内容

- 別表4/5の左側を `大区分 / 中区分 / 基準` の3列に変更。
- 別表4の `実験室` 行、`実験室内` 行を表レコードとして追加。
- 別表5の `複数名での作業`、`安全キャビネット内での適切な使用` を `使用の基準` に修正。
- 別表4/5をMarkdown表として再構成し、全行の列数が揃うことを確認。

## 検証

- goal check: PASS
- special structure audit: PASS
- structure check: PASS
- focused tests: `13 passed`
- full tests: `257 passed, 1 skipped`
- 個人環境パス検査: PASS

## レビュー記録

- `STRUCTURE_TABLE_REVIEW.md`
- `TABLE4_5_RECONSTRUCTION_CHECK.md`
- `GOAL_CHECK.md`
- `SPECIAL_STRUCTURE_AUDIT.md`

## 昇格方針

この親PRでは `data/normalized/` は変更しない。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_niid_pathogen_safety_management_20240401/` に複写する。

