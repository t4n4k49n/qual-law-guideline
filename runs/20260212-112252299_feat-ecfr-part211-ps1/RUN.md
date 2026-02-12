# RUN: 20260212-112252299_feat-ecfr-part211-ps1

- Date: 2026-02-12 11:22:52
- Branch: feat/ecfr-part211-ps1
- Task: eCFR APIからTitle 21のPart 211/Part 21 XMLを取得して指定フォルダへ保存

## Actions
- scripts/download-ecfr-part211.ps1 を作成
- Title 21の最新スナップショット日付をAPIから取得（2026-02-10）
- Part 211を取得: title-21_part-211_2026-02-10.xml
- Part 21を取得: title-21_part-21_2026-02-10.xml

## Outputs
- %USERPROFILE%/Documents/GitHub/qual-law-guideline_OLD-HANDMADE/data/xml/www.govinfo.gov_bulkdata_ECFR_title-21/title-21_part-211_2026-02-10.xml
- %USERPROFILE%/Documents/GitHub/qual-law-guideline_OLD-HANDMADE/data/xml/www.govinfo.gov_bulkdata_ECFR_title-21/title-21_part-21_2026-02-10.xml
