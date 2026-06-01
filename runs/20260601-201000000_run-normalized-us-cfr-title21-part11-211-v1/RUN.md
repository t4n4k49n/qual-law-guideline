# 21 CFR Part 11 / Part 211 正規化RUN v1

- run_id: `20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1`
- branch: `run/normalized-us-cfr-title21-part11-211-v1`
- scope: 21 CFR Part 11 / 21 CFR Part 211
- promotion candidate: `runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/promotion_candidate/`
- source preparation runs:
  - `runs/20260601-183000000_cfr-part11-xml-normalization-prep/`
  - `runs/20260601-193000000_cfr-part211-xml-normalization-prep/`

## 前提確認

- `main` は #256 merge後の `origin/main` へ同期済み
- local git hooks: `.githooks`
- eCFR XML parser `us_cfr_ecfr_xml_v1` は #255 / #256 でmainへ反映済み
- 入力はXML
- `data/normalized/` はこの親PRでは変更しない
- eCFR XMLの一次資料:
  - https://www.govinfo.gov/bulkdata/ECFR/resources/ECFR-XML-User-Guide.pdf
  - https://github.com/usgpo/bulk-data/blob/main/ECFR-XML-User-Guide.md

## 対象文書

| document | doc_id | source XML | source URL |
|---|---|---|---|
| 21 CFR Part 11 | `us_cfr_title21_part11_20251027` | `data/human-readable/cfr/source_xml/title21_part11_2025-10-27.xml` | `https://www.ecfr.gov/current/title-21/part-11` |
| 21 CFR Part 211 | `us_cfr_title21_part211_20251027` | `data/human-readable/cfr/source_xml/title21_part211_2025-10-27.xml` | `https://www.ecfr.gov/current/title-21/part-211` |

The local XML filenames provide the `as_of` date `2025-10-27`. The source URLs are current eCFR URLs; if point-in-time source URLs are required later, update metadata in a dedicated follow-up.

## 実行環境

- Python: `3.11.6`
- lxml: `6.1.1`
- PyYAML: `6.0.3`
- typer: `0.26.4`
- tool: `qai_xml2ir` `0.1.1`
- base commit: `7d7e06b`

## 候補作成

```powershell
uv run python -m qai_xml2ir.cli bundle --xml-family ecfr --input data/human-readable/cfr/source_xml/title21_part11_2025-10-27.xml --out-dir runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/promotion_candidate/us_cfr_title21_part11_20251027 --doc-id us_cfr_title21_part11_20251027 --short-title "21 CFR Part 11" --retrieved-at 2025-10-27 --source-url "https://www.ecfr.gov/current/title-21/part-11"
uv run python -m qai_xml2ir.cli bundle --xml-family ecfr --input data/human-readable/cfr/source_xml/title21_part211_2025-10-27.xml --out-dir runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/promotion_candidate/us_cfr_title21_part211_20251027 --doc-id us_cfr_title21_part211_20251027 --short-title "21 CFR Part 211" --retrieved-at 2025-10-27 --source-url "https://www.ecfr.gov/current/title-21/part-211"
```

## 出力概要

| doc_id | schema | parser_profile.id | part | subpart | section | paragraph | item | subitem | note |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `us_cfr_title21_part11_20251027` | `qai.regdoc_ir.v4` | `us_cfr_ecfr_xml_v1` | 1 | 3 | 10 | 43 | 21 | 2 | 4 |
| `us_cfr_title21_part211_20251027` | `qai.regdoc_ir.v4` | `us_cfr_ecfr_xml_v1` | 1 | 11 | 60 | 149 | 104 | 11 | 36 |

## 検証

- `uv run python -m pytest tests/test_ecfr_parser.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_cfr_notes.py tests/test_xml2ir_no_fold_article.py tests/test_egov_article_structure.py -q`
  - `12 passed`
- `uv run python tools/check_ir_structure.py runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/promotion_candidate/us_cfr_title21_part11_20251027`
  - `[OK] no structure problems found`
- `uv run python tools/check_ir_structure.py runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/promotion_candidate/us_cfr_title21_part211_20251027`
  - `[OK] no structure problems found`
- `verify_document`
  - Part 11: `OK`
  - Part 211: `OK`
- `regdoc_profile` candidate visibility
  - Part 11: `allow_rules: []` / `deny_rules: []`
  - Part 211: `allow_rules: []` / `deny_rules: []`
- heading/text whitespace audit
  - leading/trailing whitespace: `0`
  - tabs: `0`
  - embedded newlines: `0`
  - repeated spaces: `0`

## 目検・再合成確認

- eCFR `DIV5` / `DIV6` / `DIV8` が `part` / `subpart` / `section` として保持される。
- `AUTH` / `SOURCE` / `CITA` / `XREF` は informative `note` として本文から分離される。
- Part 11: `(a)(1)(i)` の深い階層が `paragraph -> item -> subitem` として保持される。
- Part 211: `§ 211.42(c)(10)(i)` through `(vi)` のローマ数字が item配下のsubitemとして保持される。
- Part 211: `§ 211.67(b)(6)` 後の `(c)` は、前item配下に吸収されず section直下のparagraphに戻る。
- この2つのXMLにはtable系タグは検出されなかったため、結合セル複写・table note対応は不要。

## 深い階層サンプル

- `SAMPLE_PART11.md`: `part11.subptc.sec11_200.pa.i1.sii`
- `SAMPLE_PART211.md`: `part211.subptc.sec211_42.pc.i10.sivi`
- `SAMPLE_EXTRACT.md`: 上記2件の要約

## 昇格方針

この親PRでは `data/normalized/` は変更しない。
承認後、`runs/20260601-201000000_run-normalized-us-cfr-title21-part11-211-v1/promotion_candidate/` の各doc_id配下から `data/normalized/<doc_id>/` へ複写する子PRを別途作成する。

## 昇格実施記録

- 親PR: `#257`
- 親PR main反映確認: `1906087`
- 昇格ブランチ: `promote/us-cfr-title21-part11-211`
- 昇格先:
  - `data/normalized/us_cfr_title21_part11_20251027/`
  - `data/normalized/us_cfr_title21_part211_20251027/`
- 昇格内容: 各doc_idで `promotion_candidate` の4ファイルを複写
  - `regdoc_ir.yaml`
  - `parser_profile.yaml`
  - `regdoc_profile.yaml`
  - `meta.yaml`
- SHA256確認: 各doc_idの4ファイルは昇格元と昇格先で一致
  - `us_cfr_title21_part11_20251027.meta.yaml`: `6447CB6546A2B7EEF59B69177E8E823F1B7AA00BB0D8485E3F05C69F6F1F3535`
  - `us_cfr_title21_part11_20251027.parser_profile.yaml`: `CCB0B252D77DA2199F87202929E14AB85CB1FF13D4B3B41601314F84CE0FB8ED`
  - `us_cfr_title21_part11_20251027.regdoc_ir.yaml`: `7483D3F99C38168A1BA74CA7CB29F1BC7487996200336E1D2DD826875CF325ED`
  - `us_cfr_title21_part11_20251027.regdoc_profile.yaml`: `D91DB1C418C76C6F3C63246390304D9E73DA573415F1E55E3ADE5A05F5AC72A5`
  - `us_cfr_title21_part211_20251027.meta.yaml`: `9135109C9AF25324EAFAE54A7E00EEAAB61A564A2C5E40EF5BF1307DC28D654E`
  - `us_cfr_title21_part211_20251027.parser_profile.yaml`: `CCB0B252D77DA2199F87202929E14AB85CB1FF13D4B3B41601314F84CE0FB8ED`
  - `us_cfr_title21_part211_20251027.regdoc_ir.yaml`: `B1988167307DA48F88C2A2CE0A18135B49FBEDB5C28505C2D77C783DE56B1514`
  - `us_cfr_title21_part211_20251027.regdoc_profile.yaml`: `ACD43419C42CE9A1D55893B564D6EA58483EEBBDDD312BD071C70B3896E37C81`
