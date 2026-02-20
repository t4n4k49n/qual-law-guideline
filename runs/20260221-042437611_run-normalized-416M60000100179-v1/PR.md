# PR: 20260221-042437611_run-normalized-416M60000100179-v1

## タイトル
正規化RUN: `jp_egov_416M60000100179_20260501_507M60000100117` を再生成

## 対象法令
- e-Gov: https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117
- doc_id: `jp_egov_416M60000100179_20260501_507M60000100117`

## 変更内容
- `runs/20260221-042437611_run-normalized-416M60000100179-v1/promotion_candidate/` に4ファイル + `manifest.yaml` を生成
- 人間レビュー素材を `runs/20260221-042437611_run-normalized-416M60000100179-v1/` に保存
- 本PRは親PR（レビュー用）であり、`data/normalized/` の変更は含まない

## 検証結果
- `assert_unique_nids`: pass
- `check_annex_article_nids`: pass
- `check_appendix_scoped_indices`: pass
- `check_ord_format_and_order`: pass

## 深い階層サンプル（ルール確認）
| 項目 | 内容 |
|---|---|
| 最深item nid | `art8.p1.i14` |
| human path（numあり階層を省略しない） | 第二章 医薬品製造業者等の製造所における製造管理及び品質管理 -> 第一節 通則 -> 第八条 （手順書等） -> 1 -> 十四 |
| YAML path | `art8.p1.i14` |
| 祖先/階層数の整合 | human path階層数=5, YAMLで辿る階層数=5（一致） |

## まとめ
本RUNでは、指定法令XMLに対する正規化出力（IR / parser_profile / regdoc_profile / meta）を再生成し、最小検証で重大な問題がないことを確認しました。正規化RUNの主目的である出力健全性を満たした状態で、昇格レビュー可能な成果物を整備できています。