# RUN 20260206-180426878_run-normalized-335AC0000000145

## Summary
- 入力XML（PMD Act）を xml2ir で正規化（IR変換）
- erify.py の最小整合性チェックをパス

## Input
- Path: $input_path
- DocID: $doc_id

## Outputs
- out/20260206-180426878_run-normalized-335AC0000000145/
  - *.regdoc_ir.yaml: IR本体
  - *.parser_profile.yaml: パーサ設定（再現用）
  - *.regdoc_profile.yaml: 文書固有設定
  - *.meta.yaml: メタデータ

## Command
- python -m qai_xml2ir.cli --input "%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\335AC0000000145_20260501_507AC0000000037\335AC0000000145_20260501_507AC0000000037.xml" --out-dir out/20260206-180426878_run-normalized-335AC0000000145 --doc-id jp_egov_335AC0000000145_20260501_507AC0000000037 --emit-only all

## Verification
- Script: src/qai_xml2ir/verify.py
- Result: PASS
  - ssert_unique_nids: OK
  - check_annex_article_nids: OK (collisions=[], invalid_annex=[])
  - check_appendix_scoped_indices: OK (problems=[])

## AI Review（目視代替）
- サンプル断片（祖先含む）
  - document
  - chapter | num=第七章 | 医薬品、医療機器及び再生医療等製品の販売業等
  - section | num=第一節 | 医薬品の販売業
  - article | num=第二十九条の二 | （店舗販売業者の遵守事項）
  - paragraph | num=1 | 厚生労働大臣は、厚生労働省令で、次に掲げる事項その他店舗の業務に関し店舗販売業者が遵守すべき事項を定めることができる。
  - item | num=二 | 店舗における医薬品の販売又は授与の実施方法（その店舗においてその店舗以外の場所にいる者に対して次のイ又はロに掲げる医薬品を販売し、又は授与する場合におけるその者との間の通信手段に応じた当該実施方法を含む。）に関する事項
  - subitem | num=ロ | 一般用医薬品
- 最終確認はPRで人間が実施する前提。

## Notes
- CLI は undle サブコマンド無しで実行（python -m qai_xml2ir.cli）。
