# text2ir selectable contamination gate

<!-- PR_BODY_FILE: runs/20260522-173239889_fix-text2ir-selectable-contamination-gate/PR.md -->

## まとめ

PDF抽出由来の表・フォーム・チェック欄・固定幅崩れが、DQチェックシート向けの通常候補として表示される問題を、文書別patchではなく text2ir 共通の検出・抑止・昇格前ゲートとして実装しました。WHO LBM 3rd の `cha8.i5` 近傍と PIC/S Annex 2A の固定幅表崩れを代表症例として確認し、同種の重大汚染が正式昇格候補に残らないようにしています。

## 変更内容

- `qai_text2ir.contamination` を追加し、selectable candidate contamination の共通detectorを実装
- `goal_check` に contamination summary を追加
- severe contamination は `promotion` / `release` modeでerror化
- parser postprocess後に、重大汚染の通常候補を `preformatted` / `possible_form` / `possible_table` へ降格
- WHO LBM 3rd / PIC/S Annex 2A の代表回帰テストを追加
- 代表9文書を再生成し、promotion goal_check と critical node の解消状況を記録

## 確認結果

- targeted tests: `18 passed`
- broader text2ir/profile tests: `30 passed`
- full pytest: `171 passed, 1 skipped`
- 代表9文書 promotion goal_check: `9/9 pass`
- WHO LBM 3rd severe contamination: `0`
- PIC/S Annex 2A severe contamination: `0`
- PIC/S Annexes refined 内 Annex 2A同等箇所 severe contamination: `0`

## 主要成果物

- `runs/20260522-173239889_fix-text2ir-selectable-contamination-gate/RUN.md`
- `runs/20260522-173239889_fix-text2ir-selectable-contamination-gate/CONTAMINATION_RESOLUTION_SUMMARY.md`
- `runs/20260522-173239889_fix-text2ir-selectable-contamination-gate/contamination_resolution_summary.json`

## 補足

- `data/normalized/` は変更していません。
- 軽微な contamination finding はsummaryに残しますが、warningノイズにはせず、正式昇格を止める対象は severe finding に限定しています。
