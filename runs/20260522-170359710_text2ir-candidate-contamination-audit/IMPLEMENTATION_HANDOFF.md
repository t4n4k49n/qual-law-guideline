# IMPLEMENTATION HANDOFF

## Purpose

次の新規ブランチで、text2ir の selectable candidate contamination を共通対策として実装するための引き継ぎ。

この文書は、WHO LBM 3rd や PIC/S Annex 2A の個別profile修正を指示するものではない。これらは共通対策の代表症例・回帰対象として扱う。

## Target Problem

PDF抽出由来の表・フォーム・チェック欄・固定幅レイアウト崩れが、通常の selectable `item` / `subitem` として出ている。

正式昇格前に止めるべきもの:

- 私用領域文字を含む通常候補
- 長いドットリーダーを含む通常候補
- `YES` / `NO` / `N/A` / `COMMENTS` 等のチェック欄を含む通常候補
- 固定幅列崩れを本文として吸収した通常候補
- 表キャプション・表行・フォーム行が通常候補へ混入したもの

## Candidate Files to Inspect

実装時はまず以下を読む。

- `src/qai_text2ir/text_parser.py`
  - 通常ノード化、preformatted判定、qualitycheck、table/note処理の主処理。
  - 関連関数候補: `is_preformatted_line`, `_is_preformatted_text_block`, `qualitycheck_document`, `run_text_postprocess_and_qualitycheck`
- `src/qai_text2ir/goal_check.py`
  - promotion / release 前のbundle検査。
  - selectable candidate contamination の最終ゲート候補。
- `src/qai_text2ir/audit_report.py`
  - 文書横断の監査表示。
  - 修正後のsummaryに contamination status を出す候補。
- `src/qai_text2ir/cli.py`
  - `--qualitycheck --strict` の挙動確認。
- `tests/test_text2ir_goal_check.py`
  - promotion mode の検査追加先。
- `tests/test_text2ir_who_lbm_3rd.py`
  - WHO代表症例の回帰追加候補。
- `tests/test_pics_annex2a_preformatted.py`
  - Annex 2A代表症例の回帰追加候補。
- `tests/test_table_note_real_samples.py`
  - preformatted / possible_table の既存期待挙動確認。

## Implementation Scope

### 1. Common Detector

共通検出関数を実装する。配置候補は `src/qai_text2ir/goal_check.py` か、新規の小さな共通モジュール。

検出入力:

- node text
- node kind
- selectable kinds
- source_spans

検出対象:

- `private_use_char`: `[\uE000-\uF8FF]`
- `dot_leader`: `\.{8,}`
- `checklist_columns`: 大文字語としての `YES`, `NO`, `N/A`, `COMMENTS`, `CHECKED ITEM`
- `fixed_width_columns`: 複数回の長い空白、列崩れを示す繰り返し spacing
- `table_or_form_caption_mix`: `Table <number>` 等とフォーム列・固定幅行が同一候補に混在
- `bullet_form_row`: bullet行に dot leader / check mark / checklist column が混ざる

注意:

- 小文字の通常英文 `no` は誤検出しない。
- 入力に私用領域文字があることだけを即エラーにしない。問題は selectable 通常候補に出ること。
- `preformatted` / `table` / `table_row` / `note` など、表示上別扱いにできるkindは通常 `item` / `subitem` より軽く扱う。

### 2. Promotion Gate

`goal_check --mode promotion` で selectable candidate contamination を検査する。

推奨判定:

- `mode=normal`: warning
- `mode=promotion`: error または fail相当
- `mode=release`: error

最低限、promotion candidateで以下が残る場合は fail に寄せる。

- selectable `item` / `subitem` / `paragraph` / `statement` に `private_use_char` と `dot_leader` が同居
- selectable `item` / `subitem` に `private_use_char` と `fixed_width_columns` が同居
- selectable候補に `YES` / `NO` / `N/A` / `COMMENTS` のフォーム列がまとまって入る

### 3. Parser-Side Guard

promotion gate だけでなく、可能なら `text_parser.py` 側にも通常ノード化抑止を入れる。

方針:

- 汚染度が高い行・ブロックを通常 `item` / `subitem` にしない。
- 既存schemaで扱えるなら `preformatted` とし、`kind_raw` / `data` に `possible_table` または `possible_form` 相当の情報を残す。
- 既存の `possible_plaintext_table_not_structured` の流れが使える場合はそれに寄せる。
- 本文として意味のある通常箇条書きまで潰さない。

### 4. Audit Report Extension

必要なら `audit_report.py` に contamination summary を追加する。

例:

- contamination_status: `pass` / `warn` / `fail`
- contamination_findings_count
- severe_contamination_count

これは必須ではないが、代表文書を横断比較するうえで有効。

## Regression Targets

### WHO LBM 3rd

対象症例:

- `who_lbm_3rd_2004_9241546506`
- `cha8.i5`
- `cha8.i5.si1`
- `cha8.i5.si2`

期待:

- `.............   ` を含む通常 selectable `item` / `subitem` が残らない。
- 該当ブロックを完全削除しない。非選択のpreformatted/form/table候補として保持するか、promotion gateで明確に止める。

### PIC/S Annex 2A

対象症例:

- `pics_pe00917_annex2a_20230825`
- `ann2a.sec2.ib.si1`
- `ann2a.sec2.ib.si2`
- `ann2a.sec2.ib.si3`
- `pics_pe00917_annexes_20230825_refined_v3_extends_trace` 内の同等箇所

期待:

- `` と固定幅三列崩れを含む通常 selectable `subitem` が残らない。
- Annexes refined 側でも同じ問題が再発しない。

## Non-Regression Targets

今回の監査で severe 0 だった以下は悪化させない。

- `eu_gmp_vol4_chap1_20130131`
- `pics_pe00917_annex11_20230825`
- `pics_pe00917_annex15_20230825`
- `pics_pe00917_part1_20230825`
- `pics_pe00917_part2_20230825`

## Required Tests

最低限追加する。

ここに列挙するテストは、実装が意図通り動くことを確認するための手段である。後述の `Acceptance Criteria` はテスト配下の項目ではなく、再生成・監査・目視確認まで含めた最終合格基準である。

- `tests/test_text2ir_goal_check.py`
  - selectable node に private-use + dot leader があると promotion mode で fail する。
  - normal mode では warning として観測できる。
  - `preformatted` 等の非通常候補は同じ扱いで落とさない、または severityを下げる。
- `tests/test_text2ir_who_lbm_3rd.py`
  - WHO代表fixtureで `cha8.i5.si1` / `cha8.i5.si2` 相当が通常 selectable候補として残らない。
- `tests/test_pics_annex2a_preformatted.py`
  - Annex 2Aの固定幅・私用領域文字混在ブロックが通常 subitem として残らない。

## Regeneration and Audit Commands

実装後に、代表9文書を最新text2irで再生成する。

参考にする既存RUN:

- `runs/20260522-130045_text2ir-final-goal-closure/RUN.md`
- `runs/20260522-170359710_text2ir-candidate-contamination-audit/TEXT2IR_CANDIDATE_CONTAMINATION_AUDIT.md`

再生成後、少なくとも以下を確認する。

- `goal_check --mode promotion`
- contamination audit
- review UIでのWHO / Annex 2Aの目視

## Acceptance Criteria

次の条件を満たして初めて「問題解消」と言える。

これは `Required Tests` の子項目ではない。テスト追加だけでなく、代表文書の再生成、contamination audit、必要な目視確認を終えた後に判定する最終条件である。

1. WHO LBM 3rd の severe contamination が 0。
2. PIC/S Annex 2A の severe contamination が 0。
3. PIC/S Annexes refined 内の Annex 2A同等箇所も severe contamination が 0。
4. EU GMP Chapter 1 / PIC/S Annex 11 / PIC/S Annex 15 の既存良好候補が悪化しない。
5. `goal_check --mode promotion` が selectable candidate contamination を検出できる。
6. `data/normalized/` は承認まで変更しない。
7. 修正後の監査結果を新規 `runs/<run_id>/` に残す。

## Branching Plan for Next Work

次の実装は、この監査PRとは別の新規ブランチで行う。

推奨ブランチ名:

```text
fix/text2ir-selectable-contamination-gate
```

推奨run_id:

```text
<yyyymmdd-hhmmssSSS>_fix-text2ir-selectable-contamination-gate
```

## Do Not Do

- WHO LBM 3rd の Table 5-7 だけを塞いで完了扱いにしない。
- PIC/S Annex 2A の該当行だけを個別除外して完了扱いにしない。
- profile修正を共通検出の代替にしない。
- strict成功だけで正式昇格可能と判断しない。
- `data/normalized/` を承認前に更新しない。
