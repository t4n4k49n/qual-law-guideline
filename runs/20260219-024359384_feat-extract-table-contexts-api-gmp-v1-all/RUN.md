# RUN: 20260219-024359384_feat-extract-table-contexts-api-gmp-v1-all

- run_id: `20260219-024359384_feat-extract-table-contexts-api-gmp-v1-all`
- branch: `feat/extract-table-contexts-api-gmp-v1`

## 目的
- `OLD-HANDMADE/data/human-readable` 全体を対象に、表ブロック + 祖先文脈 + 注記の抽出を実行し、課題抽出用の一覧を作る。

## 実行
- `python scripts/extract_table_contexts.py --input-root "%USERPROFILE%\\Documents\\GitHub\\qual-law-guideline_OLD-HANDMADE\\data\\human-readable" --output-md "runs/20260219-024359384_feat-extract-table-contexts-api-gmp-v1-all/table_context_extractions.md" --output-jsonl "runs/20260219-024359384_feat-extract-table-contexts-api-gmp-v1-all/table_context_extractions.jsonl"`

## 結果
- 抽出ブロック（raw）: `52`
- 抽出ブロック（unique）: `34`
- 抽出元の主な文書:
  - `08.病原体等安全管理規程/病原体等安全管理規程.txt` (8)
  - `12.PICS/.../PICS_PE_009-17_ANNEX-1*.txt` (各6)
  - `06.原薬GMPガイドライン/原薬GMPガイドライン.md` (4)

## 生成物
- `runs/20260219-024359384_feat-extract-table-contexts-api-gmp-v1-all/table_context_extractions.md`
- `runs/20260219-024359384_feat-extract-table-contexts-api-gmp-v1-all/table_context_extractions.jsonl`
- `runs/20260219-024359384_feat-extract-table-contexts-api-gmp-v1-all/RUN.md`

## 残課題
- caption なし table が一部残るため、前方/後方探索の追加余地あり
- 見出し抽出は文書ごとの表記差により調整余地あり

