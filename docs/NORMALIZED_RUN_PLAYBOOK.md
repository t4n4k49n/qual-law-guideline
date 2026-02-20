# NORMALIZED RUN PLAYBOOK

正規化RUN（normalized run）専用の最小手順。
目的は `runs/<run_id>/promotion_candidate/` をレビューし、承認後に `data/normalized/<doc_id>/` へ確実に昇格すること。

## 0) 前提

- 入力はXMLのみを前提とする。
- 昇格候補の正本は `runs/<run_id>/promotion_candidate/` に置く（Git追跡対象）。
- `out/<run_id>/` は正規化RUNでは必須ではない（必要時の補助出力）。
- 正式版へ昇格する前に、レビューと検証の記録を残す。
- PRは「親PR + 子PR（昇格専用）」の2段で運用する。

## 1) 実行前確認

- 対象の入力XMLパスを確認
- **出力差分の管理方針（必須）**:
  - `schema` が同一でも、`qai_xml2ir` のパーサ実装や profile 変更により出力内容は変わり得る
  - table/note 拡張のような変更は「スキーマ改定」ではなく「パーサ/プロファイル改定」として扱う
  - 正規化RUNでは `schema` の一致だけで同一性を判断しない
- **機密情報対策（必須）**:
  - `RUN.md` / `PR.md` / PR本文に、`C:\Users\...` などの個人環境の絶対パスを書かない
  - パスは `%USERPROFILE%` などの環境変数表記、または `<workspace-relative-path>` を使う
  - 例:
    - NG: `%USERPROFILE%\Documents\...`
    - OK: `%USERPROFILE%\Documents\...`
- `doc_id` を決める
  - **e-GovのURIに準拠**: `jp_egov_<law_id>_<as_of(yyyymmdd)>_<revision_id>`
  - 例: `https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117` → `jp_egov_336M50000100002_20260501_507M60000100117`
- ブランチ名と `run_id` を決める
- 正規化RUNのPRブランチは `run/normalized-...` 命名を使用する（CI判定キー）。
- 使用する実行環境を固定する
  - 推奨: `.venv` を利用し、Python と依存パッケージをプロジェクト単位で固定する
  - 例: `.venv\Scripts\python.exe -m pip install -e .[dev]`

## 2) 実行

例:
```bash
xml2ir bundle --input <path-to-xml> --out-dir runs/<run_id>/promotion_candidate --doc-id <doc_id> --emit-only all
```

実行時に以下を `runs/<run_id>/RUN.md` または `runs/<run_id>/promotion_candidate/manifest.yaml` へ記録する:
- `schema`（例: `qai.regdoc_ir.v3`）
- `parser_profile.id`（出力 `*.parser_profile.yaml` の `id`）
- `tool_version`（取得できる場合）
- 実行Python（例: `.venv\Scripts\python.exe`）
- 主要依存バージョン（最低: `lxml`, `PyYAML`, `typer`）

## 3) エラーハンドリング（最小）

- XMLのパス誤り → パスを修正して再実行
- 出力が欠けている → 再実行し、RUNに理由を記載
- 例外が出る → 例外ログを `runs/<run_id>/RUN.md` に記録し、作業停止

## 4) リリース確認（正規化チェック）

### 4-1) スキーマ検証（最小）

- `verify.py` の最小チェックを実行し、結果を記録
  - `assert_unique_nids`
  - `check_annex_article_nids`
  - `check_appendix_scoped_indices`
  - `check_ord_format_and_order`（ord存在/一意/単調増加）

### 4-2) AIレビュー（目視代替）

- IRからサンプル断片を抽出し、AIに評価させる
- 出力は RUN に貼り付け、**人の最終確認はPRで行う前提**と明記する

### 4-3) PRでの最終目視（人間）

- 正規化出力が壊れていないことを主眼に確認する
- 比較は「前回との差分説明」ではなく「今回の出力が成立しているか」の確認を優先する
- 深い階層サンプルは1件以上提示し、祖先経路を省略しない

## 5) manifest.yaml の作成

- `runs/<run_id>/promotion_candidate/manifest.yaml` を作成
- 入力元・コマンド・コミットハッシュ・検証/レビュー結果を記録
- 追加で以下も記録する:
  - `schema`
  - `parser_profile.id`
  - `tool_version`（未設定なら未設定である旨）
  - 実行環境（Python実行ファイル、主要依存バージョン）

## 6) 親PR作成（レビューPR）

- 親PR本文は `runs/<run_id>/PR.md` に作成する
- **PR.md のタイトルと表の見出しは日本語で書く**
- 親PRには以下のみ含める:
  - `runs/<run_id>/promotion_candidate/`（4ファイル + manifest）
  - `runs/<run_id>/RUN.md`
  - `runs/<run_id>/PR.md`
- 親PRでは `data/normalized/` を変更しない
- 親PR本文に以下を必ず記載する:
  - 対象e-Gov法令URL（`https://laws.e-gov.go.jp/law/<law_id>/<as_of_revision>`）
  - 検証結果
  - 深い階層サンプル（祖先省略なし）
- PR作成前に、本文・`RUN.md`・`PR.md` から `C:\\Users\\` を検索し、0件であることを確認する
- GitHubで親PRを作成し、リンクを共有する
- 親PR本文には昇格実施結果を書かない

## 7) 子PR作成（昇格専用）

- **親PRの承認確認後にのみ** 子PRを作成する
- 子PRの変更は昇格複写のみ:
  - `runs/<run_id>/promotion_candidate/*` → `data/normalized/<doc_id>/`
  - 4ファイル（`regdoc_ir` / `parser_profile` / `regdoc_profile` / `meta`）
- 子PRに含めてよい追記:
  - `runs/<run_id>/RUN.md` の昇格記録（commit id / 反映確認）
- 子PRに含めないもの:
  - パーサコード修正
  - 追加の正規化再実行
  - 無関係なドキュメント更新

## 8) 昇格完了判定

- 子PRが `main` に反映済みであることを確認する
- 必須コマンド:
  - `git rev-parse --verify <promotion_commit>`
  - `git fetch origin`
  - `git merge-base --is-ancestor <promotion_commit> origin/main`
- 条件を満たさない場合は完了報告しない
