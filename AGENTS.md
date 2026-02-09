# AGENTS.md

このリポジトリは最小ドキュメントで運用する。
迷ったら README.md / TODO.md / KNOWLEDGE.md と Git履歴を最優先する。

## 作業開始時に読む順（必須）
1) README.md
2) TODO.md（上から順に）

## 重要：文字化け回避（必須）
- このrepoのテキストファイル（.md / .py / .json など）は UTF-8（BOMなし）で保存すること
- 改行は原則LF
- 生成物（out配下のログ/JSON）も原則UTF-8で出力すること

## 運用ルール（必須）
- 1タスク = 1run（1runは小さく完結）
- コード修正を伴うタスクは必ずブランチ（main直編集禁止）
- 初期RUNの run_id は固定：`YYYYMMDD_000000000_setup`
- 開発RUNの run_id は `yyyymmdd-hhmmssSSS_<branch>`（ブランチ名に `/` が入る場合は `-` に置換）
- `runs/<run_id>/` と `out/<run_id>/` は同名で作る（同期できるように）
- 出力・ジャーナル類は上書き禁止：必ずタイムスタンプを付けて増やす
- `out/` はローカル生成物（gitignore想定）。共有したい抜粋ログ/成果は `runs/<run_id>/` にコピーする
- 解決に手間がかかった・繰り返す知見は KNOWLEDGE.md に昇格（RUN → KNOWLEDGE）
- 破壊的操作・秘密情報（.env / credential / rm / 大量削除 等）は都度確認してから
- 余分なrunは削除せず、必要なら `runs/ARCHIVE_<run_id>/` に移動して保管（任意だが推奨）

## 正規化RUN（Normalized Run）
- 正規化RUNは、`data/normalized/` へ正式版を昇格させるための特別RUNを指す。
- 指示で「正規化RUN」または「正規化ラン」「normalized run」と指定された場合、`docs/NORMALIZED_RUN_PLAYBOOK.md` に従って実行する。なお、必ず「7) 正式版への昇格（文書コミット）」まで実施すること。
- `data/normalized/` への複写はPR承認確認後にのみ行う（承認前の複写は禁止）。
- PR本文（`runs/<run_id>/PR.md`）は承認時点の内容で固定し、承認後の昇格実績は `RUN.md` のみに追記する。
- `data/normalized/` の退避命名は `ARCHIVE_<doc_id>` を使用し、同名が既にある場合は `ARCHIVE_<doc_id>_2`, `ARCHIVE_<doc_id>_3` のように連番を付与する。

## README/TODOの埋め方（重要）
- README.md と TODO.md はプロジェクト内容に依存するため、最初は雛形のみを作る。
- 5ファイル作成後、ユーザーに以下のいずれかを依頼し、情報が揃ってから追記する（勝手に埋めない）：
  - プロジェクト内容が分かる資料のアップロード（要件/メモ/仕様/リンク等）
  - または、目的・入力・出力・制約・対象ユーザー・優先度の要点共有
