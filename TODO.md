# TODO

Current Branch: chore/setup

## Now（雛形）
- [ ] run: <new_run_id>_ir-schema
  - 法令・ガイドラインを共通IR（YAML）に正規化するスキーマを確定する
- [ ] run: <new_run_id>_pipeline-min
  - 生データ（PDF/HTML/TXT/XML等）からIR/YAMLへ変換する最小パイプラインを用意する

## Next（雛形）
- 祖先/文脈の出し分けルール（表示プロファイル）をYAMLで表現する

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
