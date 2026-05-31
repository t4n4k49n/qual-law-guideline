# RUN

- run_id: `20260531-124738598_chore-track-vscode-settings-v2`
- base branch: `run/normalized-mhlw-csv-guideline-v3`
- work branch: `chore/track-vscode-settings-v2`
- task: `.vscode/settings.json` をGit追跡対象にして共有する

## 実施内容
- `.gitignore` から `.vscode/` の除外を削除する。
- `.vscode/settings.json` を追跡対象に追加する。
- `workbench.colorCustomizations` の赤系配色を全環境で共有する設定として含める。
- PR本文ガードに備え、同run内に `PR.md` を用意する。

## 注意点
- 既存作業中の `src/` 差分や別runの未追跡ファイルは本コミットに含めない。
- 既に各作業者のローカルに未追跡の `.vscode/settings.json` がある場合、マージまたはpull時に「untracked working tree file would be overwritten」で止まる可能性がある。その場合はローカル設定を退避してから再実行する。
