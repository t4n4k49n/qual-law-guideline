## 概要
- チェック項目選択画面に表示するしないを設定で変更可能にした。内部的には`candidate_visibility`（allow/deny、deny優先）と呼ばれる機構。
- これに伴い、正規化RUNも対応。生成系（xml2ir/text2ir）の `regdoc_profile` 既定値へ `candidate_visibility` を追加。成果物での標準項目とした。

## 変更内容
- *profile.yaml
  - `allow_rules`/`deny_rules` を設定可能化（具体的には下記のモックUI/生成系ロジックとして具備）
- モックUI
  - `candidate_visibility` 判定ロジックを追加（`allow_rules`/`deny_rules`、deny優先）
  - 左候補一覧へ反映し、設定確認欄にも表示
- 生成系
  - `src/qai_xml2ir/models_profiles.py`
  - `src/qai_text2ir/cli.py`
  - 既定 `dq_gmp_checklist` に以下を追加
    - `candidate_visibility.allow_rules: []`
    - `candidate_visibility.deny_rules: []`
- テスト
  - `tests/test_mock_ui_candidate_visibility.py` を追加
  - 生成系の既存テストに `candidate_visibility` 既定値検証を追加
- モック設定
  - `data/mock_ui/display_examples.yaml` の表示例2を custom profile 化
  - `data/mock_ui/profiles/example2_candidate_visibility_default.yaml` を追加
- ドキュメント
  - `docs/NORMALIZED_RUN_OUTPUT_4FILES_GUIDE.md` に `candidate_visibility` を追記
  - `docs/NORMALIZED_RUN_PLAYBOOK.md` に正規化チェック観点を追記

## 動作確認
- `.venv\Scripts\python.exe -m pytest tests/test_mock_ui_candidate_visibility.py -q`
- `.venv\Scripts\python.exe -m pytest tests/test_mock_ui_render.py -q`
- `.venv\Scripts\python.exe -m pytest tests/test_xml2ir_profiles_table_context.py -q`
- `.venv\Scripts\python.exe -m pytest tests/test_text2ir_bundle.py -q`
- `.venv\Scripts\python.exe -m pytest tests/test_bundle_gmp.py -q`

## まとめ
左側候補の可視性制御をプロファイルで宣言できるようにしつつ、生成物・テスト・運用ドキュメント・モック設定を同時に揃えました。これにより、候補表示要件の変更をコード修正ではなくプロファイル差し替え中心で進められる状態になり、正規化RUN成果物とモック検証の整合も維持しやすくなります。

<!-- PR_BODY_FILE: docs/pr_bodies/pr-candidate-visibility.md -->

