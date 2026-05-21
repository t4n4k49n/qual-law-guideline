## まとめ

text2ir文書群をxml2ir最終正規化GOALと照合するため、代表文書の再生成・ギャップ分類結果を追加します。今後の長期実装に入る前に、profile調整で済む課題、text2ir共通更改が必要な課題、拡張入口として扱うべき課題を切り分けられる状態にします。

## 変更内容

- text2ir GOALチェックリストを追加
- text2ir現状機能棚卸しを追加
- 代表9文書の再生成結果サマリを追加
- 文書別ギャップ分類表を追加
- 表・注記・子孫表示の重点レビューを追加
- 今後の実装判断を追加

## 確認

- コード、profile、テスト、data/normalized は変更なし
- 代表9文書は `--qualitycheck --strict` exit 0
- 代表9文書は `verify_document` pass
- `runs/20260522-034415_text2ir-goal-gap-confirmation/` に個人環境の絶対パスが残っていないことを確認

<!-- PR_BODY_FILE: runs/20260522-034415_text2ir-goal-gap-confirmation/PR.md -->
