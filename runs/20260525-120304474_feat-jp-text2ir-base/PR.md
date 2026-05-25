<!-- PR_BODY_FILE: runs/20260525-120304474_feat-jp-text2ir-base/PR.md -->

## まとめ

6/7/8/9 の正規化を個別に進める前提として、日本語ガイドライン文書を `text2ir` に通すための共通基盤を追加しました。これにより、全角数字・丸数字・日本語の条番号など、複数文書で共通して出る表記ゆれを同じ入口で扱えるようになります。

## 変更内容

- `JP_GUIDELINE` family の既定プロファイルを追加
- 日本語番号表記の正規化を `text_parser` に追加
- MHLW T番号HTML向けの本文抽出コマンド `extract-mhlw-html` を追加
- `JP_GUIDELINE` のプロファイルロード経路を追加
- 日本語ガイドライン共通基盤のテストを追加

## 検証

```powershell
python -m pytest tests\test_text2ir_jp_guideline.py -q
```

結果: `3 passed`

```powershell
python -m pytest tests\test_text2ir_eu_gmp_chap1.py tests\test_text2ir_who_lbm_3rd.py tests\test_text2ir_profiles_pics.py tests\test_text2ir_cfr_quality_v2.py tests\test_text2ir_goal_check.py tests\test_profile_loader_extends.py -q
```

結果: `26 passed`

## 補足

API GMP全文の試験変換では、章番号の重複に関する品質警告が残っています。これは本PRの共通基盤ではなく、次フェーズの API GMP 個別正規化で調整します。

