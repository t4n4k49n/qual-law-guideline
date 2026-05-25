## まとめ

病原体等安全管理規程向けのParser開発として、本文条文を対象にした専用 `text2ir` profile と実データテストを追加しました。正式な正規化処理や `data/normalized/` への昇格ではなく、まず第1章から第6章までの本文条文を安定して解析できることを確認する段階です。

## 変更内容

- `jp_niid_pathogen_safety_management_v1` profileを追加
- 表紙、序文、目次を本文開始前として除外
- 8a本文Parser開発として、`別表１` 以降を対象外にする境界を専用profileに追加
- 条文内の裸数字段落と丸括弧番号を、この文書の階層に合わせて専用profile側で扱うように追加
- 任意profileで終端までskipできる汎用 `skip_to_eof` をParserに追加
- 実データに基づくテストを追加

## 個別と共通の整理

- 共通: `skip_to_eof` は文書名を含まない汎用機能で、profileが明示した場合だけ有効です。
- 個別: 表紙・序文・目次・別表境界、丸括弧番号の階層変更、裸数字段落の扱いは `jp_niid_pathogen_safety_management_v1` に閉じています。
- 保留: 別表・付表の構造化は次フェーズで個別adapter候補として扱い、今回の共通処理には入れていません。

## 検証

- 実データbundle: 成功、qualitycheck warningなし
- `goal_check --mode normal`: `PASS`
- `special_structure_audit --mode normal`: `pass`
- 関連回帰テスト: `48 passed`

## 残課題

別表・付表は今回の本文Parserから除外しています。次フェーズでは `別表１` 以降を対象に、まず保持形を確認し、必要な範囲だけ個別adapter化する計画です。

<!-- PR_BODY_FILE: runs/20260525-135841668_feat-niid-pathogen-safety-parser-v1/PR.md -->
