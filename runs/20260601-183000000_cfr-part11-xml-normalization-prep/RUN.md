# 21 CFR Part 11 XML normalization preparation

- run_id: `20260601-183000000_cfr-part11-xml-normalization-prep`
- branch: `feat/cfr-part11-xml-normalization-prep`
- input: `data/human-readable/cfr/source_xml/title21_part11_2025-10-27.xml`
- trial candidate: `runs/20260601-183000000_cfr-part11-xml-normalization-prep/trial_candidate/`

## Source schema reference

- GPO/OFR ECFR XML User Guide PDF: https://www.govinfo.gov/bulkdata/ECFR/resources/ECFR-XML-User-Guide.pdf
- GPO bulk-data mirror: https://github.com/usgpo/bulk-data/blob/main/ECFR-XML-User-Guide.md

The guide describes eCFR XML as derived from OFR/GPO SGML and identifies the relevant hierarchy used by this source: `DIV5` for Part, `DIV6` for Subpart, and `DIV8` for Section. It also notes that eCFR XML is not the official legal edition; this remains source metadata rather than legal-status metadata.

## Work split

### xml2ir common changes

- Added `src/qai_xml2ir/xml_common.py` for XML local-name handling, inline text flattening, and whitespace normalization.
- Extended `xml2ir bundle` with `--xml-family egov|ecfr`; default remains `egov`.
- Extended meta generation with optional jurisdiction/language/source label/CFR identifiers while preserving existing e-Gov defaults.

### xml2ir CFR-specific changes

- Added `src/qai_xml2ir/ecfr_parser.py`.
- Mapped eCFR hierarchy:
  - `DIV5 TYPE="PART"` -> `part`
  - `DIV6 TYPE="SUBPART"` -> `subpart`
  - `DIV8 TYPE="SECTION"` -> `section`
- Split `P` leading CFR markers into nested IR nodes:
  - `(a)` -> `paragraph`
  - `(1)` -> `item`
  - `(i)` / `(ii)` after an item -> `subitem`
  - top-level `(i)` remains `paragraph`, which avoids misclassifying 21 CFR 11.1(i).
- Preserved unnumbered section chapeau text on the `section` node.
- Mapped `AUTH`, `SOURCE`, and `CITA` to informative `note` nodes.
- Added eCFR parser profile output `us_cfr_ecfr_xml_v1`.

### Other preparation artifacts

- Generated trial candidate bundle for `us_cfr_title21_part11_20251027`.
- Added parser tests for Part 11 XML structure, note separation, CFR marker nesting, and filename metadata.

## Trial candidate summary

- doc_id: `us_cfr_title21_part11_20251027`
- source date in filename/as_of: `2025-10-27`
- source URL used in metadata: `https://www.ecfr.gov/current/title-21/part-11`
- generated files:
  - `us_cfr_title21_part11_20251027.regdoc_ir.yaml`
  - `us_cfr_title21_part11_20251027.parser_profile.yaml`
  - `us_cfr_title21_part11_20251027.regdoc_profile.yaml`
  - `us_cfr_title21_part11_20251027.meta.yaml`

Observed structure in generated IR:

- `subpart`: 3
- `section`: 10
- `paragraph`: 43
- `item`: 21
- `subitem`: 2
- `note`: 4

## Checks

- `python -m pytest tests/test_ecfr_parser.py tests/test_text2ir_cfr_quality_v2.py tests/test_text2ir_cfr_notes.py -q`
  - result: `5 passed`
- `uv run python -m pytest tests/test_ecfr_parser.py tests/test_xml2ir_no_fold_article.py tests/test_egov_article_structure.py -q`
  - result: `6 passed`
- `uv run python -m qai_xml2ir.cli bundle --xml-family ecfr --input data/human-readable/cfr/source_xml/title21_part11_2025-10-27.xml --out-dir runs/20260601-183000000_cfr-part11-xml-normalization-prep/trial_candidate --doc-id us_cfr_title21_part11_20251027 --short-title "21 CFR Part 11" --retrieved-at 2025-10-27 --source-url "https://www.ecfr.gov/current/title-21/part-11"`
  - result: generated trial candidate bundle

## Remaining before formal normalized RUN

- Decide whether the source URL should be current eCFR (`/current/title-21/part-11`) or a point-in-time URL if the local XML retrieval process records one.
- Reuse the same parser for 21 CFR Part 211 after Part 11 review; Part 211 may expose deeper or table-like eCFR structures not present in Part 11.
