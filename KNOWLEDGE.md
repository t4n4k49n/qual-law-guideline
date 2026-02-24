# KNOWLEDGE

このファイルは「解決に手間と時間を要した」「過去から繰り返されている」知見を、
一般化して再利用するための置き場。

## いつ書くか（昇格基準）
- 原因特定に時間がかかった（見つけにくい/再現しづらい）
- 仕様/前提を変更・撤回した（方針転換があった）
- ログの取り方・計測方法・可視化方法が確定した
- 以後のrunでも同じ手順が必要（定石化した）
- 運用手順が変わった（やる/やらないのルール化）

## 書き方（テンプレ）
## YYYY-MM-DD: タイトル
- 症状：
- 原因：
- 対処：
- 再発防止：
- 確認コマンド：
- 参考run：`runs/<run_id>/RUN.md`

## 参照資料
- `docs/REFERENCE.md`

## 2026-02-24: eGov parser のfoldが Article/Paragraph構造を畳み替える
- 症状：
  - 同一法令内で、第一条は `article -> paragraph(1) -> item` なのに、第二条/第五条は `article(textあり) -> item` となり、UIの表示ルール（OFF時は常に分離）が崩れる。
- 原因：
  - `src/qai_xml2ir/egov_parser.py` の `parse_article` に foldロジックがあり、特定条件で `ParagraphSentence` を `article.text` に昇格し、`paragraph` ノード生成を省略する。
  - 条件: `Paragraph` が1件、`ParagraphNum` 空、`Paragraph@Num` が `None|\"\"|\"1\"`。
- 対処：
  - 次回本修正では fold廃止を第一候補とし、常に `paragraph` を生成して XML構造を保持する。
- 再発防止：
  - パーサ単体テストで `art2/art5` の `paragraph(1)` 生成を固定検証する。
  - UIテストで OFF/ON（分離/統合）を `art1/art2/art5` 横断で検証する。
- 確認コマンド：
  - `rg -n \"parse_article|fold|ParagraphNum|ParagraphSentence\" src/qai_xml2ir/egov_parser.py`
  - `rg -n -- \"nid: art2|nid: art5|text:\" data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml`
- 参考run：
  - `runs/20260220-201744501_run-normalized-336M50000100002-v1/RUN.md`
  - 詳細設計メモ: `out/20260224_060853115_egov_fold_root_cause_and_fix_spec.txt`

## 2026-02-20: Python実行は`.venv`固定にする（運用計画）
- 症状：
  - テスト実行時に`python -m pytest`がグローバルPythonを参照し、`.venv`に入っている依存（例: `lxml`）を見失う。
- 原因：
  - 「`.venv`を使う」ルールが文書ベースのみで、コミット前に機械的に強制する仕組みが無かった。
- 対処：
  - 当面は実行コマンドを明示して回避する。
  - 例：`.\.venv\Scripts\python.exe -m pytest ...`
- 再発防止：
  - 次ブランチで以下を実装する。
  - `pre-commit`で`.venv`外実行を検出してコミット前に失敗させる（主防衛線）。
  - 失敗時は「違反理由」と「正しいコマンド」を固定文で表示する。
  - CIは同一チェックを実行する最終防壁として維持する。
- 確認コマンド：
  - `.\.venv\Scripts\python.exe -m pytest tests/test_egov_table_payload_header_inference.py`

## 2026-02-20: 制御文字混入（文字化け要因）の検出強化は次ブランチで実施
- 症状：
  - RUN/PR文書に制御文字（例: BEL, NUL）が混入し、GitHub表示で文字化けが発生した。
- 原因：
  - 既存チェックは双方向制御文字（Bidi）中心で、一般制御文字の混入検知が不足していた。
- 対処：
  - 今回は対象ファイルを手修正し、文字化けを解消した。
- 再発防止：
  - 次ブランチで `scripts/check_bidi_controls.py` を拡張し、許可文字（改行・タブ等）を除く制御文字を検出対象に追加する。
  - 同チェックを `pre-commit` と GitHub Actions の両方で必須化し、コミット前とCIでブロックする。
  - 失敗時は「違反理由」と「該当ファイル:行:列」を明示して迷いを減らす。

## 2026-02-20: 正規化RUNの昇格元は`runs/.../promotion_candidate`に固定する
- 症状：
  - `out/<run_id>/`（非追跡）の内容と、`data/normalized/<doc_id>/`（追跡）の内容が後から一致しないケースが発生した。
- 原因：
  - 昇格元を`out/`に依存すると、Git履歴上で「当時の昇格元」を確定しづらい。
- 対処：
  - 正規化RUNの昇格候補正本を`runs/<run_id>/promotion_candidate/`に置く運用へ変更。
  - 昇格は承認後、`promotion_candidate`から`data/normalized/`へ複写する。
- 再発防止：
  - 正規化RUNでは`out/`を必須にせず、昇格判断の根拠は`runs/.../promotion_candidate`とGit履歴で一元化する。
  - `RUN.md`に昇格コミットIDと祖先判定結果を必ず記録する。
- 確認コマンド：
  - `git log --oneline -- data/normalized/<doc_id>/<doc_id>.regdoc_ir.yaml`
  - `git diff --unified=999999 <prev_promotion_commit> <new_promotion_commit> -- data/normalized/<doc_id>/<doc_id>.regdoc_ir.yaml`

## 2026-02-24: PR本文の文字化け対策は「運用ルール」だけでは不十分
- 症状：
  - `gh pr create --body ...` を端末で直接実行した際、改行エスケープ崩れによりPR本文が文字化けした。
  - PR #120 でも本文編集時に改行崩れが再発し、再編集で復旧が必要になった。
- 原因：
  - 既存ガード（`scripts/check_pr_body_escape_policy.py`）は「リポジトリ内ファイルの静的検査」であり、端末の直接実行コマンド自体は検査対象外。
  - pre-commit はコミット時のみ実行されるため、PR作成時の実行経路を強制できない。
- 対処：
  - 当座は `gh pr edit --body-file <utf8-file>` で本文を差し替えて復旧した。
- 再発防止（将来実施）：
  - `pull_request_target` のGitHub ActionsでPR本文をAPI取得し、文字化けパターン（例: `\\n` 生文字列、`�`）を検査する。
  - PR本文に `<!-- PR_BODY_FILE: <path> -->` を必須化し、本文ファイルとの一致検証を行う。
  - Branch protection で当該チェックを必須化し、fail時はマージ不可にする。
