# RUN: 20260522-053004_text2ir-goal-gap-longrun

## 目的

`qai_text2ir` の出力を、`qai_xml2ir` の最終正規化GOALと同等の下流利用品質へ近づける。Phase 0からPhase 6までを、Phaseごとにブランチ・コミット・push・PRマージで区切って進める。

## ブランチ運用

- Phase 0: `feature/text2ir-goal-gap-longrun-phase0`
- Phase 1以降: Phaseごとに `feature/text2ir-goal-gap-longrun-phaseN` を作成する

## run_id

`20260522-053004_text2ir-goal-gap-longrun`

## 参照した確認RUN

- `runs/20260522-034415_text2ir-goal-gap-confirmation/RUN.md`
- `runs/20260522-034415_text2ir-goal-gap-confirmation/CODEX_CONFIRMATION_REPORT.md`
- `runs/20260522-034415_text2ir-goal-gap-confirmation/GOAL_CHECKLIST.md`
- `runs/20260522-034415_text2ir-goal-gap-confirmation/TEXT2IR_CURRENT_FEATURES.md`
- `runs/20260522-034415_text2ir-goal-gap-confirmation/REGENERATION_RESULTS.md`
- `runs/20260522-034415_text2ir-goal-gap-confirmation/TEXT2IR_GAP_MATRIX.md`
- `runs/20260522-034415_text2ir-goal-gap-confirmation/TABLE_NOTE_DESCENDANT_REVIEW.md`
- `runs/20260522-034415_text2ir-goal-gap-confirmation/IMPLEMENTATION_DECISION.md`

## 変更禁止事項

- `data/normalized/` へコピーしない。
- text2ir本体に文書固有の文字列・文書名ベタ書き処理を入れない。
- 報告書、RUN、PR本文に個人環境の絶対パスを残さない。
- root直下の `TODO.md` / `KNOWLEDGE.md` を作らない。
- `local_notes/` を親repoのコミット対象にしない。

## Phase 0 実行コマンド

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

結果: `148 passed, 1 skipped`

## 主要判断

- 表・注記は既存fixtureだけで完了扱いにせず、代表文書由来fixtureを追加する。
- WHO LBM 3rdは当面item粒度をDQ候補として許容し、代表候補レビューで確認する。
- 最初の正式化候補はEU GMP Vol.4 Chapter 1とする。ただし本RUNでは `data/normalized/` へ昇格しない。
- 最初のprofile修正対象はPIC/S Annex 15の見出し継続とする。
- CFR Part 211はeCFR XML等の安定構造入力を優先する拡張入口として設計検討へ回す。

## Phase進捗

| Phase | 内容 | 状態 | PR |
|---|---|---|---|
| 0 | 現状確認・ベースライン固定 | 完了 | TBD |
| 1 | GOAL検証ハーネス | 未着手 | |
| 2 | 監査レポート生成 | 未着手 | |
| 3 | 表・注記・子孫表示の実データ検証 | 未着手 | |
| 4 | profile修正 | 未着手 | |
| 5 | 複合入口・特別部品設計 | 未着手 | |
| 6 | 代表文書再生成・GOAL評価 | 未着手 | |
