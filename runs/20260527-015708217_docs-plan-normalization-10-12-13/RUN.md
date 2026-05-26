# RUN: 20260527-015708217_docs-plan-normalization-10-12-13

## 目的

法令・ガイドライン一覧のうち、11 CFRを一旦除いた `10 EU GMP`, `12 PIC/S`, `13 WHO LBM 3rd` について、正規化へ進めるための課題を共通部分と個別部分に分けて整理する。

## 実施内容

- `README.md` / `local_notes/TODO.md` を確認した。
- `local_notes/KNOWLEDGE.md` を確認した。
- 10/12/13に関係する過去RUNと設計文書を確認した。
  - `runs/20260522-053004_text2ir-goal-gap-longrun/GOAL_CHECK_RESULTS.md`
  - `runs/20260522-053004_text2ir-goal-gap-longrun/TEXT2IR_AUDIT_REPORT.md`
  - `runs/20260522-053004_text2ir-goal-gap-longrun/TEXT2IR_GAP_RESOLUTION_MATRIX.md`
  - `runs/20260522-053004_text2ir-goal-gap-longrun/EXTENSION_ENTRANCE_DESIGN.md`
  - `docs/TEXT2IR_COMPOSITE_ENTRY_DESIGN.md`
  - `docs/CFR_XML_ADAPTER_DESIGN.md`
- 10/12/13の方針を `docs/NORMALIZATION_PLAN_10_12_13.md` に整理した。

## 判断

- 10/12/13は、bundle生成、manifest、profile provenance、qualitycheck、goal_check、audit_report、promotion_candidate運用を共通化できる。
- 文書構造と正式化単位は分ける。
  - EU GMP: 章単位。
  - PIC/S: Part/Annex単体優先。Annexes refinedは後回し。
  - WHO LBM 3rd: 対象章範囲とcandidate visibilityを先に決める。
- 11 CFRはXML入口が有利な別課題であり、この計画には含めない。
- `local_notes/KNOWLEDGE.md` には10/12/13固有の追加技術知見は薄かったが、正規化RUNの昇格元固定運用は適用する。

## 成果

- `docs/NORMALIZATION_PLAN_10_12_13.md`

## 次アクション

1. 10/12/13の既存GOAL pass文書を現行mainで再生成する。
2. 再生成結果からreadiness表を作る。
3. EU GMP Chapter 1、PIC/S Annex 11、PIC/S Annex 1、WHO対象章案の順でpromotion candidate化を検討する。

## 検証

ドキュメントのみの変更。コード・テストは変更しない。
