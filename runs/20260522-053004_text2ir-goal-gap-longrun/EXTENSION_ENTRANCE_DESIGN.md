# EXTENSION_ENTRANCE_DESIGN

## 結論

以下は共通 `qai_text2ir` parserへ無理に押し込まず、拡張入口・特別部品として扱う。

- PIC/S PE 009-17 Annexes全体 refined
- CFR Part 211 / Part 11 のeCFR XML入口
- 複雑表・PDF抽出崩れ表

共通parserに入れるのは、dispatch/fallback、profile provenance、manifest記録、GOAL検証、表・注記の共通表現など、複数文書に効く抽象機能に限定する。

## PIC/S PE 009-17 Annexes全体 refined

### 現状

- `src/qai_text2ir/profiles/pics_annexes_default_v3.yaml` は `pics_pe00917_common_v1` をextendsする。
- `postprocess.refine_subtrees` により、Annex単位で子profileへdispatchする。
- Annex 1 / 2A / 11 / 15 は専用profileへ、それ以外は `pics_annex_generic_default_v1` へfallbackする。
- manifestには `refine.applied` として適用profileが記録される。

### 設計判断

これは単純な1文書1profileではなく、親入口と子profile群からなる複合入口である。共通parserの機能としては以下に留める。

- subtree境界の抽出
- dispatch/fallback
- refine provenanceタグ
- manifestへの適用サマリ記録
- GOALチェックとaudit reportでのrefine件数集計

Annexごとのmarker、見出し継続、階層差分は子profileへ閉じ込める。

### 追加で補強すべきテスト

- dispatch対象Annexが専用profileへ入ること
- fallback対象Annexがgeneric profileへ入ること
- refine後もsource_spansが元文書行を指すこと
- manifestの `refine.applied` がAnnex単位で説明可能であること

## CFR Part 211 / Part 11

### 判断

現行repo内に正式代表入力がないため、今回のPhaseでは再生成対象にしない。Part 211は特に、プレーンテキスト共通parserだけで解くより、eCFR XML等の安定構造入力を優先する。

### text2ir汎用parserだけで解くべきでない理由

- CFRは構造入力が利用可能であり、PDF/TXT復元に依存する必要が薄い。
- section、paragraph、item、subitemの階層が法令構造として安定している。
- プレーンテキストでは表、注記、authority、source note、appendix等が崩れる可能性がある。
- 監査説明では、eCFR由来の構造・URL・版情報を明示した方が追跡性が高い。

### eCFR XML入口の利点

- section単位の構造化が安定する。
- source URL、version、identifierをmetaへ入れやすい。
- `source_spans` 相当をXML element pathまたはsection locatorで表現できる。
- 将来の差分更新で、section id単位の比較がしやすい。

### 入力配置案

```text
data/xml/us/ecfr/title-21/part-11/<retrieved_at>/...
data/xml/us/ecfr/title-21/part-211/<retrieved_at>/...
```

または、human-readable変換後も保持する場合:

```text
data/human-readable/us_cfr/title21/part11.txt
data/human-readable/us_cfr/title21/part211.txt
```

正式入力としてはXMLを正本、TXTを補助生成物とする方が望ましい。

### doc_id案

```text
us_ecfr_title21_part11_<yyyymmdd>
us_ecfr_title21_part211_<yyyymmdd>
```

### profile方針

- parser入口は `qai_ecfr2ir` ないし `qai_text2ir` の拡張入口として分ける。
- 出力IRとregdoc_profileは既存GOALに合わせる。
- `dq_gmp_checklist.selectable_kinds` は `paragraph`, `item`, `subitem`, `table_row` を基本とする。
- Part 11はデータ完全性・電子記録観点で優先度高。
- Part 211はGMP本体として重要だが、構造入口設計を先に固める。

## 複雑表・PDF崩れ表

### 3段階の扱い

| 入力形状 | 扱い | 実装境界 |
|---|---|---|
| Markdown table | 共通parserで `table/table_header/table_row/note` 化 | `qai_text2ir` 共通 |
| 単純な固定幅表 | profile明示有効化時のみ `preformatted/possible_table` または限定構造化 | `qai_text2ir` 共通 + profile |
| 複雑表・複数カラム崩れ | 前処理または専用部品へ移管 | 拡張入口 |

### confidence方針

- 悪い `table_row` 化は、構造化しないより危険。
- 低confidence時は `possible_plaintext_table_not_structured` として保持し、人間レビューへ回す。
- 正式化前に、表タイトル、ヘッダ、行、注記、source_spansの関係をサンプル比較で確認する。

## Phase 5結論

次のPhase 6では、代表9文書を再生成し、GOALチェックとaudit reportを実行する。PIC/S Annexes全体 refinedは複合入口として評価し、CFR Part 11/211は正式入力なしとして設計対象に留める。
