# 旧e-Gov正規化 再正規化RUN v3

## まとめ

旧e-Gov正規化データ5件を、公式e-Gov XMLから現行IR基準で再生成する正規化RUNです。parser改修は準備PR `#261` で分離済みであり、このPRは `promotion_candidate/` のレビューに絞っています。旧構造の `article.text` や article 直下 item を解消し、DQチェックシートで一貫して参照できる階層へ更新します。

## 対象e-Gov法令URL

| doc_id | e-Gov法令URL |
|---|---|
| `jp_egov_335AC0000000145_20260501_507AC0000000037` | `https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037` |
| `jp_egov_336CO0000000011_20260501_507CO0000000362` | `https://laws.e-gov.go.jp/law/336CO0000000011/20260501_507CO0000000362` |
| `jp_egov_336M50000100001_20260501_507M60000100117` | `https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117` |
| `jp_egov_336M50000100002_20260501_507M60000100117` | `https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117` |
| `jp_egov_416M60000100179_20260501_507M60000100117` | `https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117` |

## 変更内容

- `promotion_candidate/` に5文書分の正規化候補を作成
- `manifest.yaml` に入力XML、生成コマンド、件数、SHA256、検証結果を記録
- `SAMPLE_EXTRACT.md` に5文書分の深い階層サンプルを記録
- このPRに `src/`、`tests/`、`data/normalized/` の変更は含めない

## 検証結果

- `uv run python tools/check_ir_structure.py runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/promotion_candidate`
  - `[OK] no structure problems found (scanned: 20 yaml files)`
- `uv run python -m pytest -q tests/test_xml_common.py tests/test_egov_api_wrapper.py tests/test_egov_text_cleanup.py tests/test_egov_article_structure.py tests/test_egov_table_spans.py tests/test_egov_table_payload_header_inference.py tests/test_xml2ir_no_fold_article.py tests/test_xml2ir_profiles_table_context.py tests/test_ecfr_parser.py`
  - `19 passed`
- `verify_document`
  - 5文書すべて `OK`
- heading/text whitespace audit
  - 5文書すべて `0`

## 深い階層サンプル

以下はPR本文内の確認用抜粋です。5文書分の全サンプルは `SAMPLE_EXTRACT.md` にも記録しています。

### jp_egov_336M50000100001_20260501_507M60000100117

- source: `runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/promotion_candidate/jp_egov_336M50000100001_20260501_507M60000100117/jp_egov_336M50000100001_20260501_507M60000100117.regdoc_ir.yaml`
- target_nid: `art114_16.p2.tbl1.tblh.tblr1`

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ch3` | `chapter` | `章` | `医療機器及び体外診断用医薬品の製造販売業及び製造業等` |
| 3 | `ch3.sec1` | `section` | `節` | `医療機器及び体外診断用医薬品の製造販売業及び製造業` |
| 4 | `art114_16` | `article` | `条` | `（準用）` |
| 5 | `art114_16.p2` | `paragraph` | `項` | `前項の場合において、次の表の上欄に掲げる規定中同表の中欄に掲げる字句は、それぞれ同表の下欄に掲げる字句に読み替えるものとする。` |
| 6 | `art114_16.p2.tbl1` | `table` | `table` |  |
| 7 | `art114_16.p2.tbl1.tblh` | `table_header` | `table_header` |  |
| 8 | `art114_16.p2.tbl1.tblh.tblr1` | `table_row` | `table_row` | `第百十四条の十 \| 医療機器又は体外診断用医薬品の製造業 \| 医療機器等外国製造業者` |

### jp_egov_416M60000100179_20260501_507M60000100117

- source: `runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/promotion_candidate/jp_egov_416M60000100179_20260501_507M60000100117/jp_egov_416M60000100179_20260501_507M60000100117.regdoc_ir.yaml`
- target_nid: `art26.p1.i1.i.pt1`

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `ch2` | `chapter` | `章` | `医薬品製造業者等の製造所における製造管理及び品質管理` |
| 3 | `ch2.sec4` | `section` | `節` | `生物由来医薬品等の製造管理及び品質管理` |
| 4 | `art26` | `article` | `条` | `（生物由来医薬品等の製造所の構造設備）` |
| 5 | `art26.p1` | `paragraph` | `項` | `生物由来医薬品等に係る製品の製造業者等の製造所の構造設備は、第九条第一項及び第二十三条の規定に定めるもののほか、次に定めるところに適合するものでなければならない。` |
| 6 | `art26.p1.i1` | `item` | `号` | `生物学的製剤（ロットを構成しない血液製剤を除く。）に係る製品の製造所の構造設備は、次に定めるところに適合するものであること。` |
| 7 | `art26.p1.i1.i` | `subitem` | `イ` | `作業所には、他から明確に区別された室において、次に掲げる設備を設けること。ただし、製品の種類、製造方法等により、当該製品の製造に必要がないと認められる設備を除く。` |
| 8 | `art26.p1.i1.i.pt1` | `point` | `（１）` | `微生物の貯蔵設備` |

## 昇格方針

このPRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` から `data/normalized/<doc_id>/` へ5文書を複写します。`ARCHIVE_jp_egov_*` は昇格対象外です。

<!-- PR_BODY_FILE: runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/PR.md -->
