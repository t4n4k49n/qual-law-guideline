<!-- PR_BODY_FILE: runs/20260531-124738598_chore-track-vscode-settings-v2/PR.md -->

## まとめ
VS Codeのワークスペース設定をリポジトリで共有できるようにし、同じ表示・Python仮想環境設定を複数環境で再利用できる状態にします。

## 変更内容
- `.gitignore` から `.vscode/` の除外を削除
- `.vscode/settings.json` を追跡対象に追加
- 作業記録としてRUN文書を追加

## 確認
- local_notes境界ガード、制御文字ガード、PR本文ガードの対象条件を確認
- 既存の作業中差分は本PR対象外

## 注意
既にローカルに未追跡の `.vscode/settings.json` がある環境では、pullまたはmerge時にGitが上書きを拒否する可能性があります。その場合はローカルの `.vscode/settings.json` を退避してから再実行してください。
