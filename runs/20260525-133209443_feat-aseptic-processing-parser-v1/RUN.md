# RUN: 20260525-133209443_feat-aseptic-processing-parser-v1

## 目的

7「無菌操作法指針」向けの `text2ir` parser profile を開発する。

このRUNはParser開発であり、正式な正規化RUNではない。`data/normalized/` への昇格や、正規化承認を前提にしない。

## 対象

- ソース: `data/human-readable/pmda/aseptic_processing_guideline/source_texts/000206144.txt`
- 公開元URL: `https://www.pmda.go.jp/files/000206144.pdf`
- 出力確認先: `out/20260525-133209443_feat-aseptic-processing-parser-v1/`

## 実施内容

- 無菌操作法指針専用profile `jp_pmda_aseptic_processing_guideline_v1` を追加した。
  - 共通 `jp_guideline_default_v1` を継承する。
  - 冒頭通知、研究班、作成者一覧、目次を本文開始の `１．序論` まで除外する。
  - 本文の全角章番号 `１．`、節番号 `２．１` などを扱う。
  - 文書タイトル行の除去は、この専用profileに閉じる。
- 日本語番号正規化で全角英字を半角化するようにした。
  - 例: `Ａ１` -> `A1`
  - 日本語PDF由来TXTで一般的に起こる表記ゆれとして共通正規化に含めた。
- 参考情報の `Ａ１` / `A1.1` 系を共通 `JP_GUIDELINE` profileに追加した。
  - 付録・参考情報系の番号体系として、7固有ではなく複数ガイドラインに出得るため。
- 共通 `JP_GUIDELINE` profileから文書固有のタイトル・機関名除去を外した。
  - `原薬ＧＭＰのガイドライン` と `無菌操作法による無菌医薬品の製造に関する指針` は、それぞれ専用profile側で扱う。
  - `国立感染症研究所` / `病原体等安全管理規程` は、8向け開発時に必要性を判断する。
- 実データbundleを `out/` に生成し、構造確認を行った。

## 検証

```powershell
python -m pytest tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_jp_guideline.py tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_eu_gmp_chap1.py tests\test_text2ir_who_lbm_3rd.py tests\test_text2ir_profiles_pics.py tests\test_text2ir_cfr_quality_v2.py tests\test_text2ir_goal_check.py tests\test_profile_loader_extends.py tests\test_markdown_table_parsing.py tests\test_table_note_real_samples.py -q
```

結果: `43 passed`

```powershell
.venv\Scripts\python.exe -m qai_text2ir.cli bundle --input data\human-readable\pmda\aseptic_processing_guideline\source_texts\000206144.txt --out-dir out\20260525-133209443_feat-aseptic-processing-parser-v1 --doc-id jp_pmda_aseptic_processing_guideline_trial --title "無菌操作法による無菌医薬品の製造に関する指針" --short-title "無菌操作法指針" --doc-type guideline --source-url https://www.pmda.go.jp/files/000206144.pdf --source-format txt --retrieved-at 2026-05-23 --jurisdiction JP --language ja --family JP_GUIDELINE --parser-profile-id jp_pmda_aseptic_processing_guideline_v1 --strict
```

結果: bundle生成成功、qualitycheck warning なし。

```powershell
.venv\Scripts\python.exe -m qai_text2ir.goal_check --bundle-dir out\20260525-133209443_feat-aseptic-processing-parser-v1 --doc-id jp_pmda_aseptic_processing_guideline_trial --mode normal --format markdown --out runs\20260525-133209443_feat-aseptic-processing-parser-v1\goal_check.md
```

結果: `PASS`

## 実データ確認サンプル

本文:

`document/root` -> `chapter cha3`（3 品質システム） -> `paragraph cha3.p3_1`（3.1 品質システム一般要求事項）

参考情報:

`document/root` -> `chapter chaA1`（A1 細胞培養／発酵により製造する原薬） -> `paragraph chaA1.pA1_1`（A1.1 一般要件）

## 残課題

`special_structure_audit` では、固定幅表候補が3件残る。

- `cha7.p7_1`
- `cha11.p11_3`
- `cha11.p11_3.pre1`

これは正式正規化ではなくParser開発段階のため、本PRでは本文階層・参考情報階層の安定化までを対象とする。表候補は、今後の個別table adapter開発の検討材料として扱う。
