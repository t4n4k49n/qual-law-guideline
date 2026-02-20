# PR: 20260220-150730845_run-normalized-336CO0000000011-v4

## タイトル
正規化RUN: `jp_egov_336CO0000000011_20260501_507CO0000000362` を再生成

## 対象法令
- e-Gov: https://laws.e-gov.go.jp/law/336CO0000000011/20260501_507CO0000000362
- doc_id: `jp_egov_336CO0000000011_20260501_507CO0000000362`

## 変更内容
- `out/20260220-150730845_run-normalized-336CO0000000011-v4/` に4ファイル + `manifest.yaml` を生成
- 人間レビュー用に最深item比較の断片を `runs/20260220-150730845_run-normalized-336CO0000000011-v4/` へ保存

## 検証結果
- `assert_unique_nids`: pass
- `check_annex_article_nids`: pass
- `check_appendix_scoped_indices`: pass
- `check_ord_format_and_order`: pass

## 比較表（人間レビュー用）
| 観点 | 旧（normalized） | 新（out/20260220-150730845_run-normalized-336CO0000000011-v4） | 判定 |
|---|---|---|---|
| 最深item nid | `art37_6.p3.i2` | `art37_6.p3.i2` | 一致 |
| 最深item text | `第二種医療機器製造販売業許可を受けている者が第一種医療機器製造販売業許可を受けた場合` | `第二種医療機器製造販売業許可を受けている者が第一種医療機器製造販売業許可を受けた場合` | 互換維持 |
| parser_profile.id | `jp_law_default_v1` | `jp_law_default_v1` | unchanged |
| meta tool.version | `null or previous` | `0.1.0` | 記録あり |

## 深い階層サンプル（ルール確認）
- 選定結果:
  - 最深item: `art37_6.p3.i2`（深さ=5）
  - 同列item数: 3
  - 同列最短: `art37_6.p3.i2`（`第二種医療機器製造販売業許可を受けている者が第一種医療機器製造販売業許可を受けた場合`）

| 項目 | 内容 |
|---|---|
| human path（numあり階層を省略しない） | 第五章 医療機器及び体外診断用医薬品の製造販売業及び製造業等 -> 第一節 医療機器及び体外診断用医薬品の製造販売業及び製造業 -> 第三十七条の六 （製造販売業の許可の特例等） -> ３ -> 二 第二種医療機器製造販売業許可を受けている者が第一種医療機器製造販売業許可を受けた場合 |
| YAML path | `art37_6.p3.i2` |
| 祖先/階層数の整合 | human path階層数=5, YAMLで辿る階層数=5（一致） |

## まとめ
本RUNでは、指定法令XMLに対する正規化出力（IR / parser_profile / regdoc_profile / meta）を再生成し、最小検証と比較確認で重大な問題がないことを確認しました。正規化RUNとして、成果物を昇格可能な状態まで整備できています。
