## まとめ

法令・ガイドライン正規化の残課題を `eu_gmp_vol4_chap9_undated`、21 CFR Part 11 XML、21 CFR Part 211 XML の3件に整理し、そのうち EU GMP Chapter 9 の `undated` 解消可否を確認しました。現時点の一次資料からは文書日付を確定できないため、拙速に dated doc_id へ変更せず、根拠不足として維持する判断を記録します。

## 変更内容

- `local_notes/TODO.md` の冒頭に残課題3件を明記
- Chapter 9のローカルPDF/TXT、現行公式URL、旧公式URLの確認結果をRUNに記録
- HTTPヘッダのスナップショットを `http_headers.json` として保存

## 判断

- `cap9_en.pdf` / `cap9_en.txt` の本文には日付がない
- 現行公式URLのHEAD応答には文書日付として使える `Last-Modified` がない
- 旧URLの `/system/files/2016-11/` と `Last-Modified: 2021-12-01` はホスティング/移行情報であり、文書版日付として採用しない
- よって、現時点では `eu_gmp_vol4_chap9_undated` を維持する

## 次の判断

公式索引やアーカイブ等で明確なChapter 9の版日付が見つかった場合だけ、dated doc_idへ置き換える小さな正規化RUNを行います。見つからない場合は `undated` を受容して、残る正規化課題を 21 CFR Part 11 / Part 211 XML に移します。

<!-- PR_BODY_FILE: runs/20260601-183200000_eu-gmp-chap9-undated-prep/PR.md -->
