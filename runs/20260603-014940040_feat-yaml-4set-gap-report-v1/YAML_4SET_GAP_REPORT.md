# 旧zip版4点YAMLと現行4点YAMLのギャップレポート

## 目的

Devin が過去に `qual-law-guideline-main_0210-1000.zip` 内の4点YAMLを前提として DQ チェックリストを実装していたため、現行 `main` の正式版4点YAMLとの差分を整理する。

この文書は、チーフエンジニアが再実装範囲とリスクを判断し、Devin が実装・移行で見るべき差分を把握するためのもの。

## マーク定義

`【UI-MOC相当】` は、このrepoのUIモックと同等の候補表示・チェックシート表示・文脈表示を Devin 側でも実装する場合に読む項目を示す。

Devin 側が現時点で当該UI表示を実装していない場合、`【UI-MOC相当】` の項目は YAML構造の必須ロード要件ではなく、将来同等UIを実装する際の条件付き注意点として扱う。たとえば e-Gov の第一条第一項統合表示は、現時点で Devin 側に同等実装がないなら必須対応に含めない。

## 結論

現行の4点YAMLは、旧zip版の単純な追補ではなく、対象文書数・IR構造・選択対象kind・表示文脈の扱いが広がっている。

- 旧zip版の正式4点セットは **5件**。すべて e-Gov 国内法令。
- 現行正式4点セットは **27件**。
- 旧zip版にあって現行にない doc_id は **0件**。
- 現行で追加された doc_id は **22件**。
- 旧zip版と現行で共通する5件も、4ファイルすべてが変更されている。

したがって Devin 側では、旧実装をそのまま再利用するのではなく、少なくとも次を再確認する必要がある。

- `data/normalized/<doc_id>/` 配下の全 doc_id を動的に読むこと。
- `regdoc_profile.yaml` の `profiles.dq_gmp_checklist` を正として、選択可能kindと表示文脈を決めること。
- `table` / `table_header` / `table_row` を持つIRを扱えること。
- 【UI-MOC相当】e-Gov 国内法令で第一項統合表示を実装する場合は、見た目の変換として扱い、NID・親子関係・共通祖先判定には使わないこと。
- 旧zip版の `meta.yaml` には、未クォートの `%USERPROFILE%...` パスにより YAML として機械読取不能なものが含まれる。現行版はこの問題を解消している。

## 比較条件

| 項目 | 値 |
| --- | --- |
| 旧版入力 | `%USERPROFILE%\Downloads\qual-law-guideline-main_0210-1000.zip` |
| 現行入力 | `data/normalized` |
| 比較対象 | `*.regdoc_ir.yaml`, `*.parser_profile.yaml`, `*.regdoc_profile.yaml`, `*.meta.yaml` の4点セット |
| 比較単位 | doc_id |
| 生データ | `out/20260603-014940040_feat-yaml-4set-gap-report-v1/yaml_4set_gap_summary.json` |
| 比較スクリプト | `runs/20260603-014940040_feat-yaml-4set-gap-report-v1/compare_yaml_4sets.py` |

## 全体サマリ

| 区分 | 件数 |
| --- | ---: |
| 旧zip版の4点セット | 5 |
| 現行の4点セット | 27 |
| 共通doc_id | 5 |
| 現行のみ | 22 |
| 旧zip版のみ | 0 |
| 共通だが変更あり | 5 |
| 完全一致 | 0 |

## 現行で追加された22件

| doc_id | 文書名 | IRノード数 | 最大深さ |
| --- | --- | ---: | ---: |
| `eu_gmp_vol4_chap1_20130131` | EU GMP Vol.4 Chapter 1 Pharmaceutical Quality System | 72 | 4 |
| `eu_gmp_vol4_chap2_20140328` | EU GMP Vol.4 Chapter 2 Personnel | 60 | 4 |
| `eu_gmp_vol4_chap3_20150123` | EU GMP Vol.4 Chapter 3 Premises and Equipment | 62 | 4 |
| `eu_gmp_vol4_chap4_20110101` | EU GMP Vol.4 Chapter 4 Documentation | 130 | 5 |
| `eu_gmp_vol4_chap5_20150123` | EU GMP Vol.4 Chapter 5 Production | 124 | 4 |
| `eu_gmp_vol4_chap6_20140328` | EU GMP Vol.4 Chapter 6 Quality Control | 90 | 4 |
| `eu_gmp_vol4_chap7_20120628` | EU GMP Vol.4 Chapter 7 Outsourced Activities | 26 | 3 |
| `eu_gmp_vol4_chap8_20140813` | EU GMP Vol.4 Chapter 8 Complaints and Product Recall | 49 | 4 |
| `eu_gmp_vol4_chap9_undated` | EU GMP Vol.4 Chapter 9 Self Inspection | 6 | 3 |
| `jp_mhlw_csv_guideline_20101021` | 医薬品・医薬部外品製造販売業者等におけるコンピュータ化システム適正管理ガイドライン | 281 | 5 |
| `jp_niid_pathogen_safety_management_20240401` | 国立感染症研究所病原体等安全管理規程 | 418 | 4 |
| `jp_pmda_api_gmp_guideline_20011102` | 原薬GMPのガイドライン | 496 | 5 |
| `jp_pmda_aseptic_processing_guideline_20110420` | 無菌操作法による無菌医薬品の製造に関する指針 | 1116 | 5 |
| `pics_pe00917_annex11_20230825` | PIC/S GMP Guide Annex 11 Computerised systems | 42 | 3 |
| `pics_pe00917_annex15_20230825` | PIC/S GMP Guide Annex 15 Qualification and validation | 142 | 4 |
| `pics_pe00917_annex1_20230825` | PIC/S GMP Guide Annex 1 Manufacture of sterile medicinal products | 615 | 6 |
| `pics_pe00917_annex2a_20230825` | PIC/S GMP Guide Annex 2A Manufacture of ATMP biological medicinal substances and products | 215 | 6 |
| `pics_pe00917_part1_20230825` | PIC/S GMP Guide Part I Basic Requirements for Medicinal Products | 344 | 4 |
| `pics_pe00917_part2_20230825` | PIC/S GMP Guide Part II Basic Requirements for Active Pharmaceutical Ingredients | 601 | 5 |
| `us_cfr_title21_part11_20251027` | 21 CFR Part 11 - Electronic Records; Electronic Signatures | 85 | 6 |
| `us_cfr_title21_part211_20251027` | 21 CFR Part 211 - CGMP for Finished Pharmaceuticals | 373 | 6 |
| `who_lbm_3rd_2004_9241546506` | WHO Laboratory Biosafety Manual, 3rd ed. | 2023 | 7 |

## 共通5件の変更

旧zip版に存在した5件は現行にも存在するが、4ファイルすべてが更新されている。

| doc_id | 文書名 | 変更ファイル | IRノード数 | 最大深さ |
| --- | --- | --- | ---: | ---: |
| `jp_egov_335AC0000000145_20260501_507AC0000000037` | 医薬品医療機器等法 | IR / parser_profile / regdoc_profile / meta | 2584 -> 2950 | 6 -> 7 |
| `jp_egov_336CO0000000011_20260501_507CO0000000362` | 医薬品医療機器等法施行令 | IR / parser_profile / regdoc_profile / meta | 1063 -> 1475 | 5 -> 7 |
| `jp_egov_336M50000100001_20260501_507M60000100117` | 医薬品医療機器等法施行規則 | IR / parser_profile / regdoc_profile / meta | 6551 -> 7857 | 6 -> 7 |
| `jp_egov_336M50000100002_20260501_507M60000100117` | 薬局等構造設備規則 | IR / parser_profile / regdoc_profile / meta | 476 -> 508 | 7 -> 7 |
| `jp_egov_416M60000100179_20260501_507M60000100117` | GMP省令 | IR / parser_profile / regdoc_profile / meta | 531 -> 567 | 6 -> 7 |

構造差分は、e-Gov XMLの再正規化により `paragraph` が増え、現行IR全体では旧zip版に無かったIR kindが追加された点。

| doc_id | 旧zip版になく現行で追加されたkind |
| --- | --- |
| 医薬品医療機器等法 | `table`, `table_header`, `table_row` |
| 医薬品医療機器等法施行令 | `table`, `table_header`, `table_row` |
| 医薬品医療機器等法施行規則 | `table`, `table_header`, `table_row` |
| 薬局等構造設備規則 | `table`, `table_header`, `table_row` |
| GMP省令 | 新kind追加なし。ただし `paragraph` が 104 -> 140 に増加 |

## YAML構造差分と実装契約

この節は Devin 側の実装漏れを防ぐための契約として読む。現行YAMLをロードする実装は、下記の構造を前提にする。

### 1. 現行IRで必ず扱うkind

現行27セットの `regdoc_ir.yaml` には、次のIR kindが存在する。

| kind | 現行ノード数 | 旧zip版にも存在 | 実装上の扱い |
| --- | ---: | --- | --- |
| `document` | 27 | YES | ルート。選択候補にはしない |
| `part` | 11 | NO | 階層ノードとして保持する。 【UI-MOC相当】文脈表示では祖先になり得る |
| `subpart` | 14 | NO | 階層ノードとして保持する。 【UI-MOC相当】文脈表示では祖先になり得る |
| `chapter` | 177 | YES | 階層ノードとして保持する。 【UI-MOC相当】文脈表示では祖先になり得る |
| `section` | 578 | YES | 階層ノードとして保持する。 【UI-MOC相当】文脈表示では祖先になり得る |
| `article` | 2003 | YES | 論理構造として保持する。 【UI-MOC相当】e-Govでは第一項統合表示の対象になり得る |
| `paragraph` | 6955 | YES | 選択候補になり得る。第一項でもarticleに畳み込まない |
| `item` | 5843 | YES | 選択候補になり得る |
| `subitem` | 1340 | YES | 選択候補になり得る |
| `point` | 143 | YES | 深い箇条書きとして扱う |
| `statement` | 14 | NO | 選択候補になり得る本文単位として扱う |
| `annex` | 789 | YES | 階層ノードとして保持する。 【UI-MOC相当】別表系文脈として表示し得る |
| `appendix` | 345 | YES | 階層ノードとして保持する。 【UI-MOC相当】別表系文脈として表示し得る |
| `table` | 83 | NO | 表の親ノードとして保持する。選択候補にするかはprofileに従う |
| `table_header` | 106 | NO | 表ヘッダとして保持する。 【UI-MOC相当】表行表示時の補助文脈になり得る |
| `table_row` | 2121 | NO | 選択候補になり得る。 【UI-MOC相当】行単独で表示せず、表文脈を付ける |
| `note` | 149 | NO | 注記ノードとして保持する。 【UI-MOC相当】子孫注記または補助文脈として表示し得る |
| `figure` | 15 | NO | 図・画像系ノード。選択候補にするかはprofileに従う |
| `preamble` | 14 | NO | 文書冒頭文脈。選択候補ではなく文脈として扱う |

旧zip版に存在しなかった現行IR kindは、漏れなく次の9種類。

`figure`, `note`, `part`, `preamble`, `statement`, `subpart`, `table`, `table_header`, `table_row`

実装側でこの9種類を未知kindとして捨てると、候補漏れが起きる。 【UI-MOC相当】候補表示・チェックシート表示まで行う場合は、文脈欠落も起きる。少なくともロード、ツリー構築、選択候補判定では全kindを保持する。

### 2. 現行IRノードで出現するキー

現行27セットのIRノードで出現するキーは次の14個。

`children`, `data`, `heading`, `kind`, `kind_raw`, `nid`, `normativity`, `num`, `ord`, `refs`, `role`, `source_spans`, `tags`, `text`

実装上の扱いは次の通り。

| キー | 必須扱い | 用途 |
| --- | --- | --- |
| `nid` | YES | 選択ID、親子関係、対象特定の基準。 【UI-MOC相当】重複省略・表示対象特定にも使う |
| `kind` | YES | 候補種別の基準。 【UI-MOC相当】表示ルール・祖先探索の基準にも使う |
| `children` | YES | ツリー構築。空または欠落も許容する |
| `text` | YES | 本文表示 |
| `heading` | YES | 見出し表示 |
| `num` | YES | 条番号・項番号・号番号などの表示補助 |
| `ord` | YES | 兄弟順序の保持 |
| `kind_raw` | SHOULD | 原文由来の種別確認・デバッグ |
| `role` | SHOULD | table/header/note等の補助情報。 【UI-MOC相当】表示補助にも使い得る |
| `data` | SHOULD | 表・図などkind固有データの将来拡張用 |
| `normativity` | SHOULD | 規範性のフィルタ。 【UI-MOC相当】表示補助にも使い得る |
| `refs` | SHOULD | 参照情報 |
| `source_spans` | SHOULD | 原文位置・監査用 |
| `tags` | SHOULD | 将来の絞り込み・分類用 |

`nid`, `kind`, `children`, `text`, `heading`, `num`, `ord` を前提にしない実装は、現行YAMLの候補生成を安定して扱えない。 【UI-MOC相当】表示再現性にも影響する。

### 3. `regdoc_profile.yaml` の必須パス

DQチェックリスト実装は、IRだけで候補生成を決めてはいけない。 【UI-MOC相当】候補表示・チェックシート表示まで行う場合も、IRだけで表示を決めてはいけない。現行 `regdoc_profile.yaml` では、次のパスを読む。

| パス | 実装上の意味 |
| --- | --- |
| `$.schema` | profileスキーマ識別 |
| `$.doc_id` | 対象doc_id |
| `$.profiles.dq_gmp_checklist` | DQチェックリスト用profile |
| `$.profiles.dq_gmp_checklist.candidate_visibility.allow_rules[]` | 候補許可ルール。空でも処理できること |
| `$.profiles.dq_gmp_checklist.candidate_visibility.deny_rules[]` | 候補除外ルール。`nid_prefix` と `reason` を持ち得る |
| `$.profiles.dq_gmp_checklist.selectable_kinds[]` | 選択可能kindの正本 |
| `$.profiles.dq_gmp_checklist.grouping_policy[]` | 候補一覧上のグルーピング |
| `$.profiles.dq_gmp_checklist.grouping_policy[].when_kind` | グルーピング対象kind |
| `$.profiles.dq_gmp_checklist.grouping_policy[].group_under_kind` | どの祖先kindの下にまとめるか |
| `$.profiles.dq_gmp_checklist.context_display_policy[]` | 【UI-MOC相当】チェックシート側の文脈表示ルール |
| `$.profiles.dq_gmp_checklist.context_display_policy[].when_kind` | 【UI-MOC相当】表示ルール対象kind |
| `$.profiles.dq_gmp_checklist.context_display_policy[].include_ancestors_until_kind` | 【UI-MOC相当】祖先文脈の上限kind |
| `$.profiles.dq_gmp_checklist.context_display_policy[].include_headings` | 【UI-MOC相当】祖先見出しを出すか |
| `$.profiles.dq_gmp_checklist.context_display_policy[].include_chapeau_text` | 【UI-MOC相当】祖先本文を出すか |
| `$.profiles.dq_gmp_checklist.context_display_policy[].include_descendants` | 【UI-MOC相当】子孫文脈を追加するか |
| `$.profiles.dq_gmp_checklist.context_display_policy[].include_descendants_of` | 【UI-MOC相当】selected / ancestors のどちらの子孫を見るか |
| `$.profiles.dq_gmp_checklist.context_display_policy[].include_descendants_kinds[]` | 【UI-MOC相当】子孫として追加するkind。例: `note` |
| `$.profiles.dq_gmp_checklist.context_display_policy[].include_descendants_max_depth` | 【UI-MOC相当】子孫追加の最大深さ |
| `$.profiles.dq_gmp_checklist.render_templates` | 【UI-MOC相当】文書別レンダリング拡張。空でも存在し得る |

【UI-MOC相当】実装で `selectable_kinds` だけを読んで表示文脈を固定化すると、表行、注記、第一項統合、祖先省略で漏れが出る。

### 4. 4ファイル別の移行差分

| ファイル | 旧zip版の前提 | 現行の前提 | 実装誘導 |
| --- | --- | --- | --- |
| `*.regdoc_ir.yaml` | e-Gov 5件中心。kind集合は10種類 | 27件。kind集合は19種類 | kind固定分岐を廃止し、全kindを保持したうえでprofileで選択可否を決める |
| `*.regdoc_profile.yaml` | DQ profileは存在するが対象文書が少ない | `profiles.dq_gmp_checklist` が現行の候補仕様。 【UI-MOC相当】表示仕様も含む | 候補生成、グルーピングをprofile駆動にする。 【UI-MOC相当】文脈表示もprofile駆動にする |
| `*.parser_profile.yaml` | e-Gov中心 | e-Gov、EU GMP、PIC/S、CFR、WHO、日本ガイドラインで入力形式・構造前提が異なる | 実装ではparser_profileを変換実装の参考情報として扱い、候補・表示仕様には使わない |
| `*.meta.yaml` | 旧zip版の5件で標準YAMLパース不能箇所あり | 現行27件は標準YAMLとしてパース可能 | 旧metaを移行入力にしない。現行metaを文書名・出典の正本にする。 【UI-MOC相当】画面表示にも使い得る |

### 5. 実装で禁止するショートカット

次の実装は、現行YAMLでは候補漏れの原因になる。 `【UI-MOC相当】` 付きの項目は、UIモックと同等の候補表示・チェックシート表示を実装する場合に表示崩れの原因になる。

- doc_idを5件固定にする。
- e-Govだけを前提に階層を解釈する。
- `article`, `paragraph`, `item`, `subitem` 以外のkindを捨てる。
- `table_row` を候補対象外に固定する。
- `regdoc_profile.yaml` を読まず、IR kindだけで選択候補を決める。
- 旧zip版の `meta.yaml` を現行実装の入力として読む。
- 【UI-MOC相当】`note` を常に非表示にする。
- 【UI-MOC相当】第一項統合表示を、論理構造、NID、親子関係、祖先省略判定に使う。

## Devin向け実装メモ

### 1. doc_idを固定列挙しない

旧実装が5件固定、または e-Gov 前提で作られている場合、現行27件に対応できない。

実装側は `data/normalized/*/` を走査し、同一 doc_id の4ファイルが揃っているものをロード対象にする。

### 2. 選択ルールは `regdoc_profile.yaml` を正とする

現行プロファイルは `profiles.dq_gmp_checklist` 配下に、少なくとも次を持つ。

- `selectable_kinds`
- `grouping_policy`
- `context_display_policy`
- `render_templates`

DQチェックリストでは、IRの全ノードをそのまま選択対象にするのではなく、対象文書ごとの `selectable_kinds` と `candidate_visibility` を先に適用する。

【UI-MOC相当】候補表示・チェックシート表示までUIモックと同等に実装する場合は、同じprofile内の `grouping_policy` と `context_display_policy` も表示仕様として扱う。

### 3. `table_row` を選択対象として扱う

現行では表が `table` / `table_header` / `table_row` としてIRに出る。特に e-Gov 再正規化データとPIC/S・CFR系で重要。

`table_row` は、本文ノードと同じようにチェック項目候補になる。

【UI-MOC相当】表行をチェックシート上に表示する場合は、表の祖先文脈を失うと意味が崩れるため、`context_display_policy` に従って `table` などの祖先を表示する。

### 4. 【UI-MOC相当】第一項統合表示は国内e-Govだけの見た目変換として扱う

この項目は、Devin 側でUIモックと同等の e-Gov 第一項統合表示を実装する場合だけ読む。

日本国内法令では、第一条第一項相当の表示を `第一条　<第一項本文>` のように統合表示できる。

ただしこれは表示上の例外であり、次には使わない。

- NID生成
- 親子関係
- 兄弟判定
- 共通祖先判定
- 重複省略判定

内部的には `article -> paragraph -> item/subitem...` の論理構造を維持し、最後の描画段でだけ統合する。

### 5. 旧zip版の `meta.yaml` は信頼できる入力として扱わない

旧zip版の共通5件では、`meta.yaml` に未クォートの `%USERPROFILE%...` パスが含まれ、標準YAMLパーサで読めないものがある。

現行版を正とし、旧zip版の `meta.yaml` は移行比較用の参考に留める。

## チーフエンジニア向け判断ポイント

今回の再実装は「法令追加」だけではなく、データ構造の正式化を伴う。

影響範囲は次の順で見るのがよい。

1. データローダー: 5件固定から27件動的ロードへ変える。
2. 候補生成: `regdoc_profile.yaml` の `profiles.dq_gmp_checklist` を仕様として扱う。
3. 【UI-MOC相当】表示: 祖先文脈、子孫注記、共通祖先省略、兄弟のみ省略、第一項統合表示を分ける。
4. テスト: e-Govだけでなく、EU GMP、PIC/S、CFR、WHO、日本ガイドライン文書を代表ケースに入れる。

特に、旧実装が「条文っぽい階層」だけを前提にしている場合、現行の `table_row`、CFRの深い階層、PIC/S Annex 1の深さ6、WHO文書の大規模ノード数により候補漏れが起きる可能性がある。 【UI-MOC相当】候補表示・チェックシート表示まで行う場合は、表示崩れも起きる可能性がある。

## 推奨テスト観点

| 観点 | 代表doc_id | 確認内容 |
| --- | --- | --- |
| 【UI-MOC相当】e-Gov 第一項統合 | `jp_egov_336M50000100002_20260501_507M60000100117` | 統合表示ON/OFFで見た目だけが変わり、選択NIDと親子関係が変わらない |
| e-Gov 表系ノード | `jp_egov_336CO0000000011_20260501_507CO0000000362` | `table_row` が候補になる。 【UI-MOC相当】表の文脈が表示される |
| EU GMP 通常章 | `eu_gmp_vol4_chap4_20110101` | paragraph/item/subitem が候補・階層として扱える。 【UI-MOC相当】祖先文脈が自然に出る |
| PIC/S 深い階層 | `pics_pe00917_annex1_20230825` | 最大深さ6でも候補生成が崩れない。 【UI-MOC相当】文脈表示も崩れない |
| CFR 深い階層 | `us_cfr_title21_part211_20251027` | Part/Subpart/Section/Paragraph系の階層で候補生成できる。 【UI-MOC相当】祖先文脈が出る |
| 大規模日本語指針 | `jp_pmda_aseptic_processing_guideline_20110420` | 1000超ノードでも検索・候補生成が実用速度で動く |
| WHO大規模文書 | `who_lbm_3rd_2004_9241546506` | 2000超ノードでもロード・検索が破綻しない。 【UI-MOC相当】描画も破綻しない |

## 補足

このレポートはコード挙動ではなく、旧zip版と現行正式YAMLの差分をもとに作成した。実装側の正解は現行 `data/normalized` の4点セット、特に `regdoc_profile.yaml` と `regdoc_ir.yaml` である。
