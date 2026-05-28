## まとめ

PIC/S Annex 1の正式昇格候補を、表セルの目検復元修正を反映した状態で作り直しました。全6表について、結合セル・折返しセルの扱いがIRメタデータとテストで固定され、旧候補で問題だったTable 4のGrade帰属も修正済みです。

## 対象

- 文書: PIC/S GMP Guide PE 009-17 Annex 1 Manufacture of sterile medicinal products
- source_url: `https://picscheme.org/docview/8881`
- doc_id: `pics_pe00917_annex1_20230825`
- run_id: `20260528-172651562_run-normalized-pics-annex1-v2`

## 変更内容

- `runs/20260528-172651562_run-normalized-pics-annex1-v2/promotion_candidate/` に正式昇格候補を作成
- 4ファイル、manifest、goal check結果を同梱
- 深い階層サンプルを `SAMPLE_EXTRACT.md` に追加
- `data/normalized/` は未変更

## 検証結果

- `qualitycheck.warnings_count`: `0`
- `goal_check`: `PASS`
- `goal_check warnings`: `none`
- schema: `qai.regdoc_ir.v4`
- node_count: `615`
- source span coverage: `1.0`
- special_structure_audit: `pass`
- source_tables: `6`
- generated_tables: `6`
- generated_rows: `35`
- unresolved_count: `0`
- `python -m pytest tests\test_pics_annex1_tables.py -q`: `9 passed`

## 表セルの確認結果

- Table 1/5: 二段ヘッダとGrade Dの折返しセルをレビュー済みメタデータとして保持
- Table 2/6: Grade Aの横結合No growthセルを各測定法列へ展開し、展開元を保持
- Table 3/4: Grade列の縦結合セルを各操作レコードへ展開
- Table 4: `Background support for grade A...` は Grade B、`Cleaning of equipment.` と `Handling of components...` は Grade Dとして反映

## 深い階層サンプル

`runs/20260528-172651562_run-normalized-pics-annex1-v2/SAMPLE_EXTRACT.md` より:

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann1` | `annex` | `ANNEX` | `MANUFACTURE OF STERILE MEDICINAL PRODUCTS` |
| 3 | `ann1.sec8` | `section` | `8` | `Production and Specific Technologies` |
| 4 | `ann1.sec8.tbl4` | `table` | `table` | `Table 4: Examples of operations and grades for aseptic preparation and processing operations` |
| 5 | `ann1.sec8.tbl4.tblh` | `table_header` | `table_header` | `Grade | Operation` |
| 6 | `ann1.sec8.tbl4.tblh.tblr12` | `table_row` | `table_row` | `Grade D | Cleaning of equipment.` |

## 昇格方針

この親PRでは `data/normalized/` を変更しません。承認後、子PRで `promotion_candidate` から `data/normalized/pics_pe00917_annex1_20230825/` へ複写します。

<!-- PR_BODY_FILE: runs/20260528-172651562_run-normalized-pics-annex1-v2/PR.md -->
