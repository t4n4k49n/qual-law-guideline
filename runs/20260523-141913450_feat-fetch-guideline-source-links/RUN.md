# RUN: XML source alternatives fetch

- run_id: `20260523-141913450_feat-fetch-guideline-source-links`
- branch: `feat/fetch-guideline-source-links`
- purpose: 既に取得した原文リンク群について、より処理しやすい公式XMLが存在するケースを確認し、存在したものを取得する。

## 実施内容

- e-Gov 5件は既存処理がXMLベースであり、追加取得対象から除外した。
- eCFR Versioner API から、21 CFR Part 11 / Part 211 のXMLを取得した。
- eCFR は `versions/title-21.json` で 2026-05-23 時点の最新 content version を確認し、`2025-10-27` 版を使用した。
- 取得結果の機械可読ログを `XML_FETCHED_SOURCES.json` として保存した。

## 取得できたXML

| 文書 | 保存先 |
|---|---|
| FDA 21 CFR Part 11 | `data/human-readable/cfr/source_xml/title21_part11_2025-10-27.xml` |
| FDA 21 CFR Part 211 | `data/human-readable/cfr/source_xml/title21_part211_2025-10-27.xml` |

## XML未確認

以下は今回の確認範囲では、公式XMLの取得口を確認できなかったため追加取得していない。

- EU GMP Volume 4 / Annexes
- PIC/S PE 009 bundled PDFs
- WHO LBM
- PMDA PDF文書群
- NIID PDF
- MHLW CSV HTML

## 成果物

- `runs/20260523-141913450_feat-fetch-guideline-source-links/XML_FETCHED_SOURCES.json`
- `out/20260523-141913450_feat-fetch-guideline-source-links/XML_FETCHED_SOURCES.json`
