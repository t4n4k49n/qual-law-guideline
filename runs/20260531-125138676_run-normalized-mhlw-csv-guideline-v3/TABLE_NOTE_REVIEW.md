# CSVガイドライン 表・note 目検チェック

- source: `runs/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/promotion_candidate/jp_mhlw_csv_guideline_20101021.regdoc_ir.yaml`

## 別紙1 コンピュータ化システムのライフサイクルモデル

- nid: `annex1`
- source_format: `html_image_reference`
- extractable_text: `False`
- text: `画像1 (36KB)`

- table: none

## 別紙2 カテゴリ分類表と対応例

- nid: `annex2`
- source_format: `html_page1_placeholder_and_page2_tables`
- extractable_text: `True`
- text: ``

### table 1 カテゴリ分類表

- nid: `annex2.tbl1`
- display_rows: `7`
- reconstructed_columns: `category_no, category_name, content, content_detail, development_plan, system_assessment, system_registry, urs, fs, ds`
- semantic_reconstruction: `csv_annex2_semantic_records_v1`
- semantic_record_count: `5`

| row_nid | row_num | semantic_record_id | cells_prefix |
|---|---:|---|---|
| `annex2.tbl1.tblh.tblr1` | `1` | `non_data_row_not_semantic_record` | カテゴリ / カテゴリ / 内容 / 内容 / 開発計画書 / システムアセスメント |
| `annex2.tbl1.tblh.tblr2` | `2` | `csv_annex2.category1` | 1 / 基盤ソフト / ・カテゴリ3以降のアプリケーションが構築される基盤となるもの(プラットフォーム)・運用環境を管理するソフトウェア / ・カテゴリ3以降のアプリケーションが構築される基盤となるもの(プラットフォーム)・運用環境を管理するソフトウェア / ○1 / ○1 |
| `annex2.tbl1.tblh.tblr3` | `3` | `csv_annex2.category2` | 2 /  / このカテゴリは設定しない / このカテゴリは設定しない / ― / ― |
| `annex2.tbl1.tblh.tblr4` | `4` | `csv_annex2.category3` | 3 / 構成設定していないソフトウェア / 商業ベースで販売されている既製のパッケージソフトウェアで、それ自体は業務プロセスに合わせて構成設定していないもの(実行時のパラメータの入力のみで調整されるアプリケーション等は本カテゴリに含まれる) / 製造設備、分析機器、製造支援設備等に搭載されるシステム / ◎ / ◎ |
| `annex2.tbl1.tblh.tblr5` | `5` | `csv_annex2.category3` | 3 /  / 商業ベースで販売されている既製のパッケージソフトウェアで、それ自体は業務プロセスに合わせて構成設定していないもの(実行時のパラメータの入力のみで調整されるアプリケーション等は本カテゴリに含まれる) / 単独のコンピュータシステム / ◎ / ◎ |
| `annex2.tbl1.tblh.tblr6` | `6` | `csv_annex2.category4` | 4 / 構成設定したソフトウェア / ユーザの業務プロセスに合わせて構成設定したソフトウェア(アプリケーション上で動作するマクロ等を含む)。但し、プログラムを変更した場合はカテゴリ5とする / ユーザの業務プロセスに合わせて構成設定したソフトウェア(アプリケーション上で動作するマクロ等を含む)。但し、プログラムを変更した場合はカテゴリ5とする / ◎ / ◎ |
| `annex2.tbl1.tblh.tblr7` | `7` | `csv_annex2.category5` | 5 / カスタムソフトウェア / 業務プロセスに合わせて設計され、プログラムされたソフトウェア(アプリケーション上で動作するマクロ等を含む) / 業務プロセスに合わせて設計され、プログラムされたソフトウェア(アプリケーション上で動作するマクロ等を含む) / ◎ / ◎ |

### table 2 本ガイドラインの対象外

- nid: `annex2.tbl2`
- display_rows: `1`
- reconstructed_columns: `excluded_item, description`
- semantic_reconstruction: `csv_annex2_semantic_records_v1`
- semantic_record_count: `1`

| row_nid | row_num | semantic_record_id | cells_prefix |
|---|---:|---|---|
| `annex2.tbl2.tblh.tblr1` | `1` | `csv_annex2.excluded.r1` | 本ガイドラインの対象外 / ・電卓、電子時計、表示のみの電磁はかり等、商業ベースで販売されている汎用の機器・製造記録の作成や出荷判定等のGQP省令及びGMP省令に係る業務に使用されない市販のワープロソフト、表計算ソフト等で、社会一般で広く利用されているパッケージソフトウェア及びPC。なお、それらソフトにより製造記録の作成や出荷判定等のGQP省令及びGMP省令に係る業務に使用する場合は、本ガイドラインの対象とせず、バージョン番号、PCの機 |

## 結合セル・semantic record確認

- category3.raw_row_nums: `[4, 5]`
- row4 semantic_record_id: `csv_annex2.category3`
- row5 semantic_record_id: `csv_annex2.category3`
