## まとめ

txtconcat生成物をGit管理対象から外し、今後の作業ツリーに一時結合ファイルが残り続けないようにします。

## 変更内容

- `.gitignore` に `txtconcat_*.*` を追加
- このRUN記録を追加

## 確認

- 変更対象は `.gitignore` とRUN記録のみ
- `data/normalized/` は変更していません

<!-- PR_BODY_FILE: runs/20260522-153634337_ignore-txtconcat-files/PR.md -->
