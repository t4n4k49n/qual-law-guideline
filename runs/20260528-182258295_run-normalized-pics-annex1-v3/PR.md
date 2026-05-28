## まとめ

PIC/S Annex 1の正式昇格候補を、表セルの目検復元、Table 4のGrade帰属修正、Table 1/5の二段ヘッダ復元を反映した状態で作り直しました。特にTable 1/5は、IRの`table_header.text`と`data.columns`だけで各列の意味が単独で読めるよう、上段の結合ヘッダを含む完全列名にしています。

## 対象

- 文書: PIC/S GMP Guide PE 009-17 Annex 1 Manufacture of sterile medicinal products
- source_url: `https://picscheme.org/docview/8881`
- doc_id: `pics_pe00917_annex1_20230825`
- run_id: `20260528-182258295_run-normalized-pics-annex1-v3`

## 変更内容

- `runs/20260528-182258295_run-normalized-pics-annex1-v3/promotion_candidate/` に正式昇格候補を作成
- 4ファイル、manifest、goal check結果を同梱
- 深い階層サンプルを `SAMPLE_EXTRACT.md` に追加
- RUN開始時に `runs/<run_id>/` と `out/<run_id>/` を同名作成済み
- `data/normalized/` は未変更

## 検証結果

- `qualitycheck.warnings_count`: `0`
- `goal_check`: `PASS`
- `goal_check warnings`: `none`
- IR内のwarning/warn系メタデータ: `0`
- schema: `qai.regdoc_ir.v4`
- node_count: `615`
- source span coverage: `1.0`
- special_structure_audit: `pass`
- source_tables: `6`
- generated_tables: `6`
- generated_rows: `35`
- unresolved_count: `0`
- `python -m pytest tests\test_pics_annex1_tables.py -q`: `9 passed`

## 表確認結果

- Table 1/5: 二段ヘッダを親ヘッダ込みの完全列名として反映
- Table 2/6: Grade Aの横結合No growthセルを各測定法列へ展開し、展開元を保持
- Table 3/4: Grade列の縦結合セルを各操作レコードへ展開
- Table 4: `Background support for grade A...` は Grade B、`Cleaning of equipment.` と `Handling of components...` は Grade Dとして反映

## 深い階層サンプル

`runs/20260528-182258295_run-normalized-pics-annex1-v3/SAMPLE_EXTRACT.md` より:

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann1` | `annex` | `ANNEX` | `MANUFACTURE OF STERILE MEDICINAL PRODUCTS` |
| 3 | `ann1.sec4` | `section` | `4` | `Premises` |
| 4 | `ann1.sec4.p4_27` | `paragraph` | `4.27` | `For cleanroom classification, the total of particles equal to or greater than 0.5 and 5 µm should be measured. This measurement should be performed both at rest and in simulated operations in accordance with the limits specified in Table 1.` |
| 5 | `ann1.sec4.p4_27.tbl1` | `table` | `table` | `Table 1: Maximum permitted total particle concentration for classification` |
| 6 | `ann1.sec4.p4_27.tbl1.tblh` | `table_header` | `table_header` | `Grade | Maximum limits for total particle >= 0.5 µm/m3 at rest | Maximum limits for total particle >= 0.5 µm/m3 in operation | Maximum limits for total particle >= 5 µm/m3 at rest | Maximum limits for total particle >= 5 µm/m3 in operation` |

## 昇格方針

この親PRでは `data/normalized/` を変更しません。承認後、子PRで `promotion_candidate` から `data/normalized/pics_pe00917_annex1_20230825/` へ複写します。

<!-- PR_BODY_FILE: runs/20260528-182258295_run-normalized-pics-annex1-v3/PR.md -->
