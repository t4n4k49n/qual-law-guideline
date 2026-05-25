<!-- PR_BODY_FILE: runs/20260525-235003289_feat-mhlw-csv-annex-source-recovery/PR.md -->

## まとめ

CSVガイドライン別紙の次工程に入る前提として、別紙1/2の正本候補と復元方法をCSV個別開発として切り分けました。別紙1は画像由来でOCR等が必要、別紙2は公式page2 HTMLに表本体があるためOCRなしでHTML表parserへ進める、という判断をRUN成果物として追跡できます。

## 変更内容

- CSV専用のソース回収inventory `mhlw_csv_annex_source_recovery` を追加
- `別紙1` 画像エンドポイントと `別紙2` 公式page2 HTMLを回収候補として記録
- `runs/20260525-235003289_feat-mhlw-csv-annex-source-recovery/` にRUN、inventory、検証結果を追加
- 共通HTML抽出器・共通Parserには変更なし

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_mhlw_csv_annex_source_recovery.py tests\test_mhlw_csv_annexes.py tests\test_text2ir_csv_guideline.py tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `14 passed`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-235003289_feat-mhlw-csv-annex-source-recovery --doc-id jp_mhlw_csv_guideline_source_recovery_v1 --mode normal --out runs\20260525-235003289_feat-mhlw-csv-annex-source-recovery\goal_check.md
```

結果: `PASS`

```powershell
.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --bundle-dir out\20260525-235003289_feat-mhlw-csv-annex-source-recovery --doc-id jp_mhlw_csv_guideline_source_recovery_v1 --mode normal --out runs\20260525-235003289_feat-mhlw-csv-annex-source-recovery\special_structure_audit.md
```

結果: `pass`

## 備考

- 公式page2: `https://www.mhlw.go.jp/web/t_doc?dataId=00tb6573&dataType=1&pageNo=2`
- 別紙1画像: `https://www.mhlw.go.jp/web/t_img?img=6676058`
- `data/normalized/` への昇格は行っていません。
