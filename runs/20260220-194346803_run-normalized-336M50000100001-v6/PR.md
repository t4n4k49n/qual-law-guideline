# PR: 20260220-194346803_run-normalized-336M50000100001-v6

## タイトル
正規化RUN: `jp_egov_336M50000100001_20260501_507M60000100117` を再生成

## 対象法令
- e-Gov: https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117
- doc_id: `jp_egov_336M50000100001_20260501_507M60000100117`

## 変更内容
- `runs/20260220-194346803_run-normalized-336M50000100001-v6/promotion_candidate/` に4ファイル + `manifest.yaml` を生成
- 人間レビュー素材を `runs/20260220-194346803_run-normalized-336M50000100001-v6/` に保存

## 検証結果
- `assert_unique_nids`: pass
- `check_annex_article_nids`: pass
- `check_appendix_scoped_indices`: pass
- `check_ord_format_and_order`: pass

## 深い階層サンプル（ルール確認）
| 項目 | 内容 |
|---|---|
| 最深item nid | `art114_45_3.p1.i3` |
| human path（numあり階層を省略しない） | 第三章 医療機器及び体外診断用医薬品の製造販売業及び製造業等 -> 第一節 医療機器及び体外診断用医薬品の製造販売業及び製造業 -> 第百十四条の四十五の三 （変更計画の確認を受けることができる場合） -> 1 -> 三 原材料 |
| YAML path | `art114_45_3.p1.i3` |
| 祖先/階層数の整合 | human path階層数=5, YAMLで辿る階層数=5（一致） |

## まとめ
本RUNでは、指定法令XMLに対する正規化出力（IR / parser_profile / regdoc_profile / meta）を再生成し、最小検証で重大な問題がないことを確認しました。正規化RUNとして、成果物を昇格可能な状態まで整備できています。
