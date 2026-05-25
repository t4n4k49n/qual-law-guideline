# NIID annex readiness inventory

| annex | decision | promotion mode | table | rows | cells | reason |
| --- | --- | --- | --- | ---: | --- | --- |
| 別表1 | promotion_candidate_as_annex_text | annex_text | no |  |  | narrative reference text; table reconstruction is not applicable |
| 付表1-1 | promotion_candidate_as_annex_text | annex_text | no |  |  | risk group description text; table reconstruction is not applicable |
| 付表1-2 | promotion_candidate_as_numbered_annex_text | annex_text_with_existing_subitems | no |  |  | numbered assessment items are preserved as annex text/subitems; no table reconstruction needed |
| 付表1-3 | promotion_candidate_as_numbered_annex_text | annex_text_with_existing_subitems | no |  |  | animal experiment risk assessment items are preserved as annex text/subitems; no table reconstruction needed |
| 付表2 | promotion_candidate_as_raw_table | table_raw_rows_with_column_schema | yes | 28 | 0/28 | multi-line wrapped cells cannot be safely split in v1, but the full table is preserved with source spans |
| 付表3 | promotion_candidate_as_partial_cell_table | table_rows_with_partial_cells | yes | 21 | 15/21 | safe fixed-width rows are cell-split; remaining note/header rows are preserved raw |
| 付表4 | promotion_candidate_as_partial_cell_table | table_rows_with_partial_cells | yes | 24 | 5/24 | ABSL start rows are cell-split; wrapped continuation rows are preserved raw |
| 別表2 | promotion_candidate_as_sectioned_annex_text | annex_text | no |  |  | BSL criteria are section-style text, not a column reconstruction target |
| 別表3 | promotion_candidate_as_sectioned_annex_text | annex_text | no |  |  | ABSL criteria are section-style text, not a column reconstruction target |
| 別表4 | promotion_candidate_as_raw_annex_text | annex_text_raw_hold | no |  |  | complex wide matrix is fully preserved as annex text; cell reconstruction is not required for readiness |
| 別表5 | promotion_candidate_as_raw_annex_text | annex_text_raw_hold | no |  |  | complex wide matrix is fully preserved as annex text; cell reconstruction is not required for readiness |
| 別表6 | promotion_candidate_as_numbered_annex_text | annex_text | no |  |  | numbered operational requirements are preserved as annex text; not a table target |
| 別表7 | promotion_candidate_as_partial_cell_table | table_rows_with_partial_cells | yes | 30 | 11/30 | safe fixed-width rows are cell-split; wrapped record rows remain raw |
| 別表8 | promotion_candidate_as_raw_annex_text | annex_text_raw_hold | no |  |  | embedded item table is fully preserved as annex text; cell reconstruction is not required for readiness |
| 別表9 | promotion_candidate_as_numbered_annex_text | annex_text | no |  |  | disaster response requirements are preserved as numbered annex text; not a table target |
| 別表10 | promotion_candidate_as_partial_cell_table | table_rows_with_partial_cells | yes | 33 | 10/33 | safe comparison rows are cell-split; wrapped rows remain raw |
