# RUN: 20260522-034415_text2ir-goal-gap-confirmation

## 目的

text2ir系文書について、コード修正なしで現状確認・再生成・xml2ir最終正規化GOALとの差分分類を行う。

## ブランチ

`docs/text2ir-goal-gap-confirmation`

## 厳守事項への対応

- ソースコード、profile、テスト、`data/normalized/` は変更しない。
- 成果物は `runs/20260522-034415_text2ir-goal-gap-confirmation/`、再生成物は `out/20260522-034415_text2ir-goal-gap-confirmation/` のみに作成する。
- 報告書には個人環境の絶対パスを記載しない。

## 参照資料

- `runs/20260522-012123133_docs-text2ir-gap-review-brief/EXTERNAL_REVIEW_BRIEF.md`
- `runs/20260522-012123133_docs-text2ir-gap-review-brief/RUN.md`
- `docs/NORMALIZED_RUN_OUTPUT_4FILES_GUIDE.md`
- `docs/NORMALIZED_RUN_PLAYBOOK.md`
- `docs/NORMALIZED_RELEASE_CHECKLIST.md`
- `docs/REFERENCE.md`
- `out/administrators-memos/20260522text2ir側文書の正規化向上/01_Chappi_Codex確認用プロンプト/text2ir_goal_gap_guidance.md`

## 実行概要

- 代表9文書を現行profileで再生成した。
- CFR Part 11 / Part 211 は現行repo内の入力ファイルが見つからなかったため再生成対象外とした。
- 生成後に `qai_xml2ir.verify.verify_document` を9件へ適用し、全件passを確認した。
