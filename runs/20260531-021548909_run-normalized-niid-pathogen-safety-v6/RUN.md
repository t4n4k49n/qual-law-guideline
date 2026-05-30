# RUN: NIID病原体等安全管理規程 正規化RUN v6

## 目的

別表4/5について、原表に存在しない便宜カテゴリを除き、事実に基づく大項目/小項目構造へ修正する。

## 入力

- source text: `data/human-readable/niid/pathogen_safety_management/source_texts/Kanrikitei3_20240401.txt`
- source PDF: `https://www.niid.go.jp/niid/images/cepr/kanrikitei/Kanrikitei3_20240401.pdf`
- doc_id: `jp_niid_pathogen_safety_management_20240401`

## 修正内容

- 別表4から存在しない `位置・構造` カテゴリを削除。
- 別表4は `対象病原体等BSL` から `実験室まで通行制限` までを大項目のみ、小項目 `－` として保持。
- 別表4は `保管施設（庫）` 以降を大項目/小項目形式で保持。ただし `感染動物の飼育設備` と `滅菌設備` は大項目のみ、小項目 `－`。
- 別表5は全行を大項目/小項目形式で保持。
- 別表4/5のMarkdown再構成表を `TABLE4_5_RECONSTRUCTION_CHECK.md` に出力し、列数整合を確認。

## 検証

- goal check: PASS
- special structure audit: PASS
- structure check: PASS
- focused tests: `13 passed`
- full tests: `257 passed, 1 skipped`
- 個人環境パス検査: PASS

## 昇格方針

この親PRでは `data/normalized/` は変更しない。承認後、子PRで `promotion_candidate/` の4ファイルのみを `data/normalized/jp_niid_pathogen_safety_management_20240401/` に複写する。

