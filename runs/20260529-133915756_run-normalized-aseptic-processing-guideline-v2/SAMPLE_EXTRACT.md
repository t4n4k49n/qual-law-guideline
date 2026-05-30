# 深い階層サンプル抽出

- source: `runs/20260529-133915756_run-normalized-aseptic-processing-guideline-v2/promotion_candidate/jp_pmda_aseptic_processing_guideline_20110420.regdoc_ir.yaml`
- target_nid: `cha3.sec3_1.i7`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha3` | `chapter` | `1.` | `品質システム` |
| 3 | `cha3.sec3_1` | `section` | `３．１` | `品質システム一般要求事項` |
| 4 | `cha3.sec3_1.i7` | `item` | `7）` | `予測的バリデーション及び工程管理の定期照査製品の無菌性に係る全ての工程及び行為が無菌性を保証する科学的根拠に基づく設計・運用を模倣して実証する行為であるバリデーションを実行すること．また，設定した工程管理プログラムはバリデーションで検証すること．` |
