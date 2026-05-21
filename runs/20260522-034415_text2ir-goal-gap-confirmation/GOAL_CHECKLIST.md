# GOAL_CHECKLIST

## 結論

現行の正式正規化GOALは、`qai_xml2ir` が生成する `qai.regdoc_ir.v4` の4ファイル構成を基準にする。ただし text2ir はPDF由来テキスト等を扱うため、完全同型ではなく、DQ/GMPチェックシート、検索、表示、レビュー、差分管理、監査説明で同等に扱えることをGOALとする。

## チェックリスト

| 項目 | GOAL | 根拠 | text2ir評価で見ること |
|---|---|---|---|
| IR schema | `qai.regdoc_ir.v4` | `src/qai_xml2ir/models_ir.py` | 生成IRの `schema` がv4である |
| Node共通フィールド | `kind`, `nid`, `num`, `heading`, `text`, `ord`, `role`, `normativity`, `kind_raw`, `source_spans`, `tags`, `children`, `data` | `src/qai_xml2ir/models_ir.py` | 欠損しても下流利用に影響しない形で出力される |
| `nid` | 全ノード一意。選択・参照のキー | `src/qai_xml2ir/verify.py` | duplicateがない |
| `ord` | root以外は正の整数で一意、文書順で単調増加 | `src/qai_xml2ir/verify.py` | missing/duplicate/order violationがない |
| `source_spans` | 入力元との対応を追える | `models_ir.py`, 正式版meta | root以外の主要ノードに入力行等のlocatorがある |
| `data` | v4要素。表セル等の構造payloadに使える | `models_ir.py`, `egov_parser.py` | table系ではpayloadを保持できる。通常文書では空でもよい |
| 4ファイル | `regdoc_ir.yaml`, `parser_profile.yaml`, `regdoc_profile.yaml`, `meta.yaml` | README, 4FILES guide | 全ファイルが揃う |
| `meta.yaml` | doc識別子、source、bundle、generationを含む | 正式版 `data/normalized/*/*.meta.yaml` | source/generation/bundleが説明可能 |
| `parser_profile.yaml` | parser profile idと構造ルールを含む | 正式版/CLI | 使用profileとprovenanceが説明可能 |
| `regdoc_profile.yaml` | `dq_gmp_checklist` を含む | `models_profiles.py`, 4FILES guide | selectable/context/groupingが標準項目を満たす |
| `dq_gmp_checklist` | `candidate_visibility`, `selectable_kinds`, `grouping_policy`, `context_display_policy` | 4FILES guide, tests | table_rowとnote descendant表示も含められる |
| verify/qualitycheck | nid/ord/構造検証、text2ir品質警告のstrict化 | `verify.py`, `text_parser.py`, `cli.py` | strict成功だけでなくGOAL観点の目視/集計も残す |

## 今回の判定基準

- v4、4ファイル、manifest、source_spans、nid/ord検証passは「基礎GOAL到達」と扱う。
- 表・注記・子孫表示は、コードとfixtureで実装済みでも、代表文書の実出力でノード化されていない場合は「実データ到達確認未了」と扱う。
- strict成功は正式昇格可能の十分条件ではなく、GOALギャップ表と人間レビューが必要。
