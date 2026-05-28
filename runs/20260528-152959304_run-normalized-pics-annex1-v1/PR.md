## まとめ

PIC/S Annex 1を正規化RUNのレビュー対象として正式な候補正本にしました。表・注記を含むAnnex 1を扱える状態にすることで、PIC/S単体Annexの正規化対象をAnnex 11から一段広げ、DQチェックシートで表行まで選択候補にできるデータ整備を進めています。

## 変更内容

| 項目 | 内容 |
|---|---|
| 対象 | `pics_pe00917_annex1_20230825` |
| 入力 | `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt` |
| source_url | `https://picscheme.org/docview/8881` |
| parser_profile | `pics_annex1_default_v2` |
| 出力 | `runs/20260528-152959304_run-normalized-pics-annex1-v1/promotion_candidate/` |

## 事前確認

Annex 1は表・注記を含むため、先に通常RUN `runs/20260528-102010880_review-pics-annex1-table-note/` で確認した。そこで検出したページフッター混入はPR #194で修正済みであり、今回の正規化RUNは修正後のmainから `promotion_candidate/` に再生成している。

## 検証

- promotion goal: PASS
- schema: `qai.regdoc_ir.v4`
- nodes: 615
- verify: pass
- source span coverage: 1.0
- table: 6
- table_row: 35
- note: 16
- warnings: none
- errors: none
- selectable_kinds: `subitem`, `item`, `paragraph`, `statement`, `table_row`

追加確認:

- IR本文中のページフッター混入: 0件
- 関連テスト: `tests/test_pics_annex1_tables.py tests/test_text2ir_profiles_pics.py tests/test_pics_annexes_bundle_specials.py` で18 passed

## 深い階層サンプル

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ann1` | `annex` | `ANNEX` | `MANUFACTURE OF STERILE MEDICINAL PRODUCTS` |
| 3 | `ann1.sec9` | `section` | `9` | `Environmental & process monitoring` |
| 4 | `ann1.sec9.p9_30` | `paragraph` | `9.30` | `Action limits for viable particle contamination are shown in Table 6.` |
| 5 | `ann1.sec9.p9_30.tbl6` | `table` | `table` | `Table 6: Maximum action limits for viable particle contamination` |
| 6 | `ann1.sec9.p9_30.tbl6.tblh` | `table_header` | `table_header` | `Grade | Air sample CFU/m3 | Settle plates (diameter 90 mm) CFU/4 hours (a) | Contact plates (diameter 55 mm) CFU/plate (b) | Glove print, including 5 fingers on both hands CFU/glove` |
| 7 | `ann1.sec9.p9_30.tbl6.tblh.tblr1` | `table_row` | `table_row` | `A | No growth (c) | No growth (c) | No growth (c) | No growth (c)` |

## 昇格方針

この親PRでは `data/normalized/` を変更しない。承認後に、子PRで `promotion_candidate/` から `data/normalized/pics_pe00917_annex1_20230825/` へ4ファイルのみ複写する。

<!-- PR_BODY_FILE: runs/20260528-152959304_run-normalized-pics-annex1-v1/PR.md -->
