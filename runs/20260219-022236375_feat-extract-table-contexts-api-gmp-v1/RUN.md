# RUN: 20260219-022236375_feat-extract-table-contexts-api-gmp-v1

- run_id: `20260219-022236375_feat-extract-table-contexts-api-gmp-v1`
- branch: `feat/extract-table-contexts-api-gmp-v1`

## 目的
- 指定ディレクトリ配下の txt/md から表ブロックを抽出し、親・先祖文脈（見出し行）と表下注記をセットで出力する。

## 実装
- `scripts/extract_table_contexts.py` を追加。
  - 対象: `*.txt`, `*.md`
  - 抽出: Markdown table（header + separator + row）
  - 文脈: 直近の見出し候補を最大3件まで祖先として付与
  - 注記: `Note/注/注記/備考/※/（注）` を表直後から収集

## 実行
- `python scripts/extract_table_contexts.py --input-root "%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\human-readable\06.原薬GMPガイドライン" --output-md "runs/20260219-022236375_feat-extract-table-contexts-api-gmp-v1/table_context_extractions.md" --output-jsonl "runs/20260219-022236375_feat-extract-table-contexts-api-gmp-v1/table_context_extractions.jsonl"`

## 結果
- 抽出ブロック数: `8`
- 出力:
  - `runs/20260219-022236375_feat-extract-table-contexts-api-gmp-v1/table_context_extractions.md`
  - `runs/20260219-022236375_feat-extract-table-contexts-api-gmp-v1/table_context_extractions.jsonl`

## 既知課題（次アクション候補）
- 一部 markdown で caption（表1行）を取りこぼすケースがある（空行・整形差分の影響）。
- 祖先判定が文中の「第xx章には...」を見出しとして誤検出するケースがある。
- 同内容の重複ファイル（`*.md` / `*_formatted*.txt`）により重複抽出が発生する。



