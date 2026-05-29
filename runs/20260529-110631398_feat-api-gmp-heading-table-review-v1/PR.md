# 原薬GMPガイドラインのHeading/表レビュー修正

## まとめ

原薬GMPガイドラインを正式な正規化RUNへ進める前に、条文直上の見出しと表1の保持状態を確認し、チェックシート表示で必要な文脈が落ちないように階層構造を修正しました。これにより、見出しがある条文は見出し配下の本文としてたどれ、見出しがない章は章直下の本文として扱える状態になります。

## 変更内容

- API GMP専用profileで `x.y` を `section`、`x.y0` / `x.yy` を `paragraph` として扱うよう修正。
- 表1 adapterが `section` 配下にも表を接続できるよう修正。
- Heading階層と表1接続の回帰テストを追加。
- Codex目検レビューRUNを追加。

## 確認

- `2.1 原則` 配下に `2.10` 以降が入ることを確認。
- `3.1 従業員の適格性` 配下に `3.10` 以降が入ることを確認。
- `12.3 適格性評価` 配下に `12.30` が入ることを確認。
- `1.3 適用範囲` 配下に表1が残ることを確認。
- 見出しがない章13/15/16はparagraphを章直下に保持。

## 検証

- `.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_api_gmp_guideline.py -q`: `4 passed`
- `.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_api_gmp_guideline.py tests/test_text2ir_jp_guideline.py tests/test_text2ir_goal_check.py tests/test_table_note_real_samples.py -q`: `20 passed`
- `.\.venv\Scripts\python.exe -m pytest -q`: `253 passed, 1 skipped`
- GOAL check: pass
- Special structure audit: pass

## 次工程

旧 `20260525-121645707_run-normalized-api-gmp-guideline-v1` のpromotion candidateは使わず、この修正を取り込んだ後に新しい正規化RUNでfreshな `promotion_candidate/` を作成する。

<!-- PR_BODY_FILE: runs/20260529-110631398_feat-api-gmp-heading-table-review-v1/PR.md -->
