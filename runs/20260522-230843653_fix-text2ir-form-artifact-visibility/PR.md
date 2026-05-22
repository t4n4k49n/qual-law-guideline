<!-- PR_BODY_FILE: runs/20260522-230843653_fix-text2ir-form-artifact-visibility/PR.md -->

## まとめ

このPRの実装差分は、検証の結果、方針不採用としてrevert済みです。履歴上は試行内容とrevertの経緯を残し、mainへ取り込む前提のPRではありません。

## 状態

- `4ce1caf`: form artifact visibility fix の試行
- `9f5a119`: 上記試行をrevert

## 方針

WHO LBM Chapter 8 の特殊性を前提に、今回の共通visibility実装は採用しません。
