# RUN: 機密情報（ユーザー名）混入箇所の総点検

- run_id: 20260209-165925717_chore-redact-personal-paths
- branch: chore/redact-personal-paths
- date: 2026-02-09 16:59:25 +09:00
- status: 実施済み（置換完了・PR作成済み）

## 目的
- ローカルとリモートの両方を同じ優先度で対象化し、`<username>` を含む記述を駆逐する。

## スコープ（並列）
- ローカル: 作業ツリー上の実ファイル
- リモート: `origin/*` 全ブランチ（`origin/HEAD` 除外）

## 実施コマンド
```powershell
# local
rg -n -i --glob "*.md" "<username>"
rg -n -i "<username>"

# remote
git fetch origin --prune
git for-each-ref refs/remotes/origin
git grep -n -I -i "<username>" <remote-ref>
```

## 検出結果（ローカル）
- 方針確定時点の検出対象（16件）:
1. docs/NORMALIZED_RUN_PLAYBOOK.md:19
2. runs/20260204_000000000_setup/RUN.md:17
3. runs/20260206-111530177_run-xml2ir-336M50000100002/RUN.md:9
4. runs/20260206-122710668_run-normalized-run-playbook/RUN.md:10
5. runs/20260206-153010_run-normalized-gmp-ordinance/RUN.md:8
6. runs/20260206-180426878_run-normalized-335AC0000000145/RUN.md:19
7. runs/20260206-180426878_run-normalized-335AC0000000145/PR.md:21
8. runs/20260207-153154910_run-normalized-336M50000100002-v2/RUN.md:5
9. runs/20260207-153154910_run-normalized-336M50000100002-v2/PR.md:7
10. runs/20260207-153733372_run-normalized-336M50000100002-v2-rerun/RUN.md:5
11. runs/20260207-153733372_run-normalized-336M50000100002-v2-rerun/PR.md:8
12. data/normalized/jp_egov_335AC0000000145_20260501_507AC0000000037/jp_egov_335AC0000000145_20260501_507AC0000000037.meta.yaml:54
13. data/normalized/jp_egov_336CO0000000011_20260501_507CO0000000362/jp_egov_336CO0000000011_20260501_507CO0000000362.meta.yaml:54
14. data/normalized/jp_egov_336M50000100001_20260501_507M60000100117/jp_egov_336M50000100001_20260501_507M60000100117.meta.yaml:54
15. data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/jp_egov_336M50000100002_20260501_507M60000100117.meta.yaml:54
16. data/normalized/jp_egov_416M60000100179_20260501_507M60000100117/jp_egov_416M60000100179_20260501_507M60000100117.meta.yaml:54

## 検出結果（リモート）
- 対象: `origin/*` 41ブランチ
- 検出行数: 459
- ヒットしたリモートブランチ数: 41
- `origin/main` のヒット数: 16
- 詳細一覧（全行）: `out/20260209-165925717_chore-redact-personal-paths/20260209-170138060_remote_keyword_hits.tsv`

### リモートヒット数上位（Top 10）
- origin/fix/promote-approved-normalized-main-sync: 20件
- origin/run/normalized-336M50000100001-v3: 20件
- origin/run/normalized-336CO0000000011-v3: 19件
- origin/run/normalized-416M60000100179-v3: 19件
- origin/run/normalized-335AC0000000145-v3-rerun: 18件
- origin/chore/playbook-no-promotion-note-in-pr: 18件
- origin/chore/playbook-normalized-note-sync: 18件
- origin/docs/normalized-pr-text-policy: 18件
- origin/fix/ord-absolute-order: 17件
- origin/run/normalized-336M50000100002-v3: 17件

## 置換方針（文脈別）
- 実行コマンド（PowerShell文脈）: `%USERPROFILE%\...` -> `$env:USERPROFILE\...`
- 説明文・手順・PR本文（シェル非依存/CMD互換）: `%USERPROFILE%\...` -> `%USERPROFILE%\...`
- meta.yamlの入力元path（可搬性重視）: `%USERPROFILE%\...` -> `%USERPROFILE%\...`

## 置換前後サマリ

### ファイル数ベース（4象限）
| 区分 | PowerShell置換 (`$env:USERPROFILE`) | 非PowerShell置換 (`%USERPROFILE%`) | 両方混在 |
|---|---:|---:|---:|
| ローカル（実ファイル） | 3 | 14 | 0 |
| リモート（branch+file単位） | 93 | 366 | 0 |

- 補足: ローカル実ファイルは対象17ファイルすべてで、`%USERPROFILE%\...` のヒットは各ファイル1件のみ（同一ファイル内の複数ヒットなし）。
- 補足: リモートをブランチ重複除外のユニークファイルパスで集計すると、PowerShell置換 3 / 非PowerShell置換 18 / 混在 0 / 合計 21。

### 置換数ベース（4象限）
| 区分 | PowerShell置換 (`$env:USERPROFILE`) | 非PowerShell置換 (`%USERPROFILE%`) | 合計 |
|---|---:|---:|---:|
| ローカル（置換行数） | 3 | 16 | 19 |
| リモート（置換行数） | 93 | 366 | 459 |

- 置換後（予定）: ユーザー名 `<username>` を含む絶対パスを環境変数ベース表記に統一。

## 次アクション
- ローカル置換（19行）を方針どおり実施
- リモート側は本ブランチで対処可能範囲を先行修正し、残分は対象ブランチへ展開方針を決定
- `rg -n -i "<username>"` と `git grep -n -I -i "<username>" origin/main` の再検証
- 差分確認後にコミット
## 実施結果
- ローカル実ファイルの置換を実施し、`<username>` は作業ツリー（`.git`除外）で0件。
- ブランチ `chore/redact-personal-paths` をリモートへpush済み。
- PR作成: https://github.com/T4N4K4-KUN/qual-law-guideline/pull/44

## 検証結果（最新）
- `rg -n -uu -g "!.git" -i "<username>"` => 0件
- `git grep -n -I -i "<username>" origin/chore/redact-personal-paths` => 0件
- `git grep -n -I -i "<username>" origin/main` => 16件（PR #44 未マージ分）