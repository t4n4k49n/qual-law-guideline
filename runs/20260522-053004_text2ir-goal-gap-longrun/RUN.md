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
| 0 | 現状確認・ベースライン固定 | 完了 | #132 |
| 1 | GOAL検証ハーネス | 完了 | #133 |
| 2 | 監査レポート生成 | 完了 | #134 |
| 3 | 表・注記・子孫表示の実データ検証 | 完了 | #135 |
| 4 | profile修正 | 完了 | #136 |
| 5 | 複合入口・特別部品設計 | 完了 | #137 |
| 6 | 代表文書再生成・GOAL評価 | 完了 | TBD |

## Phase 1 実行内容

追加:

- `src/qai_text2ir/goal_check.py`
- `tests/test_text2ir_goal_check.py`

実装内容:

- text2ir bundle directoryとdoc_idを指定し、4ファイル、IR schema、node field、nid/ord、source_spans coverage、meta、parser_profile、regdoc_profile、manifestを一括確認するGOAL検証ハーネスを追加。
- `python -m qai_text2ir.goal_check --bundle-dir <dir> --doc-id <doc_id> --format markdown|json|yaml` で実行可能にした。
- 機械可読サマリとMarkdownサマリを出力可能にした。

テスト:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_goal_check.py
.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_bundle.py tests\test_markdown_table_parsing.py tests\test_normal_note_descendants.py tests\test_text2ir_goal_check.py
.\.venv\Scripts\python.exe -m pytest -q
```

結果:

- `5 passed`
- `13 passed`
- `153 passed, 1 skipped`

## Phase 2 実行内容

追加:

- `src/qai_text2ir/audit_report.py`
- `tests/test_text2ir_audit_report.py`

実装内容:

- `out/<run_id>/<doc_id>/` 形式の複数bundleを横断し、doc_id、入力、parser profile、schema、4ファイル、manifest、strict、warnings、node数、kind別件数、source_spans coverage、table/note件数、profile provenance、refine適用数、GOALチェック結果を集計する監査レポート生成を追加。
- `python -m qai_text2ir.audit_report --run-out-dir <dir> --format markdown|json|yaml --out <path>` で実行可能にした。

テスト:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_text2ir_audit_report.py tests\test_text2ir_goal_check.py
.\.venv\Scripts\python.exe -m pytest -q
```

結果:

- `7 passed`
- `155 passed, 1 skipped`

## Phase 3 実行内容

追加・変更:

- `tests/fixtures/text2ir/pics_annex1_table2_markdown_excerpt.txt`
- `tests/fixtures/text2ir/pics_annex1_table2_plaintext_excerpt.txt`
- `tests/test_table_note_real_samples.py`
- `src/qai_text2ir/text_parser.py`
- `runs/20260522-053004_text2ir-goal-gap-longrun/TABLE_NOTE_REAL_SAMPLE_REVIEW.md`

実装内容:

- Markdown table構造化時に、table/header/row/noteへ `data` payloadを付与する。
- 表下注記を `note` として保持し、`data.note_type: table_note` を付与する。
- profileで `preprocess.detect_plaintext_tables.enabled` を有効化した場合のみ、プレーンテキスト表らしきブロックを `preformatted` / `possible_table` として保持する。
- 低信頼な固定幅表は無理に `table_row` 化せず、`possible_plaintext_table_not_structured` タグとsource_spansでレビュー対象にする。

テスト:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_table_note_real_samples.py tests\test_markdown_table_parsing.py tests\test_normal_note_descendants.py tests\test_text2ir_goal_check.py
.\.venv\Scripts\python.exe -m pytest -q
```

結果:

- `15 passed`
- `158 passed, 1 skipped`

## Phase 4 実行内容

追加・変更:

- `src/qai_text2ir/text_parser.py`
- `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml`
- `src/qai_text2ir/profiles/pics_annex11_default_v1.yaml`
- `src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml`
- `src/qai_text2ir/profiles/pics_part2_default_v1.yaml`
- `tests/fixtures/pics_annex15_heading_continuation_fixture.txt`
- `tests/fixtures/pics_annex2a_part_hierarchy_fixture.txt`
- `tests/test_pics_annex2a_profile.py`
- `runs/20260522-053004_text2ir-goal-gap-longrun/PROFILE_FIX_REVIEW.md`
- `runs/20260522-053004_text2ir-goal-gap-longrun/WHO_LBM_CANDIDATE_GRANULARITY_REVIEW.md`

実装内容:

- Annex 15の見出し継続をprofileで有効化できる汎用オプションを追加。
- Annex 11とPart IIは `section` を `structural_kinds` に含め、見出しと本文を分離。
- Annex 2AはB1等のsection markerを追加。
- WHO LBM 3rdはitem粒度候補10件をレビューし、当面許容と記録。

テスト:

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_pics_annex15_profile.py tests\test_pics_annex11_profile.py tests\test_pics_annex2a_profile.py tests\test_pics_part2_v1.py
.\.venv\Scripts\python.exe -m pytest -q
```

結果:

- `7 passed`
- `160 passed, 1 skipped`

## Phase 5 実行内容

追加:

- `runs/20260522-053004_text2ir-goal-gap-longrun/EXTENSION_ENTRANCE_DESIGN.md`

内容:

- PIC/S PE 009-17 Annexes全体 refinedを、親入口と子profile群からなる複合入口として整理。
- CFR Part 211 / Part 11は、現行repoに正式代表入力がないため再生成対象にせず、eCFR XML等の安定構造入力を優先する拡張入口として設計。
- 複雑表・PDF崩れ表は共通parserへ過剰実装せず、Markdown table、単純固定幅表、複雑表の3段階に分けて境界を定義。

## Phase 6 実行内容

代表9文書を `out/20260522-053004_text2ir-goal-gap-longrun/<doc_id>/` へ再生成した。

結果:

- 9文書すべて `--qualitycheck --strict` exit 0。
- 9文書すべて `python -m qai_text2ir.goal_check` exit 0。
- `TEXT2IR_AUDIT_REPORT.md` / `text2ir_audit_report.json` を作成。
- 関連テスト `17 passed`。
- 全体テスト `160 passed, 1 skipped`。

作成:

- `GOAL_CHECK_RESULTS.md`
- `goal_check_results.json`
- `TEXT2IR_AUDIT_REPORT.md`
- `text2ir_audit_report.json`
- `TEST_RESULTS.md`
- `IMPLEMENTATION_SUMMARY.md`
- `TEXT2IR_GAP_RESOLUTION_MATRIX.md`
- `PROMOTION_CANDIDATE_REVIEW.md`
- `NEXT_REVIEW_REQUEST.md`

補足:

- CFR Part 11 / Part 211 は現行repo内に正式代表入力がないため再生成対象外。

## Phase 7 実行内容

Phase 6で再生成済みの出力から、正式昇格ではなく人間レビュー用の review candidate を作成した。`data/normalized/` へのコピーは行っていない。

作成先:

- `runs/20260522-053004_text2ir-goal-gap-longrun/review_candidate/eu_gmp_vol4_chap1_20130131/`
- `runs/20260522-053004_text2ir-goal-gap-longrun/review_candidate/pics_pe00917_annex15_20230825/`
- `runs/20260522-053004_text2ir-goal-gap-longrun/review_candidate/pics_pe00917_annex11_20230825/`

各候補に含めたもの:

- `<doc_id>.regdoc_ir.yaml`
- `<doc_id>.parser_profile.yaml`
- `<doc_id>.regdoc_profile.yaml`
- `<doc_id>.meta.yaml`
- `manifest.yaml`
- `GOAL_CHECK_RESULT.md`
- `SAMPLE_COMPARISON.md`
- `QUALITYCHECK_RESULT.md`

補足:

- 複製元は `out/20260522-053004_text2ir-goal-gap-longrun/<doc_id>/`。
- 候補化対象は、長期指示書の優先順に従い、EU GMP Chapter 1、PIC/S Annex 15、PIC/S Annex 11とした。
- `data/normalized/` は未変更。

確認:

- review candidate 3文書すべて `python -m qai_text2ir.goal_check` 相当の確認でPASS。
- 3文書とも warning は `meta_family_missing` のみ。
