# 正式版（data/normalized）への格納チェックリスト

目的: `out/<run_id>/` の成果物を `data/normalized/<doc_id>/` に昇格するための最小要件を、短いチェックで満たす。

## チェックリスト（最小）

- [ ] スキーマ検証が通る（IRスキーマ or 別途合意した検証ルール）
- [ ] `out/<run_id>/manifest.yaml` を作成し、入力元・生成コマンド・コミットハッシュを記録した
- [ ] 目視レビュー or サンプル比較を実施した（結果をRUNに簡潔に記録）
- [ ] **比較表の人間可読経路が、対象ノードの祖先を全て含んでいる（章/節/条/項/号/イロハ/枝番など `num` のある階層を省略しない）**

## 作成物

- `out/<run_id>/manifest.yaml`
- `runs/<run_id>/RUN.md`（簡潔でOK）

## 例: manifest.yaml（テンプレ）

```yaml
schema: qai.run_manifest.v1
run_id: 20260206-115043870_run-normalized-checklist
created_at: "2026-02-06T11:50:00Z"
git:
  commit: "<git-commit-hash>"
  branch: "<branch-name>"
input:
  path: "C:\\path\\to\\input.xml"
  checksum: "<sha256>"
command:
  argv: "xml2ir bundle --input ... --out-dir ... --doc-id ..."
outputs:
  doc_id: "<doc_id>"
  files:
    - "<doc_id>.regdoc_ir.yaml"
    - "<doc_id>.parser_profile.yaml"
    - "<doc_id>.regdoc_profile.yaml"
    - "<doc_id>.meta.yaml"
review:
  method: "visual|sample_compare"
  notes: "簡潔に記載"
```

## スキーマ検証の方法（最小）

- 現時点の前提: 出力はIR（YAML）。XSDではなく **IRスキーマ or プロジェクト内の検証ルール**で判定する。
- 最小ルール例:
  - `schema` / `doc_id` / `content` が存在する
  - `content` 直下がツリー構造であり、`nid` が一意である
  - `ord` が `^\d{6}(\.\d{6})*$` に一致する（`root` を除く）
  - 同一親の `children` が `ord` の辞書順で昇順になっている
  - `appendix` の連番や `annex` の `article` 命名が破綻していない
- 実装済みの検証:
  - `tests/test_integration_real_xml.py` 内の `verify` 関数群を利用
  - 例: `assert_unique_nids`, `check_annex_article_nids`, `check_appendix_scoped_indices`

## レビューの最小ルール（目視）

- 1件以上の条文をピックアップし、以下を確認する
  - 条文の見出し（条タイトル）と本文の対応が崩れていない
  - 号・イロハが正しい階層（条→号→イロハ）で並んでいる
  - 明らかな欠落（本文の抜け・順序の逆転）が無い
- 実施結果は `runs/<run_id>/RUN.md` に1〜2行で記載する
