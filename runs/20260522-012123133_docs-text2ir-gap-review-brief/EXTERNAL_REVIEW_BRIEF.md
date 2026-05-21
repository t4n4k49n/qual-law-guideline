# text2ir正規化ギャップ評価 外部レビュー用ブリーフ

## 背景

このリポジトリでは、国内外の製薬クオリフィケーション関連の法令・ガイドラインを共通IRとして正規化し、GMPチェックシート等で参照可能にすることを目指している。

現時点で正式版として `data/normalized/` に置かれている主対象は、e-Gov XML由来の以下5文書である。

- 医薬品、医療機器等の品質、有効性及び安全性の確保等に関する法律
- 同施行令
- 同施行規則
- 薬局等構造設備規則
- 医薬品及び医薬部外品の製造管理及び品質管理の基準に関する省令（GMP省令）

これらは `qai_xml2ir`、すなわち e-Gov日本法令XML向けパーサーで処理されてきた。一方で、CFR、EU GMP、WHO、PIC/S などの文書は、PDF由来テキストやプレーンテキストを `qai_text2ir` で処理している。

今回の論点は、5文書以外の text2ir 系文書を、どのように xml2ir の最終正規化レベルへ近づけるかである。

## 目指すGOAL

GOALは、`qai_xml2ir` の最終正規化レベルと同等の下流利用品質である。

ただし、text2ir は e-Gov XMLのような構造化入力ではなく、PDF/TXT由来の雑多な文書を扱う。そのため「xml2irと完全同型の構造」を機械的に求めるのではなく、「同じ下流利用品質を満たすこと」をGOALとするのが現実的である。

GOALの候補観点:

- IR schema が現行世代に揃っていること
- 4ファイル構成が揃うこと
  - `regdoc_ir.yaml`
  - `parser_profile.yaml`
  - `regdoc_profile.yaml`
  - `meta.yaml`
- `nid` が一意で、構造上の意味と対応していること
- `ord` が一意かつ安定し、文書順序を表すこと
- 本文単位の階層が崩れていないこと
  - e-Gov法令なら `article -> paragraph -> item`
  - ガイドラインなら `chapter/section/annex -> paragraph/item/subitem` 等の文書に応じた対応関係
- `source_spans` や `meta` により、入力元と出力ノードの関係をレビュー可能であること
- `regdoc_profile.dq_gmp_checklist` に現行標準項目が含まれること
- 正規化RUNとして `runs/<run_id>/promotion_candidate/` に置いてレビューできること
- 生成・検証・レビュー・昇格の手順が再現可能であること

## 現時点の事実

### パーサー本体

実装上のパーサー本体は大きく2種類ある。

1. `qai_xml2ir`
   - e-Gov日本法令XML用
   - 主な実装: `src/qai_xml2ir/egov_parser.py`
   - 現行の正式版5文書はこちらで処理

2. `qai_text2ir`
   - TXT化したPDF/HTML/プレーンテキスト用の汎用テキストパーサー
   - 主な実装: `src/qai_text2ir/text_parser.py`
   - 文書ごとの違いは `src/qai_text2ir/profiles/*.yaml` で吸収

### text2ir profile

`src/qai_text2ir/profiles/` には24個のprofileがある。

主な系統:

- US CFR
  - `us_cfr_default_v1`
  - `us_cfr_default_v2`
- EU GMP
  - `eu_gmp_chap1_default_v1`
  - `eu_gmp_chap1_default_v2`
- WHO LBM
  - `who_lbm_3rd_default_v1` から `v4`
- PIC/S PE 009-17
  - 共通: `pics_pe00917_common_v1`
  - Part I: `pics_part1_default_v1` から `v3`
  - Part II: `pics_part2_default_v1`
  - Annex単体: Annex 1 / 2A / 11 / 15 など
  - Annexes全体: `pics_annexes_default_v1` から `v3`
- テスト用
  - `markdown_table_test_v1`

重要なのは、profileが24個あるだけで、パーサー本体が24種類あるわけではない点である。多くは同じ text parser に対する文書別設定である。

### 既存の到達点

過去RUNの記録から、以下は `--qualitycheck --strict` を通した4 YAML生成まで到達している。

- EU GMP Vol.4 Chapter 1
- WHO Laboratory Biosafety Manual, 3rd edition
- PIC/S PE 009-17 Part I
- PIC/S PE 009-17 Part II
- PIC/S PE 009-17 Annex 1
- PIC/S PE 009-17 Annex 2A
- PIC/S PE 009-17 Annex 11
- PIC/S PE 009-17 Annex 15
- PIC/S PE 009-17 Annexes全体 refined

CFRについては、21 CFR Part 11は品質改善RUNがあり、21 CFR Part 211はテキスト処理履歴とeCFR XML取得履歴がある。ただし、正式正規化候補としては他文書より整理が浅い可能性がある。

### 注意すべき差分

既存の text2ir 成果物には `qai.regdoc_ir.v3` 世代のものが多い。一方で、e-Gov XML由来の現行正規化は `qai.regdoc_ir.v4` 世代で運用されている。

したがって、過去RUNで strict 成功していることは有力な事実だが、そのまま正式昇格可能という意味ではない。現行GOALに照らして再生成・再評価が必要である。

## 推定・仮説

### 推定1: まず必要なのは実装ではなくギャップ評価

いきなり profile や text2ir を修正するより、まず GOALチェックリストを作り、各最終profileで再生成してギャップ表を作るべきである。

理由:

- 既存RUNの成功条件は文書ごとに異なる
- v3/v4世代差がある
- text2ir本体に入れるべき共通機能と、profileだけで済む問題を分離する必要がある
- 文書固有対応を共通パーサーへ混ぜると、長期的な保守性が落ちる

### 推定2: text2ir本体に入れるべきなのは抽象的な共通機能だけ

text2ir は雑多な文書を扱う共通パーサーである。したがって、text2ir本体へ文書名ベタ書きの知識を入れるべきではない。

共通機能として入れる候補:

- schema v4出力対応
- `regdoc_profile` 標準項目の自動付与
- source provenance / source_spans の安定化
- manifest出力の標準化
- qualitycheckの標準化
- heading continuation、TOC skip、running header drop 等の抽象化
- table / note / preformatted block の共通表現
- marker曖昧性解決の汎用ルール
- profile inheritance / provenance の整理

文書固有の判断は profile 側、または拡張部品側に逃がすべきである。

### 推定3: 一部文書には拡張パーサーが必要かもしれない

PIC/S Annexes全体のように、親profileで全体を切り、各Annexを子profileで refine する方式は、すでに拡張部品的な性格を持っている。

また、CFR Part 211については、eCFR XMLを取得した履歴がある。もしXML入力が安定して使えるなら、プレーンテキストを text2ir で頑張るより、CFR XML専用の入口を作るほうが良い可能性がある。

この場合、`text2ir` に無理に吸収するのではなく、`cfrxml2ir` 的な別パーサー、または `text2ir` とは別の入力アダプターとして設計する選択肢がある。

## ギャップ分類の考え方

各文書のギャップは、少なくとも以下3分類に分ける。

### A. profile変更で済む課題

- ヘッダ/フッタ/ページ番号除去
- TOCスキップ
- marker regex調整
- running header除去
- heading continuation
- Annex/Chapter/Sectionの文書固有構造
- 特定Annex向けの refine dispatch

### B. text2ir共通更改が必要な課題

- schema v4相当の出力
- 4ファイル標準出力の整合
- `regdoc_profile` 標準項目の自動付与
- source provenance / source_spans の整備
- `ord` / `nid` の安定性改善
- qualitycheck項目の標準化
- table / note / preformatted block の共通表現
- marker曖昧性解決の汎用化

### C. 拡張パーサーまたは特別部品が必要な課題

- 複数カラムPDF由来の構造崩れ
- 巨大表や図表ブロック
- 文書内で構造文法が大きく切り替わるケース
- 親文書を分割し、部分ごとに別profileで再parseするケース
- CFR XMLなど、そもそもtextより構造化入力を使うべきケース

## ピックアップすべき文書リスト

外部レビューでは、全件を一度に見るより、性質が異なる文書を代表として選ぶのがよい。

### 1. EU GMP Vol.4 Chapter 1

- 入力: `data/human-readable/eu_gmp/vol4/chap1_2013-01_en.txt`
- 最終profile候補: `eu_gmp_chap1_default_v2`
- 代表RUN: `runs/20260217-025810168_feat-eu-gmp-chap1-v2-strict-zero-rerun/RUN.md`
- 事実:
  - strict warning 0の記録あり
  - 文書サイズが比較的小さく、ギャップ評価の試金石に向く
- 推定:
  - profile側の成熟度は高い
  - 主要ギャップは text2ir共通出力仕様と正規化RUN運用側に寄る可能性が高い

### 2. WHO Laboratory Biosafety Manual, 3rd edition

- 入力: `data/human-readable/who/WHO_LBM_3rd.txt`
- 最終profile候補: `who_lbm_3rd_default_v4`
- 代表RUN: `runs/20260218-011744140_feat-who-lbm-v4-marker-ref-join/RUN.md`
- 事実:
  - strict warning 0の記録あり
  - chapter heading continuation、Annex参照誤検出対策が入っている
- 推定:
  - 大型PDF由来文書の代表として有用
  - heading continuation、TOC/Annex処理、本文参照保持の共通化観点を検証できる

### 3. PIC/S PE 009-17 Part I

- 入力: `data/human-readable/pics/pe009-17_part1_2023-08-25_en.txt`
- 最終profile候補: `pics_part1_default_v3`
- 代表RUN: `runs/20260218-024512389_feat-pics-part1-full-v3-strict/RUN.md`
- 事実:
  - strict warning 0の記録あり
  - Chapter 1から9までを単一文書として処理
- 推定:
  - PIC/S本流文書の代表として優先度が高い
  - TOC/ヘッダ/フッタ除去、章構造、bullet処理の評価に向く

### 4. PIC/S PE 009-17 Part II

- 入力: `data/human-readable/pics/pe009-17_part2_2023-08-25_en.txt`
- 最終profile候補: `pics_part2_default_v1`
- 代表RUN: `runs/20260218-033318157_feat-pics-part2-v1-strict/RUN.md`
- 事実:
  - strict warning 0の記録あり
  - API GMP側の節構造を保持
- 推定:
  - Part Iとは違う番号体系・章立てを持つため、汎用性検証に向く

### 5. PIC/S PE 009-17 Annex 1

- 入力: `data/human-readable/pics/pe009-17_annex1_2023-08-25_en.txt`
- 最終profile候補: `pics_annex1_default_v2`
- 代表RUN: `runs/20260218-055612198_feat-pics-annex1-v2-strict/RUN.md`
- 事実:
  - strict warning 0の記録あり
  - Annex 1は構造と本文量が大きい
  - Glossaryが無番号見出しのため本文扱いになる残課題が記録されている
- 推定:
  - Annex系の難しさを代表する文書
  - profileで解ける範囲と、追加構造種別が必要な範囲の見極めに向く

### 6. PIC/S PE 009-17 Annex 2A

- 入力: `data/human-readable/pics/pe009-17_annex2a_2023-08-25_en.txt`
- 最終profile候補: `pics_annex2a_default_v1`
- 代表RUN: `runs/20260218-101934654_feat-pics-annex2a-v1-strict/RUN.md`
- 事実:
  - strict warning 0の記録あり
  - Figure/Table、Part A/B、B3.3などの特殊構造を扱っている
- 推定:
  - preformatted block、図表、複合番号体系の検証に向く
  - 拡張部品が必要かどうかを判断しやすい

### 7. PIC/S PE 009-17 Annex 11

- 入力: `data/human-readable/pics/pe009-17_annex11_2023-08-25_en.txt`
- 最終profile候補: `pics_annex11_default_v1`
- 代表RUN: `runs/20260218-041935361_feat-pics-annex11-v1-strict/RUN.md`
- 事実:
  - strict warning 0の記録あり
  - Computerised systemsとしてチェックシート候補に関係が深い可能性が高い
- 推定:
  - DQ/GMPチェックシート用途に近く、優先評価対象にしやすい

### 8. PIC/S PE 009-17 Annex 15

- 入力: `data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt`
- 最終profile候補: `pics_annex15_default_v1`
- 代表RUN: `runs/20260218-052028430_feat-pics-annex15-v1-strict/RUN.md`
- 事実:
  - strict warning 0の記録あり
  - Qualification and validationそのものを扱う
- 推定:
  - 本プロジェクトのクオリフィケーション文脈に最も近い重要候補

### 9. PIC/S PE 009-17 Annexes全体 refined

- 入力: `data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt`
- 最終profile候補: `pics_annexes_default_v3`
- 代表RUN: `runs/20260218-172825019_feat-pics-trace-provenance-v1/RUN.md`
- 事実:
  - strict warning 0の記録あり
  - subtree refine、dispatch、fallback、provenance記録がある
- 推定:
  - text2ir共通機能と拡張部品の境界を検証する本命
  - ただし最初に着手するには複雑すぎる可能性がある

### 10. 21 CFR Part 11

- 代表RUN: `runs/20260211-190200082_feat-cfr-v2-quality-fixes/RUN.md`
- 最終profile候補: `us_cfr_default_v2`
- 事実:
  - Subpart構造化、kind_raw、source_spans重複、heading/chapeau分離などの品質修正履歴あり
  - 4 YAML生成履歴あり
- 推定:
  - CFR text2irの代表として評価対象にできる
  - ただし正式化の優先度はPIC/SやEU/WHOより後でもよい

### 11. 21 CFR Part 211

- 関連RUN:
  - `runs/20260212-112252299_feat-ecfr-part211-ps1/RUN.md`
  - `runs/20260212-051108599_feat-text-unwrap-hyphen-normalization/RUN.md`
- 事実:
  - Part 211のtext2ir処理履歴がある
  - eCFR XML取得履歴がある
- 推定:
  - text2irで進めるべきか、CFR XML専用入口を検討すべきかの分岐点
  - 外部レビューでは設計論点として扱う価値が高い

## 推奨する進め方

### Step 1: GOALチェックリストを作る

まず、xml2ir最終正規化レベルを基準にしたチェックリストを作る。

観点例:

- schema世代
- 4ファイル構成
- `nid`一意性
- `ord`一意性・順序性
- 文書種別ごとの階層妥当性
- `source_spans`
- `meta.generation`
- `regdoc_profile.dq_gmp_checklist`
- `candidate_visibility`
- manifest / provenance
- qualitycheck結果
- 深い階層サンプルのレビュー可能性

### Step 2: 各最終profileで再生成する

まずは代表文書を選び、現行mainの text2ir で再生成する。

最初の候補:

1. EU GMP Vol.4 Chapter 1
2. WHO LBM 3rd
3. PIC/S Part I
4. PIC/S Part II
5. PIC/S Annex 15
6. PIC/S Annexes全体 refined

### Step 3: ギャップ表を作る

各文書について、GOALとの差分を以下に分類する。

- profile変更で済む
- text2ir共通更改が必要
- 拡張パーサー/特別部品が必要
- 判断保留

### Step 4: 実装順序を決める

実装は、文書個別の修正ではなく、複数文書に効く共通更改を優先する。

ただし、PIC/S Annex 15やAnnex 11のように業務上重要な文書は、多少個別profile寄りでも先に正式化候補へ進める判断はあり得る。

## 外部レビューで聞きたいこと

- xml2ir最終正規化レベルを text2ir のGOALに置く考え方は妥当か
- text由来文書に対して、xml2irと同じ構造品質をどこまで求めるべきか
- profileで吸収すべき範囲と、text2ir本体に入れるべき範囲の線引きは妥当か
- PIC/S Annexesの subtree refine / dispatch / fallback は、共通機能として扱うべきか、拡張部品として扱うべきか
- CFR Part 211は text2ir継続か、eCFR XML専用パーサーを検討すべきか
- 正式正規化に入る最初の文書として、EU GMP / WHO / PIC/S Part I / PIC/S Annex 15 のどれが適切か
