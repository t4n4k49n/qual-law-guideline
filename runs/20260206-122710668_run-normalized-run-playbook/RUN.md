# RUN 20260206-122710668_run-normalized-run-playbook

## Summary
- doc_id運用をe-Gov URI準拠に変更（`jp_egov_<law_id>_<as_of>_<revision_id>`）
- xml2ir 再実行（入力: 336M50000100002_20260501_507M60000100117.xml）
- 4ファイル（IR / parser_profile / regdoc_profile / meta）を出力
- manifest.yaml を更新（検証/レビュー結果を記録）

## Command
python -m qai_xml2ir.cli --input "C:\Users\ryoki\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\336M50000100002_20260501_507M60000100117\336M50000100002_20260501_507M60000100117.xml" --out-dir "out\20260206-122710668_run-normalized-run-playbook" --doc-id "jp_egov_336M50000100002_20260501_507M60000100117" --emit-only all

## Outputs
- out\20260206-122710668_run-normalized-run-playbook\jp_egov_336M50000100002_20260501_507M60000100117.regdoc_ir.yaml
- out\20260206-122710668_run-normalized-run-playbook\jp_egov_336M50000100002_20260501_507M60000100117.parser_profile.yaml
- out\20260206-122710668_run-normalized-run-playbook\jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml
- out\20260206-122710668_run-normalized-run-playbook\jp_egov_336M50000100002_20260501_507M60000100117.meta.yaml
- out\20260206-122710668_run-normalized-run-playbook\manifest.yaml

## Checks
- verify.py: assert_unique_nids / check_annex_article_nids / check_appendix_scoped_indices => PASS
- AIレビュー（目視代替）:
  - サンプル断片:
    - 第二章 医薬品等の製造業 / 第一節 医薬品の製造業 / 第九条 （放射性医薬品区分の医薬品製造業者等の製造所の構造設備） / 1 / 四 / ヌ / （１）
      - 外部と区画された構造であること。
  - 判定: 条文→段落→号→イロハ→枝番の階層が妥当で、本文の欠落・順序の逆転は見当たらない。
  - 備考: 人の最終確認はPRで実施する前提。

## Notes
- 旧 doc_id（jp_test_336M50000100002_20260501）の成果物は `out\20260206-122710668_run-normalized-run-playbook\archive\20260206-145630\` に退避。
- 実行日時: 2026-02-06 14:57 頃
