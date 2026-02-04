# REFERENCE

本リポジトリの指針となる旧管理メモ（HTML）の要点を整理し、常時参照できる形でまとめる。
原典（HTML）は `references/administrators-memos/` に保管し、ここでは要点と参照先を示す。

## 原典（HTML）
- `references/administrators-memos/QAI - Gitで法令データ管理 (2026_2_4 16：33：42).html`
- `references/administrators-memos/QAI - YAML構造提案 (2026_2_3 10：10：27).html`
- `references/administrators-memos/YAML構造設定の質問 (2026_2_4 16：30：21).html`

## 要点（仮GOAL / 方針）
- 法令・ガイドラインを共通フォーマットに正規化し、中間表現（IR）を中核に運用する。
- 入力差分（PDF/HTML/TXT/XML）はアダプタ差分として扱い、成果物（IR/ID/参照関係）は共通化する。
- 文脈を保つため、条文ツリー化と祖先の呼び出しが可能な構造にする。
- UI/表示の都合はメタデータやプロファイルで調整し、文書構造と表示ルールを分離する。
- 海外法令（PIC/S、CFR等）を考慮し、フォルダ構造で法令体系を固定しない（体系はメタで管理）。

## 参照ガイド
- 正規化・IR設計の背景: `QAI - YAML構造提案 (2026_2_3 10：10：27).html`
- 文脈呼び出し／祖先の出し分け: `YAML構造設定の質問 (2026_2_4 16：30：21).html`
- モノリポ運用と配置方針: `QAI - Gitで法令データ管理 (2026_2_4 16：33：42).html`
