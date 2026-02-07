## 概要

正規化RUN時の個人環境情報（`C:\Users\...`）漏洩を防ぐため、RUNBOOKとチェックリストに明示ルールを追加しました。

## 変更内容

- `docs/NORMALIZED_RUN_PLAYBOOK.md`
  - `RUN.md` / `PR.md` / PR本文に `C:\Users\...` を書かないルールを追加
  - `%USERPROFILE%` またはワークスペース相対パスを使うルールを追加
  - PR作成前に `C:\\Users\\` 検索で0件確認する手順を追加
- `docs/NORMALIZED_RELEASE_CHECKLIST.md`
  - 個人環境絶対パスが含まれていないことをチェック項目に追加

## 期待効果

- 承認済みPR本文やRUN記録へのローカル環境情報混入を予防
- 正規化RUNのレビュー手順にセキュリティ観点を標準化
