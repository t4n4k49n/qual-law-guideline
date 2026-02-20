# PR: 20260220-183649508_run-normalized-335AC0000000145-v4

## タイトル
正規化RUN: `jp_egov_335AC0000000145_20260501_507AC0000000037` を再生成

## 対象法令
- e-Gov: https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037
- doc_id: `jp_egov_335AC0000000145_20260501_507AC0000000037`

## 変更内容
- `runs/20260220-183649508_run-normalized-335AC0000000145-v4/promotion_candidate/` に4ファイル + `manifest.yaml` を生成
- 人間レビュー素材を `runs/20260220-183649508_run-normalized-335AC0000000145-v4/` に保存

## 検証結果
- `assert_unique_nids`: pass
- `check_annex_article_nids`: pass
- `check_appendix_scoped_indices`: pass
- `check_ord_format_and_order`: pass

## 深い階層サンプル（ルール確認）
| 項目 | 内容 |
|---|---|
| 最深item nid | `art63.p1.i2` |
| human path（numあり階層を省略しない） | 第九章 医薬品等の取扱い -> 第五節 医療機器の取扱い -> 第六十三条 （直接の容器等の記載事項） -> 1 -> 二 名称 |
| YAML path | `art63.p1.i2` |
| 祖先/階層数の整合 | human path階層数=5, YAMLで辿る階層数=5（一致） |

## まとめ
本RUNでは、指定法令XMLに対する正規化出力（IR / parser_profile / regdoc_profile / meta）を再生成し、最小検証で重大な問題がないことを確認しました。正規化RUNとして、成果物を昇格可能な状態まで整備できています。
