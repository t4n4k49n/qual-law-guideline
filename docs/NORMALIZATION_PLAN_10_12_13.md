# 10/12/13 正規化方針検討

## 前提

対象は次の3分類とする。CFR Part 11 / Part 211（11）は、eCFR XML入口を優先する別課題として一旦除外する。

- 10: EU GMP
- 12: PIC/S
- 13: WHO LBM 3rd

ここでの検討は通常の方針検討RUNであり、正式な正規化RUNではない。`data/normalized/` への昇格は、別途 `docs/NORMALIZED_RUN_PLAYBOOK.md` に従って行う。

## 結論

10/12/13には共通化できる部分がある。ただし、最後まで同一処理で押し切るべきではない。

共通化すべき範囲:

- 4ファイルbundle生成。
- manifest / profile provenance / git commit / input checksumの記録。
- `qualitycheck --strict`。
- `goal_check`。
- `audit_report`。
- `SAMPLE_COMPARISON` による人間レビュー。
- `promotion_candidate/` への正本配置。
- `data/normalized/` への昇格は親PR承認後の子PRで行う。

文書別に分ける範囲:

- 入力粒度。EU GMPは章単位、PIC/SはPart/Annex単位、WHOは対象章範囲を決める。
- profile。EU/PIC/S/WHOで既存profileが別。
- 複合入口。PIC/S Annexes refinedは正式昇格の最初の候補にしない。
- 表・注記・possible_tableの扱い。
- selectable粒度。WHOはitem粒度の人間レビューが残る。

## 現行main再生成後の判断

`runs/20260527-105034029_docs-readiness-10-12-13-rerun/` で Phase A/B を実施した。詳細なreadiness表は `runs/20260527-105034029_docs-readiness-10-12-13-rerun/READINESS_10_12_13.md` を正とする。

再生成結果:

- 単体8文書は `qualitycheck --strict`、GOAL、promotion GOAL がすべてpass。
- 旧成果で出ていた `meta_family_missing` は、現行CLIで `--family` を付けることで解消した。
- 実文書本体でも table/note が出るようになっており、PIC/S Annex 1、Annex 2A、Part II、WHO LBM 3rd は表・注記レビューを正式候補化前に挟む。
- PIC/S Annexes refined は `page-number-only line remains` により strict fail したため、正式化初手から外す。

再生成後の優先順位:

1. EU GMP Chapter 1: 最初の正規化RUN候補。warningなし、表・注記なし、レビュー負荷が小さい。
2. PIC/S Annex 11: PIC/S単体Annexの最初の候補。warningなし、表・注記なし。
3. PIC/S Annex 1: 技術的にはready。表・注記のSAMPLE_COMPARISON後に候補化する。
4. WHO LBM 3rd: 技術的にはready。対象章範囲とcandidate visibilityの判断を先に固定する。
5. PIC/S Annex 2A / Part II / Part I / Annex 15: ready later。Annex単体の運用型が固まってから順次扱う。
6. PIC/S Annexes refined: not ready。横断検索・参考候補として維持し、単体Annex正式化後に修正・再評価する。

## 過去記録から使うべき知見

### 使う

- `runs/20260522-053004_text2ir-goal-gap-longrun/GOAL_CHECK_RESULTS.md`
  - 代表9文書はGOAL_CHECK pass。
  - ただし旧成果ではGOAL warningとして `meta_family_missing` が出ていた。
  - 現行CLIで再生成した結果、`--family` 指定によりこのwarningは解消した。
- `runs/20260522-053004_text2ir-goal-gap-longrun/TEXT2IR_AUDIT_REPORT.md`
  - 9文書のschema、4files、manifest、strict、source coverage、node数を横断集計済み。
  - 正規化RUN候補にも同じ監査を流用する。
- `runs/20260522-053004_text2ir-goal-gap-longrun/TEXT2IR_GAP_RESOLUTION_MATRIX.md`
  - EU/PIC/S/WHOで解消済み・保留中の課題が整理済み。
  - 表・注記の実文書全体での構造化状況は再確認済み。正式候補化では文書別にSAMPLE_COMPARISONで確認する。
- `runs/20260522-053004_text2ir-goal-gap-longrun/EXTENSION_ENTRANCE_DESIGN.md`
  - PIC/S Annexes refinedは複合入口として扱い、共通parserへ押し込まない。
  - CFR XML入口は11番用の別課題として分ける。
- `docs/TEXT2IR_COMPOSITE_ENTRY_DESIGN.md`
  - PIC/S Annexes refinedは正式昇格の最初の候補にせず、Annex単体を優先する。
- `local_notes/KNOWLEDGE.md`
  - 10/12/13固有の技術知見は薄い。
  - 正規化RUNの昇格元を `runs/<run_id>/promotion_candidate/` に固定する運用知見は使う。

### 今回は使わない

- CFR XML adapter設計。
  - 11番専用の方針であり、10/12/13のTXT系正式化とは切り離す。

## 10 EU GMP

### 現状

- `data/human-readable/eu_gmp/vol4/` にPDF/TXT sourceがある。
- Chapter 1は `eu_gmp_chap1_default_v2` でGOAL pass済み。
- 一覧上はChapter 1から9、Part II相当が対象。
- EU GMP用XML入力は現repoでは確認できない。

### 課題

- Chapter 1以外の章を同じ品質で再生成・検証する。
- Chapter単位で正式化するか、Part I bundleとして正式化するかを決める。
- Part IIはPart I章群と別docとして扱う。
- 表・注記・possible_tableの有無を章ごとに監査する。
- Chapter 1以外でも現行CLIの `--family EU_GMP` を付け、meta familyを明示する。

### 方針

EU GMPはTXTベースで進める。XML側へ切り替える材料は現時点でない。

推奨順:

1. Chapter 1を正規化RUNでpromotion candidate化する。
2. Chapter 2から9を同一手順で再生成し、章単位のreadinessを出す。
3. Part IIを別docとして再生成する。
4. Part I全体bundleが必要かを最後に判断する。

Chapter 1は現行main再生成でstrict / GOAL / promotion GOALがpassし、warningなし、table/noteなし。最初の正規化RUNに進める。

## 12 PIC/S

### 現状

- `data/human-readable/pics/` にPart I、Part II、Annex 1、Annex 11、Annex 2A、Annexes全体のTXT/PDF sourceがある。
- 代表9文書GOAL_CHECKで、Part I、Part II、Annex 1、Annex 11、Annex 15、Annex 2A、Annexes refinedがpass済み。
- `pics_annexes_default_v3` は親profileと子profile群を使う複合入口。
- PIC/S XML入力は現repoでは確認できない。

### 課題

- 正式化対象を、一覧にあるPart I / Part II / Annex 1 / Annex 11 / Annex 2Aに合わせて再確認する。
- Annexes refinedは便利だが、正式昇格の最初の候補にしない。
- Annex単体でpromotion candidateを作れるものから進める。
- 表・注記・possible_tableをAnnexごとに確認する。
- 複合入口を使う場合は、dispatch/fallback履歴と子profile provenanceのレビュー負荷を明示する。
- 現行CLIでは `--family PICS` を付け、meta familyを明示する。
- Annexes refinedは現行mainでstrict failしているため、page-number-only line除去後に再評価する。

### 方針

PIC/SはTXTベースで進める。既存profileとテスト資産が最も使える。

推奨順:

1. Annex 11
2. Annex 1
3. Annex 2A
4. Part II
5. Part I
6. Annex 15
7. Annexes refinedは横断検索・参考候補として維持し、正式化は最後に判断する。

Annex 11は現行main再生成でstrict / GOAL / promotion GOALがpassし、warningなし、table/noteなし。PIC/Sの最初の正規化RUN候補とする。

Annex 1、Annex 2A、Part IIはreadyだが、表・注記またはfigureを含むため、promotion candidate化前にSAMPLE_COMPARISONで確認する。Part Iは範囲が広いため、Annex単体の運用型を先に固める。

## 13 WHO LBM 3rd

### 現状

- `data/human-readable/who/WHO_LBM_3rd.txt` とPDF sourceがある。
- `who_lbm_3rd_default_v4` でGOAL pass済み。
- 過去記録ではitem粒度は当面許容、UI実レビュー未了。
- 一覧メモ上は2章から11章を対象とする案がある。
- WHO XML入力は現repoでは確認できない。

### 課題

- 正式対象範囲を決める。
  - 2章から11章に切る。
  - 全体を保持し、candidate visibilityで候補表示を絞る。
- item粒度が実利用で細かすぎないか確認する。
- 章単位に分けるか、1文書bundleで保持するか決める。
- general tables / chapter 8 survey parserの成果を正式候補へ含めるか判断する。
- 現行CLIでは `--family WHO_LBM` を付け、meta familyを明示する。

### 方針

WHOはTXTベースで進める。技術課題より、対象範囲と表示粒度の判断が先。

推奨順:

1. 2章から11章を対象範囲とする案で再生成する。
2. 全体保持 + candidate visibility絞り込み案と比較する。
3. 代表章でSAMPLE_COMPARISONを作り、人間レビューで粒度を確認する。
4. 問題なければpromotion candidate化する。

現行main再生成ではstrict / GOAL / promotion GOALがpassし、warningなし。ただし table 15、row 210、note 14 があり、対象範囲とcandidate visibilityの判断が未決のため、EU GMP Chapter 1やPIC/S Annex 11より前には出さない。

## 共通実行計画

### Phase A: 現行CLIで再生成

10/12/13の既存GOAL pass文書を、現行mainで再生成する。

目的:

- 旧成果の `meta_family_missing` が現行で残るか確認。
- `qualitycheck --strict` を再確認。
- `goal_check` と `audit_report` を再作成。

実施済み:

- run: `runs/20260527-105034029_docs-readiness-10-12-13-rerun/`
- 単体8文書はpass。
- PIC/S Annexes refinedはstrict fail。

### Phase B: 文書別readiness表を作る

各文書について、次を一覧化する。

- source有無。
- profile有無。
- GOAL pass/fail。
- quality warnings。
- table/note/possible_table件数。
- promotion candidateに進めるか。
- 追加reviewが必要な点。

実施済み。詳細は `runs/20260527-105034029_docs-readiness-10-12-13-rerun/READINESS_10_12_13.md` を参照する。

### Phase C: promotion candidate化

最初の候補は、説明負荷が小さい単体文書から作る。

推奨:

1. EU GMP Chapter 1
2. PIC/S Annex 11
3. PIC/S Annex 1（表・注記レビュー後）
4. WHO LBM 3rd対象章案（対象範囲とcandidate visibility判断後）

### Phase D: 正式昇格

各文書単位で正規化RUNを切る。`data/normalized/` への複写は親PR承認後の子PRでのみ行う。

## 判断

10/12/13は、生成・検証・監査・RUN運用は共通化できる。一方、文書構造の扱いは次のように分ける。

- EU GMP: 章単位正規化。
- PIC/S: Part/Annex単体正規化。Annexes refinedは後回し。
- WHO LBM: 対象章範囲とcandidate visibilityを先に決める。

このため、まずは共通の再生成・監査RUNを切り、その結果で文書別の正式正規化RUNへ分岐するのが最も安全で早い。
