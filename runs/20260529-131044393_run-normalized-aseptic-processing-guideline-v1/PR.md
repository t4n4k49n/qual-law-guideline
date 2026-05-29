# 無菌操作法指針 正規化RUN v1

## まとめ

無菌操作法指針を `qai.regdoc_ir.v4` の正規化候補として生成し、PR #220 で承認された heading/table 目検修正を反映しました。表1から表3は、PDF上の結合見出しを `header_structure.spanning_headers` に保持し、データ行を `table_row` として利用できる粒度にしています。

このPRは親PRです。`data/normalized/` は変更せず、承認後に昇格専用の子PRで `promotion_candidate` から正式版へ複写します。

## 対象

- 文書: 無菌操作法による無菌医薬品の製造に関する指針
- doc_id: `jp_pmda_aseptic_processing_guideline_20110420`
- source PDF: `https://www.pmda.go.jp/files/000206144.pdf`
- source text: `data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt`
- promotion candidate: `runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/promotion_candidate/`
- parser profile: `jp_pmda_aseptic_processing_guideline_v1`
- schema: `qai.regdoc_ir.v4`

## 検証結果

- goal check: PASS
  - nodes: 436
  - source span coverage: 1.0
  - table: 3
  - table_header: 3
  - table_row: 12
- special structure audit: PASS
  - generated_tables: 3
  - generated_rows: 12
  - unresolved_special_blocks: 0
- focused tests: `7 passed`
- full tests: `253 passed, 1 skipped`

## 目検確認

- heading:
  - 章・節・深い細目の親子関係を `SAMPLE_EXTRACT.md` で確認。
  - サンプル: `root -> cha7 -> cha7.sec7_1 -> cha7.sec7_1.p7_1_1`
  - `cha7.sec7_1` の heading は「清浄度レベルによる作業所の分類」。
- 表:
  - 表1 `cha7.sec7_1.tbl1`: 「名称」「最大許容微粒子数（個／m3）」「非作業時」「作業時」の結合見出しを保持。
  - 表2 `cha11.sec11_3.tbl2`: 「表面付着微生物」の結合見出しを保持し、C/D の区域条件を2行に分離。
  - 表3 `cha11.sec11_3.tbl3`: 「空中微生物」「表面付着微生物」の結合見出しと単位を保持。

## レビュー用ファイル

- `runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/RUN.md`
- `runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/GOAL_CHECK.md`
- `runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/SPECIAL_STRUCTURE_AUDIT.md`
- `runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/SAMPLE_EXTRACT.md`
- `runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/HEADING_TABLE_REVIEW.md`

## 正式版昇格について

このPRでは `data/normalized/` を変更していません。承認後、子PRで `runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/promotion_candidate/` から `data/normalized/jp_pmda_aseptic_processing_guideline_20110420/` へ複写します。

<!-- PR_BODY_FILE: runs/20260529-131044393_run-normalized-aseptic-processing-guideline-v1/PR.md -->
