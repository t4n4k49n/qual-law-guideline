# EU GMP Vol.4 Chapter 9 `undated` 解消準備

- run_id: `20260601-183200000_eu-gmp-chap9-undated-prep`
- branch: `feat/eu-gmp-chap9-undated-prep`
- target: `data/normalized/eu_gmp_vol4_chap9_undated/`
- status: investigation complete, no dated doc_id promoted yet

## 背景

法令・ガイドライン正規化の残課題を以下3件へ絞った。

1. EU GMP Vol.4 Chapter 9 の `undated` doc_id解消
2. 21 CFR Part 11 XML正規化
3. 21 CFR Part 211 XML正規化

本RUNでは1件目について、現在の `eu_gmp_vol4_chap9_undated` を dated doc_id に変更できる根拠があるかを確認した。

## 確認対象

- local PDF: `data/human-readable/eu_gmp/vol4/source_pdfs/cap9_en.pdf`
- local text: `data/human-readable/eu_gmp/vol4/source_texts/cap9_en.txt`
- normalized current: `data/normalized/eu_gmp_vol4_chap9_undated/`
- current official URL: `https://health.ec.europa.eu/document/download/07195808-d02e-4d7a-b8f4-f84a83278b62_en?filename=cap9_en.pdf`
- legacy official URL found by web search: `https://health.ec.europa.eu/system/files/2016-11/cap9_en_0.pdf`

## Evidence

### Local Source Text

`cap9_en.txt` contains only:

- `CHAPTER 9 SELF INSPECTION`
- `Principle`
- clauses `9.1` to `9.3`
- page number `59`

It does not contain:

- Brussels date
- Ref. Ares number
- status/revision note
- deadline/effective date
- publication date

### Official PDF Text

The official PDF content is a one-page Chapter 9 text and likewise does not expose a document date in visible text.

Web-opened official PDF text from the legacy URL confirms the same visible content:

- `CHAPTER 9 SELF INSPECTION`
- clauses `9.1` to `9.3`
- page `59`

### HTTP Header Check

Header snapshot is recorded in `http_headers.json`.

- Current document/download URL:
  - `Content-Disposition`: `inline; filename="cap9_en.pdf"`
  - no `Last-Modified` header in the HEAD response
- Legacy `/system/files/2016-11/` URL:
  - path contains `2016-11`
  - `Last-Modified`: `Wed, 01 Dec 2021 14:00:32 GMT`

These values identify hosting/migration metadata, not a stable legal or guideline version date.

### Checksums

- `cap9_en.pdf`: `5AB3990863E77ECA92B72D503E999C50E746907D0FC2B262D5EB7AABCD8FC052`
- `cap9_en.txt`: `0AFEEB40A99CBFB8456B86C3CEE821C3C6843463364D678164785A665ED4E979`
- current `regdoc_ir.yaml`: `DDEABD753BE3316427B08114E30C2D9B72AF353A8F920920DEBDF8DB390D5205`

## Decision

Do not create a dated replacement doc_id from the available evidence.

Reason:

- The visible source document has no date.
- The current official URL has no usable `Last-Modified` header.
- The legacy URL path `2016-11` and legacy `Last-Modified` value are hosting metadata and should not be treated as the guideline version date.

## Recommended Next Step

Keep `eu_gmp_vol4_chap9_undated` as the normalized identifier unless a primary source with a clear Chapter 9 date is found.

Possible future actions:

- Search an official EudraLex index page or archived Commission page for an explicit Chapter 9 version/publication date.
- If a reliable date is found, run a small normalized RUN that renames/re-emits only Chapter 9 from:
  - `eu_gmp_vol4_chap9_undated`
  - to `eu_gmp_vol4_chap9_<yyyymmdd>`
- If no reliable date is found, mark the `undated` identifier as accepted and remove it from active normalization debt.
