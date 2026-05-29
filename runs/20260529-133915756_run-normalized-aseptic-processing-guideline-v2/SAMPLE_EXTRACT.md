# 深い階層サンプル抽出

- source: `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/promotion_candidate/jp_pmda_aseptic_processing_guideline_20110420.regdoc_ir.yaml`
- target_nid: `cha3.sec3_1.i1`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha3` | `chapter` | `1.` | `品質システム` |
| 3 | `cha3.sec3_1` | `section` | `３．１` | `品質システム一般要求事項` |
| 4 | `cha3.sec3_1.i1` | `item` | `1）` | `全般 品質システムには組織構成，手順，工程，資源の他，本指針で規定する無菌操作法で無菌医 薬品を製造するための要件に適合する信頼性を保証するために必要な活動が含まれているこ と． 無菌性を含め品質に関わる全ての活動を明確に示し，文書化すること．無菌操作法で製造す る製造所は，工程中での製品の微生物汚染を回避するために必要な管理基準を設定し，適 切に運用する必要があることから，無菌医薬品製造に関わる品質システムを設定すること．品 質システムには無菌操作の不具合，及び監視項目での異常並びに逸脱などが発生した時の 調査システムと是正・予防と是正・予防後の検証システムを含むこと．` |
