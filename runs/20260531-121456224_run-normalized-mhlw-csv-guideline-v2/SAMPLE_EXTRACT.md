# 深い階層サンプル抽出

- source: `runs/20260531-121456224_run-normalized-mhlw-csv-guideline-v2/promotion_candidate/jp_mhlw_csv_guideline_20101021.regdoc_ir.yaml`
- target_nid: `annex2.tbl1.tblh.tblr5`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `annex2` | `annex` | `別紙` | `カテゴリ分類表と対応例` |
| 3 | `annex2.tbl1` | `table` | `table` | `カテゴリ分類表` |
| 4 | `annex2.tbl1.tblh` | `table_header` | `table_header` | `category_no | category_name | content | content_detail | development_plan | system_assessment | system_registry | urs | fs | ds | supplier_audit | acceptance_test | validation_plan_report | dq | iq | oq | pq | sop | document_control | remarks` |
| 5 | `annex2.tbl1.tblh.tblr5` | `table_row` | `table_row` | `3 |  | 商業ベースで販売されている既製のパッケージソフトウェアで、それ自体は業務プロセスに合わせて構成設定していないもの(実行時のパラメータの入力のみで調整されるアプリケーション等は本カテゴリに含まれる) | 単独のコンピュータシステム | ◎ | ◎ | ◎ | ◎ | ― | ― | △ | ― | ◎ | ― | ◎2 | ― | ◎ | ◎ | ◎ |` |
