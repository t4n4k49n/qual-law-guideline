# TODO

Current Branch: feat/repo-structure

## Now（雛形）
- [x] run: 20260211-021901686_test-text2ir-cfr-realfile-rerun-20260211
  - `(c)` alpha/roman 競合問題を発見時と同条件でrerunし、現行mainで再現確認を完了
- [ ] run: <new_run_id>_ir-schema
  - 法令・ガイドラインを共通IR（YAML）に正規化するスキーマを確定する
- [ ] run: <new_run_id>_pipeline-min
  - 生データ（PDF/HTML/TXT/XML等）からIR/YAMLへ変換する最小パイプラインを用意する

## Next（雛形）
- 祖先/文脈の出し分けルール（表示プロファイル）をYAMLで表現する
- 参照ドキュメントを根拠にIRスキーマの確定版を作る
- コードと出力を同時に版管理する構成（シンプル案）のリポジトリ作成
- PR本文文字化けの恒久対策を実装する（将来実施）
  - `pull_request_target` でPR本文をAPI取得し、`\\n` 生文字列や `�` を検査する
  - PR本文に `<!-- PR_BODY_FILE: ... -->` を必須化し、本文ファイルと一致検証する
  - Branch protection で上記チェックを必須化し、fail時はマージ不可にする
  - 背景: PR #120 でPR本文の文字化け/改行崩れが再発した

## Notes（固定）
- TODO.md は上書き更新する。履歴は Git のコミットで追える（重要な更新はコミットに含める）。
- 1タスク=1run（runs/<run_id>/RUN.md）
- runs と out は同名運用
- 生成物は上書き禁止（タイムスタンプ付与）
- 詰まりが再発する知見は KNOWLEDGE.md に昇格

---

## TODO を具体化するためにユーザーへ依頼する情報（必須）
- 最初に作るべき最小機能（Step 1/2/3 のどこから始めるか）
- 対象のデータ例（あれば）
- 成功判定（出力例、許容誤検出など）
