# RUN

- run_id: `20260208-020954085_docs-runbook-path-masking`
- branch: `docs/runbook-path-masking`
- task: `正規化RUNの手順書に個人環境パス漏洩防止ルールを追加`

## Changes

- `docs/NORMALIZED_RUN_PLAYBOOK.md`
  - `C:\Users\...` の絶対パスを禁止し、`%USERPROFILE%` / 相対パスを使う規則を追加
  - PR前に `C:\\Users\\` 検索で0件確認する手順を追加
- `docs/NORMALIZED_RELEASE_CHECKLIST.md`
  - 個人環境絶対パス非含有のチェック項目を追加
