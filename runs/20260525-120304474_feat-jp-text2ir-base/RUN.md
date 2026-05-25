# RUN: 20260525-120304474_feat-jp-text2ir-base

## 目的

`docs/NORMALIZATION_PLAN_6_9.md` のフェーズ1として、日本語ガイドライン系文書を `text2ir` に投入するための共通基盤を追加する。

対象範囲は、6/7/8/9 の個別正規化に先立つ共通部品に限定する。

## 実施内容

- `JP_GUIDELINE` family の既定プロファイルを追加した。
  - 全角数字、全角ピリオド、丸数字、`第9条の2` 型の番号を正規化する。
  - 日本語ガイドラインに多い章、条、節、項目、丸数字、箇条書き、プレーンテキスト表を扱う。
- `text_parser` の番号抽出を日本語番号表記に対応させた。
- MHLW T番号HTML向けの抽出コマンド `extract-mhlw-html` を追加した。
  - `#contents .eline p` を中心に本文行を抽出する。
  - 目次見出しや目次専用行を除外する。
- `JP_GUIDELINE` のプロファイルロード経路を追加した。
- 日本語ガイドライン向けの単体テストを追加した。

## 検証

以下を実行し、成功を確認した。

```powershell
python -m pytest tests\test_text2ir_jp_guideline.py -q
```

結果: `3 passed`

```powershell
python -m pytest tests\test_text2ir_eu_gmp_chap1.py tests\test_text2ir_who_lbm_3rd.py tests\test_text2ir_profiles_pics.py tests\test_text2ir_cfr_quality_v2.py tests\test_text2ir_goal_check.py tests\test_profile_loader_extends.py -q
```

結果: `26 passed`

また、既存ソース `data/human-readable/pmda/api_gmp_guideline/source_texts/000156438.txt` に対して `JP_GUIDELINE` profile の試験変換を実施し、bundle 生成自体が完了することを確認した。

## 既知事項

API GMP全文の試験変換では、章番号の重複に関する品質警告が残る。これは共通基盤ではなく、フェーズ2の API GMP 個別正規化でプロファイルまたは前処理を調整する。

