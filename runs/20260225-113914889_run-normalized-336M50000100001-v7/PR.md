# PR: 20260225-113914889_run-normalized-336M50000100001-v7

## タイトル
正規化RUN: $docId を再生成

## 対象法令
- e-Gov: https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117
- doc_id: $docId

## 変更内容
- uns/20260225-113914889_run-normalized-336M50000100001-v7/promotion_candidate/ に4ファイル + manifest.yaml を生成
- 人間レビュー素材を uns/20260225-113914889_run-normalized-336M50000100001-v7/ に保存
- 本PRは親PR（レビュー用）であり、data/normalized/ の変更は含まない

## 検証結果
- ssert_unique_nids: pass
- check_annex_article_nids: pass
- check_appendix_scoped_indices: pass
- check_ord_format_and_order: pass
- check_article_paragraph_structure: pass

## 深い階層サンプル（ルール確認）
| 項目 | 内容 |
|---|---|
| 最深item nid | rt114_54.p1.i12.ro.pt1 |
| 最深item本文 | 容易に、かつ、安全に取り扱うことができること。 |
| human path（numあり階層を省略しない） | 第三章 医療機器及び体外診断用医薬品の製造販売業及び製造業等 -> 第一節 医療機器及び体外診断用医薬品の製造販売業及び製造業 -> 第百十四条の五十四 （医療機器又は体外診断用医薬品の製造販売業者の遵守事項） -> 1 -> 十二 -> ロ -> （１） |
| YAML path（ancestor nid chain） | ch3 -> ch3.sec1 -> art114_54 -> art114_54.p1 -> art114_54.p1.i12 -> art114_54.p1.i12.ro -> art114_54.p1.i12.ro.pt1 |
| 祖先/階層数の整合 | human path階層数=7, YAMLで辿る階層数=7（一致） |

## まとめ
本RUNでは、指定法令XMLに対する正規化出力（IR / parser_profile / regdoc_profile / meta）を再生成し、最小検証で重大な問題がないことを確認しました。正規化RUNの主目的である出力健全性を満たした状態で、昇格レビュー可能な成果物を整備できています。

<!-- PR_BODY_FILE: runs/20260225-113914889_run-normalized-336M50000100001-v7/PR.md -->
