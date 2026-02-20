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

## ord / nid / num（責務分離）
- `nid`: 構造ID（参照/経路復元）
- `num`: 表示用ラベル
- `ord`: 文書内の絶対順序（int）
- `ord` は Num を解釈しない。`Num="15:16"` のような並列表現でもソース順をそのまま保証する。

## 参照ガイド
- 正規化・IR設計の背景: `QAI - YAML構造提案 (2026_2_3 10：10：27).html`
- 文脈呼び出し／祖先の出し分け: `YAML構造設定の質問 (2026_2_4 16：30：21).html`
- モノリポ運用と配置方針: `QAI - Gitで法令データ管理 (2026_2_4 16：33：42).html`

---

## 運用ルール（出力と版管理）
### 原則
- 正規化RUNの正本は `runs/<run_id>/promotion_candidate/` に置く（Git管理対象）
- `out/<run_id>/` は補助出力（任意）
- `data/normalized/` は昇格後の正式版のみを置く

### 正式版の取り扱い
1) まず `runs/<run_id>/promotion_candidate/` に出力する  
2) 親PRでレビューする  
3) 承認後、子PRで `data/normalized/<doc_id>/` に昇格する  

### 正式化の判断基準（最小）
- スキーマ検証が通る
- 入力元・生成コマンド・実行時のコミットハッシュを `runs/<run_id>/promotion_candidate/manifest.yaml` に記録
- 目視レビューまたはサンプル比較を通過

### コードと出力の対応づけ
- 公式版は「どのコミットで生成されたか」を必ず記録する
- バグが見つかった場合は新しい版を作成し、古い版は残す（上書きしない）

### 手順の正本
- 正規化RUNの実行手順は `docs/NORMALIZED_RUN_PLAYBOOK.md` を参照

---

## リポジトリ構成（シンプル案）
```
data/
  normalized/   # 最新成果（上書き可）
  registry/     # 生成履歴・索引
  releases/     # 重要版の固定保存
pipelines/
```
