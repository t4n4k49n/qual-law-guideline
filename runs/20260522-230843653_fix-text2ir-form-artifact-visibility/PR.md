<!-- PR_BODY_FILE: runs/20260522-230843653_fix-text2ir-form-artifact-visibility/PR.md -->

## まとめ

WHO LBM 3rd の記入式フォーム残骸が通常候補・通常本文のように表示される問題を、文書個別の削除ではなく `text2ir` 共通の artifact visibility と promotion gate で閉じます。これにより、PDF抽出由来のフォーム記入欄はIR内に参照用として残しつつ、DQ/GMPチェック候補や通常レビュー画面には出ない状態にします。

## 変更内容

- `form_artifact` / `not_selectable` / `layout_artifact` を default review / DQ候補から除外する共通判定を追加
- `text_parser` でフォーム残骸を通常本文から分離し、`form_artifact.text` を短いsummaryに制限
- raw情報は `data.raw_text_escaped` に保持し、通常表示対象外であることを明示
- `goal_check --mode promotion` で default-visible form leakage、長すぎる artifact text、literal PUA をFAIL化
- WHO LBM Table 5 fixture、mock UI visibility、goal_check regression を追加
- 代表9文書を再生成し、review UI用 `out/*_review_ui/` に複写

## 検証

- `python -m pytest -q`
  - `171 passed, 1 skipped`
- 代表9文書の再生成
  - 全件成功
- 代表9文書の `goal_check --mode promotion`
  - 全件PASS
- artifact visibility audit
  - literal PUA: 全件0
  - default-visible form leakage: 全件0
  - candidate export leakage: 全件0
  - WHO LBM form_artifact: 3件、長文artifact text: 0件

## 主要成果物

- `runs/20260522-230843653_fix-text2ir-form-artifact-visibility/RUN.md`
- `runs/20260522-230843653_fix-text2ir-form-artifact-visibility/FORM_ARTIFACT_VISIBILITY_AUDIT.md`
- `runs/20260522-230843653_fix-text2ir-form-artifact-visibility/WHO_LBM_TABLE5_7_REVIEW.md`
- `runs/20260522-230843653_fix-text2ir-form-artifact-visibility/GOAL_CHECK_SUMMARY.md`
