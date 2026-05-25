## まとめ

6/7/8/9の個別開発計画フェーズAとして、対象外OK範囲をParserではなくcandidate visibilityで制御するための文書別profileを追加しました。IRには対象範囲を残したまま、候補表示だけを文書別ルールで落とせるようにしています。

## 変更内容

- candidate visibility profileのロード・適用部品を追加
- `text2ir bundle` に `--candidate-visibility-profile-id` / `--candidate-visibility-profile` を追加
- 6/7/8/9向けの文書別candidate visibility profileを追加
- profile適用とmock-ui candidate visibilityロジックの結合テストを追加
- 個別adapter計画と4ファイルガイドへ利用方法を追記

## 個別と共通の整理

- 共通: profileをregdoc_profileへ適用する仕組みとCLIオプション。
- 個別: 対象外OKの具体的なNID範囲、用語集、表1、序論、定義、第5章、第6章などの判断。
- Parser profileには対象外OK範囲を入れていません。

## 検証

- `tests/test_candidate_visibility_profiles_6_9.py`: `6 passed`
- 関連回帰: `26 passed`
- 追加確認: `9 passed`
- 絶対パス混入チェック: 該当なし

## 次フェーズ

計画通り、PR承認後は8b「病原体等安全管理規程の別表・付表保持adapter」に進む想定です。

<!-- PR_BODY_FILE: runs/20260525-144814194_feat-candidate-visibility-profiles-6-9/PR.md -->
