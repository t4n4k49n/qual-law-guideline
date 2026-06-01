# 21 CFR Part 211 XML normalization preparation

- run_id: `20260601-193000000_cfr-part211-xml-normalization-prep`
- branch: `feat/cfr-part211-xml-normalization-prep`
- input: `data/human-readable/cfr/source_xml/title21_part211_2025-10-27.xml`
- trial candidate: `runs/20260601-193000000_cfr-part211-xml-normalization-prep/trial_candidate_r3/`

## Source schema reference

- GPO/OFR ECFR XML User Guide PDF: https://www.govinfo.gov/bulkdata/ECFR/resources/ECFR-XML-User-Guide.pdf
- GPO bulk-data mirror: https://github.com/usgpo/bulk-data/blob/main/ECFR-XML-User-Guide.md

Part 211 uses the same eCFR hierarchy as Part 11: `DIV5` for Part, `DIV6` for Subpart, and `DIV8` for Section. This source also contains direct `XREF` amendment links under sections.

## Work split

### xml2ir common changes

- No additional common xml2ir surface was required beyond the Part 11 preparation already merged.
- Reused `--xml-family ecfr`, shared XML text flattening, whitespace normalization, and US/CFR metadata fields.

### xml2ir CFR-specific changes

- Tightened CFR marker classification for Part 211:
  - Lowercase alphabetic markers that continue the section-level sequence, such as `(c)` after `(b)(1)` through `(b)(6)`, return to `paragraph`.
  - Roman subitems such as `§ 211.42(c)(10)(i)` through `(vi)` remain under the preceding item.
- Added direct `XREF` handling as informative `note` nodes so amendment links are not dropped.
- Updated the eCFR parser profile marker list with `XREF`.

### Other preparation artifacts

- Generated a Part 211 trial candidate bundle for `us_cfr_title21_part211_20251027`.
- Added Part 211 tests covering:
  - alpha paragraph recovery after item lists
  - roman subitems under an item
  - section-level `XREF` note preservation

## Trial candidate summary

- doc_id: `us_cfr_title21_part211_20251027`
- source date in filename/as_of: `2025-10-27`
- source URL used in metadata: `https://www.ecfr.gov/current/title-21/part-211`
- generated files:
  - `us_cfr_title21_part211_20251027.regdoc_ir.yaml`
  - `us_cfr_title21_part211_20251027.parser_profile.yaml`
  - `us_cfr_title21_part211_20251027.regdoc_profile.yaml`
  - `us_cfr_title21_part211_20251027.meta.yaml`

Observed structure in generated IR:

- `subpart`: 11
- `section`: 60
- `paragraph`: 149
- `item`: 104
- `subitem`: 11
- `note`: 36

## Checks

- `uv run python -m pytest tests/test_ecfr_parser.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_cfr_notes.py tests/test_xml2ir_no_fold_article.py tests/test_egov_article_structure.py -q`
  - result: `12 passed`
- `uv run python -m qai_xml2ir.cli bundle --xml-family ecfr --input data/human-readable/cfr/source_xml/title21_part211_2025-10-27.xml --out-dir runs/20260601-193000000_cfr-part211-xml-normalization-prep/trial_candidate_r3 --doc-id us_cfr_title21_part211_20251027 --short-title "21 CFR Part 211" --retrieved-at 2025-10-27 --source-url "https://www.ecfr.gov/current/title-21/part-211"`
  - result: generated trial candidate bundle

## Remaining before formal normalized RUN

- Run Part 11 and Part 211 together through the formal normalized-run playbook after review.
- Decide whether source URLs should remain `/current/title-21/part-...` or use point-in-time eCFR URLs if the retrieval process records one.
