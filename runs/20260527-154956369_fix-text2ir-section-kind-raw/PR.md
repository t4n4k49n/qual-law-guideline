## まとめ

text2irで番号付きsectionの `kind_raw` が実際の原文マーカーではなくprofileの固定例示値になる問題を修正します。PIC/S Annex 11の正式化前にこの修正を入れることで、レビュー表とIR上の `kind_raw` が原文の `14.` などと一致し、転記・確認時の誤解を避けられます。

## 変更内容

- `section` の `kind_raw` をmatchしたraw token優先に変更
- PIC/S Annex 11 fixtureに `14. Electronic Signature` を追加
- `section_14.kind_raw == "14."` の回帰テストを追加
- RUN記録を追加

## 検証

- `.\.venv\Scripts\python.exe -m pytest tests/test_pics_annex11_profile.py -q`
- `.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_bundle.py tests/test_text2ir_profiles_pics.py -q`
- 実データ再生成で `ann11.sec14.kind_raw` が `14.` になることを確認

<!-- PR_BODY_FILE: runs/20260527-154956369_fix-text2ir-section-kind-raw/PR.md -->
