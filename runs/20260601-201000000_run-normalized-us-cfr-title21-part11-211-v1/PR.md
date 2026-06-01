## まとめ

21 CFR Part 11 / Part 211 の正式昇格前レビュー用に、2文書分の正規化RUN親PRを作成します。eCFR XMLから `promotion_candidate/` に正本候補を生成し、CFR特有の項番階層、改正リンク注記、Authority/Source/Citation注記がIR上で保持・分離されていることを確認しました。

## 対象文書

| 文書 | doc_id | source URL |
|---|---|---|
| 21 CFR Part 11 | `us_cfr_title21_part11_20251027` | `https://www.ecfr.gov/current/title-21/part-11` |
| 21 CFR Part 211 | `us_cfr_title21_part211_20251027` | `https://www.ecfr.gov/current/title-21/part-211` |

入力XMLは `data/human-readable/cfr/source_xml/` 配下の `2025-10-27` 版です。eCFR XMLの一次資料は GPO/OFR ECFR XML User Guide を参照しています。

## 確認結果

- `uv run python -m pytest tests/test_ecfr_parser.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_cfr_notes.py tests/test_xml2ir_no_fold_article.py tests/test_egov_article_structure.py -q`
  - `12 passed`
- 各候補で `tools/check_ir_structure.py`
  - `[OK] no structure problems found`
- 各候補で `verify_document`
  - `OK`
- `regdoc_profile` candidate visibility
  - `allow_rules: []` / `deny_rules: []`
- heading/textの空白監査
  - leading/trailing whitespace、tab、embedded newline、repeated spaces: `0`

## レビュー観点

- `DIV5` / `DIV6` / `DIV8` が `part` / `subpart` / `section` として保持されている
- `AUTH` / `SOURCE` / `CITA` / `XREF` が informative `note` として分離されている
- Part 11 の `(a)(1)(i)` が `paragraph -> item -> subitem` として保持されている
- Part 211 の `§ 211.42(c)(10)(i)` through `(vi)` が item配下のsubitemとして保持されている
- Part 211 の `§ 211.67(b)(6)` 後の `(c)` が、前item配下に吸収されずsection直下のparagraphへ戻っている
- この2つのXMLにはtable系タグがないため、結合セル複写・table note対応は不要

## 深い階層サンプル

`SAMPLE_PART11.md` と `SAMPLE_PART211.md` に祖先経路を省略せず記録しています。

| 文書 | target_nid | 階層 |
|---|---|---|
| Part 11 | `part11.subptc.sec11_200.pa.i1.sii` | document -> part -> subpart -> section -> paragraph -> item -> subitem |
| Part 211 | `part211.subptc.sec211_42.pc.i10.sivi` | document -> part -> subpart -> section -> paragraph -> item -> subitem |

## 昇格方針

この親PRでは `data/normalized/` は変更しません。承認後、子PRで `promotion_candidate/` から `data/normalized/<doc_id>/` へ2文書分を複写します。

<!-- PR_BODY_FILE: runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/PR.md -->
