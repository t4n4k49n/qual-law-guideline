# RUN 20260206-122710668_run-normalized-run-playbook

## Summary
- xml2ir 実行（入力: 336M50000100002_20260501_507M60000100117.xml）
- 4ファイル（IR / parser_profile / regdoc_profile / meta）を出力
- manifest.yaml を作成（検証/レビュー結果を記録）

## Command
python -m qai_xml2ir.cli --input "%USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336M50000100002_20260501_507M60000100117\336M50000100002_20260501_507M60000100117.xml" --out-dir "out\20260206-122710668_run-normalized-run-playbook" --doc-id "jp_test_336M50000100002_20260501" --emit-only all

## Outputs
- out\20260206-122710668_run-normalized-run-playbook\jp_test_336M50000100002_20260501.regdoc_ir.yaml
- out\20260206-122710668_run-normalized-run-playbook\jp_test_336M50000100002_20260501.parser_profile.yaml
- out\20260206-122710668_run-normalized-run-playbook\jp_test_336M50000100002_20260501.regdoc_profile.yaml
- out\20260206-122710668_run-normalized-run-playbook\jp_test_336M50000100002_20260501.meta.yaml
- out\20260206-122710668_run-normalized-run-playbook\manifest.yaml

## Checks
- verify.py: assert_unique_nids / check_annex_article_nids / check_appendix_scoped_indices => PASS
- AIレビュー（目視代替）:
  - サンプル断片:
    - art1.p1: 薬局の構造設備の基準は、次のとおりとする。
    - art1.p1.i1: 調剤された薬剤又は医薬品を購入し、又は譲り受けようとする者が容易に出入りできる構造であり、薬局であることがその外観から明らかであること。
    - art1.p1.i2: 換気が十分であり、かつ、清潔であること。
    - art1.p1.i3: 当該薬局以外の薬局又は店舗販売業の店舗の場所、常時居住する場所及び不潔な場所から明確に区別されていること。
    - art1.p1.i4: 面積は、おおむね一九・八平方メートル以上とし、薬局の業務を適切に行なうことができるものであること。
  - 判定: 条文→段落→号の階層が妥当で、本文の欠落・順序の逆転は見当たらない。
  - 備考: 人の最終確認はPRで実施する前提。

## Notes
- 実行日時: 2026-02-06 12:31 頃
