# RUN: 20260212-115234311_feat-eu-gmp-chap1-text2ir

Input source URL: https://health.ec.europa.eu/document/download/e458c423-f564-4171-b344-030a461c567f_en
Retrieved at: 2026-02-12

PDF to text procedure:
- Command: pdftotext -layout -nopgbrk "%USERPROFILE%/Documents/GitHub/qual-law-guideline_OLD-HANDMADE/data/human-readable/10.EU GMP/Part I/vol4-chap1_2013-01_en.pdf" data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt
- Post-process: normalize line endings to LF and save as UTF-8 (no BOM).

Bundle argv:
- python -m qai_text2ir.cli --input data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt --out-dir out/20260212-115234311_feat-eu-gmp-chap1-text2ir --doc-id eu_gmp_vol4_chap1_20130131 --title "EU GMP Vol.4 Chapter 1 Pharmaceutical Quality System" --short-title "EU GMP Ch1 PQS" --jurisdiction EU --language en --doc-type guideline --source-url "https://health.ec.europa.eu/document/download/e458c423-f564-4171-b344-030a461c567f_en" --source-format pdf --retrieved-at "2026-02-12" --eu-volume "4" --parser-profile src/qai_text2ir/profiles/eu_gmp_chap1_default_v1.yaml --emit-only all

Visual review:
- root > chapter(1) exists, chapter heading contains "Pharmaceutical Quality System".
- paragraph 1.1..1.10 are present and prose is attached.
- paragraph 1.4 has item nodes (i) through (xiv).
- paragraph 1.8 contains bullet-derived subitem nodes.
- No structural-break warnings were observed; one non-fatal hyphen-wrap quality warning remains (item xiv), noted for next cleanup phase.
