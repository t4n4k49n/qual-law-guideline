# GMPチェックシート生成UI（モック）

## 起動方法
1. 依存をインストール
   - `pip install streamlit pyyaml`
2. アプリ起動
   - `streamlit run apps/mock_gmp_checklist_ui.py`

## 入力データ
- 優先: `txtconcat_20260222-040007081.txt`（リポジトリ直下）
- 代替: 画面上部の `file_uploader` から txtconcat を指定
- どちらも無い場合は `data/normalized/...336M50000100002...` の `regdoc_ir/regdoc_profile` を自動使用

## 画面の見方
- 左カラム: 検索 + 候補選択（`selectable_kinds` に含まれる kind のみ表示）
- 右カラム: チェックシートプレビュー（`context_display_policy` を反映）
- 下部: 適用中の YAML 設定確認
- `プロファイル切替`
  - オリジナル設定
  - モック用設定
    - `subitem.include_chapeau_text = false`
    - `table_row.include_ancestors_until_kind = table`

## デモボタン
- `デモ1：ロだけ` -> `art12.p1.i2.ro`
- `デモ2：ロ＋ハ` -> `art12.p1.i2.ro`, `art12.p1.i2.ha`
- `デモ3：表1行` -> `appdx_table1.tbl1.tblh.tblr1`
- `デモ4：表2行` -> `appdx_table1.tbl1.tblh.tblr1`, `appdx_table1.tbl1.tblh.tblr2`

## 欠落NIDの扱い
- 既定: `on_missing_nids="error"`（存在しないNIDがあれば例外）
- 旧fold由来らしきNID（例: `art12.i2.ro`）は、`.p1` 挿入候補（例: `art12.p1.i2.ro`）をメッセージで提示
- 互換モード:
  - `on_missing_nids="warn"`: 警告を出して続行
  - `on_missing_nids="ignore"`: 旧挙動（非推奨）

## 要件1〜4の期待結果
1. 要件1（ロだけ）
   - 2行のみ:
   - `（一般区分の医薬部外品製造業者等の製造所の構造設備）`
   - `ロ　常時居住する場所及び不潔な場所から明確に区別されていること。`
2. 要件2（ロ＋ハ）
   - 見出し（文脈ブロック）は1回だけ
   - ロとハが連続表示
3. 要件3（表1行）
   - 表タイトル（別表）+ ヘッダ + 注記 + 1行目を表示
4. 要件4（表2行）
   - 2行目でタイトル/ヘッダ/注記は繰り返さず、行だけ追加

## テスト
- `pytest tests/test_mock_ui_render.py -q`
