# RUN: PDF text extraction for unnormalized sources

- run_id: `20260523-154243089_feat-fetch-guideline-source-links`
- branch: `feat/fetch-guideline-source-links`
- purpose: 原文のみ取得済みで未正規化の優先文書について、PDF原文を `qai_text2ir` へ投入できるTXTへ変換する。

## 実施内容

- Poppler `pdftotext` を使用した。
- 実行形式: `pdftotext -layout -nopgbrk -enc UTF-8 <pdf> <txt>`
- 既存TXTへの上書きを避けるため、今回の生成物は各文書配下の `source_texts/` に配置した。

## 対象

- PMDA API GMP guideline
- PMDA 無菌操作法指針
- NIID 病原体等安全管理規程
- EU GMP Volume 4 PDFセット

## 成果物

- `runs/20260523-154243089_feat-fetch-guideline-source-links/PDF_TEXT_EXTRACTION_RESULTS.json`
- `out/20260523-154243089_feat-fetch-guideline-source-links/PDF_TEXT_EXTRACTION_RESULTS.json`

## 備考

- すべての対象PDFでテキスト抽出が成立した。
- OCRは使用していない。
