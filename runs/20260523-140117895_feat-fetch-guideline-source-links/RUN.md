# RUN: 20260523-140117895_feat-fetch-guideline-source-links

## Scope

- Source list: `F:\dbe\202407Nexredge\20251223開発分科会（法令）\会議後７（20260202NXR返事＠Slack）\GMP法令等の確認20251223_20260128（除外項目確認用） .xlsx.md`
- Branch: `feat/fetch-guideline-source-links`
- Purpose: Fetch source documents linked from the table and place them under `data/human-readable/`.

## Result

- Fetched 25 linked source files.
- PDF links were saved as `.pdf`.
- HTML/source page links were saved as `.html`.
- PIC/S `docview` links returned PDF bytes, so the files were saved with `.pdf` extensions.
- e-Gov law page links returned the SPA entry HTML; XML-derived IR for these laws already exists under `data/normalized/`.

## Output

- Tracked source list: `runs/20260523-140117895_feat-fetch-guideline-source-links/FETCHED_SOURCES.json`
- Local fetch log: `out/20260523-140117895_feat-fetch-guideline-source-links/fetch_results.json`

## Placement

- `data/human-readable/egov/source_pages/`
- `data/human-readable/pmda/api_gmp_guideline/`
- `data/human-readable/pmda/aseptic_processing_guideline/`
- `data/human-readable/niid/pathogen_safety_management/`
- `data/human-readable/mhlw/csv_guideline/`
- `data/human-readable/eu_gmp/vol4/source_pdfs/`
- `data/human-readable/cfr/source_pdfs/`
- `data/human-readable/pics/source_docs/`
- `data/human-readable/who/source_pdfs/`

## Next

- Convert newly fetched PDFs/HTML to text in a separate 1-run task before running `text2ir`.
- For e-Gov laws, continue to use XML-derived normalized IR as the authoritative structured source.
