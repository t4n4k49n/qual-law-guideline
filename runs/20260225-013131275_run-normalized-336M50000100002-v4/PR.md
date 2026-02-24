# PR: 20260225-013131275_run-normalized-336M50000100002-v4

## タイトル
正規化RUN: $docId を再生成

## 対象法令
- e-Gov: https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117
- doc_id: $docId

## 変更内容
- uns/20260225-013131275_run-normalized-336M50000100002-v4/promotion_candidate/ に4ファイル + manifest.yaml を生成
- 人間レビュー素材を uns/20260225-013131275_run-normalized-336M50000100002-v4/ に保存
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
| 最深item nid | rt8.p1.i1.i.pt1 |
| human path（numあり階層を省略しない） | 第二章 医薬品等の製造業 -> 第一節 医薬品の製造業 -> 第八条 （特定生物由来医薬品等の医薬品製造業者等の製造所の構造設備） -> 1 -> 一 -> イ -> （１） |
| YAML path | ch2.ch2.sec1.art8.art8.p1.art8.p1.i1.art8.p1.i1.i.art8.p1.i1.i.pt1 |
| 祖先/階層数の整合 | human path階層数=7, YAMLで辿る階層数=7（一致） |

## まとめ
本RUNでは、指定法令XMLに対する正規化出力（IR / parser_profile / regdoc_profile / meta）を再生成し、最小検証で重大な問題がないことを確認しました。正規化RUNの主目的である出力健全性を満たした状態で、昇格レビュー可能な成果物を整備できています。
