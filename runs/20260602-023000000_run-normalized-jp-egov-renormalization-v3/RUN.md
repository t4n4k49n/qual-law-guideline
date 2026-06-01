# 旧e-Gov正規化 再正規化RUN v3

- run_id: `20260602-023000000_run-normalized-jp-egov-renormalization-v3`
- branch: `run/normalized-jp-egov-renormalization-v3`
- scope: 旧e-Gov正規化の現行基準への再正規化
- promotion candidate: `runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/promotion_candidate/`
- source preparation runs:
  - `runs/20260602-005222271_egov-renormalization-prep/`
  - `runs/20260602-014000000_egov-renormalization-text-cleanup-prep/`

## 前提確認

- `main` は PR `#261` merge後の `origin/main` へ同期済み
- 入力は公式e-Gov API v1から取得済みのXML
- `data/normalized/` はこの親PRでは変更しない
- `data/normalized/ARCHIVE_jp_egov_336M50000100002_20260501_507M60000100117/` は昇格対象外
- この親PRには parser 改修を含めない
- PR本文に対象e-Gov法令URLと深い階層サンプルを直接記載する
- e-Gov法令XMLスキーマ参照: `https://laws.e-gov.go.jp/docs/law-data-basic/419a603-xml-schema-for-japanese-law/`

## 実行環境

- Python: `3.11.6`
- lxml: `6.1.1`
- PyYAML: `6.0.3`
- typer: `0.26.4`
- tool: `qai_xml2ir` `0.1.1`
- base commit: `3bb898e`

## 対象文書

| doc_id | source XML | source URL |
|---|---|---|
| `jp_egov_335AC0000000145_20260501_507AC0000000037` | `data/human-readable/egov/source_xml/335AC0000000145_20260501_507AC0000000037.xml` | `https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037` |
| `jp_egov_336CO0000000011_20260501_507CO0000000362` | `data/human-readable/egov/source_xml/336CO0000000011_20260501_507CO0000000362.xml` | `https://laws.e-gov.go.jp/law/336CO0000000011/20260501_507CO0000000362` |
| `jp_egov_336M50000100001_20260501_507M60000100117` | `data/human-readable/egov/source_xml/336M50000100001_20260501_507M60000100117.xml` | `https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117` |
| `jp_egov_336M50000100002_20260501_507M60000100117` | `data/human-readable/egov/source_xml/336M50000100002_20260501_507M60000100117.xml` | `https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117` |
| `jp_egov_416M60000100179_20260501_507M60000100117` | `data/human-readable/egov/source_xml/416M60000100179_20260501_507M60000100117.xml` | `https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117` |

## 候補作成

各文書を以下の形で生成した。

```powershell
uv run python -m qai_xml2ir.cli bundle `
  --input data/human-readable/egov/source_xml/<law_id>_<as_of>_<revision_id>.xml `
  --out-dir runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/promotion_candidate/<doc_id> `
  --doc-id <doc_id> `
  --retrieved-at 2026-06-02 `
  --source-url https://laws.e-gov.go.jp/law/<law_id>/<as_of>_<revision_id> `
  --xml-family egov `
  --emit-only all
```

## 出力概要

| doc_id | schema | parser_profile.id | article | paragraph | item | subitem | point | table | appendix | annex |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `jp_egov_335AC0000000145_20260501_507AC0000000037` | `qai.regdoc_ir.v4` | `jp_law_default_v1` | 642 | 1467 | 669 | 71 | 0 | 2 | 0 | 57 |
| `jp_egov_336CO0000000011_20260501_507CO0000000362` | `qai.regdoc_ir.v4` | `jp_law_default_v1` | 290 | 673 | 95 | 13 | 0 | 14 | 2 | 156 |
| `jp_egov_336M50000100001_20260501_507M60000100117` | `qai.regdoc_ir.v4` | `jp_law_default_v1` | 967 | 2502 | 2236 | 465 | 67 | 26 | 342 | 502 |
| `jp_egov_336M50000100002_20260501_507M60000100117` | `qai.regdoc_ir.v4` | `jp_law_default_v1` | 35 | 86 | 111 | 175 | 48 | 1 | 1 | 42 |
| `jp_egov_416M60000100179_20260501_507M60000100117` | `qai.regdoc_ir.v4` | `jp_law_default_v1` | 69 | 140 | 260 | 64 | 17 | 0 | 0 | 5 |

## 検証

- `uv run python tools/check_ir_structure.py runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/promotion_candidate`
  - `[OK] no structure problems found (scanned: 20 yaml files)`
- `uv run python -m pytest -q tests/test_xml_common.py tests/test_egov_api_wrapper.py tests/test_egov_text_cleanup.py tests/test_egov_article_structure.py tests/test_egov_table_spans.py tests/test_egov_table_payload_header_inference.py tests/test_xml2ir_no_fold_article.py tests/test_xml2ir_profiles_table_context.py tests/test_ecfr_parser.py`
  - `19 passed`
- `verify_document`
  - 5文書すべて `OK`
- `regdoc_profile` candidate visibility
  - 5文書すべて `allow_rules: []` / `deny_rules: []`
- heading/text whitespace audit
  - 5文書すべて `0`

## 目検・再合成確認

- 旧fold出力で問題になっていた `article.text` は空になり、本文は `paragraph` 以下に保持される。
- `article` 直下の `item/subitem/point` はなく、`article -> paragraph -> item -> subitem -> point` の階層で保持される。
- 表は `table_header` / `table_row` として分離され、結合セルは既存の fill 方針でセル値を複写する。
- e-Gov API v1の `DataRoot/ApplData/LawFullText/Law` ラッパから `LawNum` と `LawBody` を取得できる。
- XML由来の改行・インデントは除去済み。全角スペースは条文内の列挙表現として保持した。

## 深い階層サンプル

- `SAMPLE_EXTRACT.md`
  - 5文書それぞれ1件ずつ、祖先経路を省略せず抽出
- `PR.md`
  - 対象e-Gov法令URLと深い階層サンプル抜粋を本文内に直接記載

## 昇格方針

この親PRでは `data/normalized/` は変更しない。
承認後、`runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/promotion_candidate/` の各doc_id配下から `data/normalized/<doc_id>/` へ複写する子PRを別途作成する。

## 昇格実施記録

- 親PR: `#263`
- 親PR main反映確認: `486e073`
- 昇格ブランチ: `promote/jp-egov-renormalization-v3`
- 昇格元: `runs/20260602-023000000_run-normalized-jp-egov-renormalization-v3/promotion_candidate/`
- 昇格先:
  - `data/normalized/jp_egov_335AC0000000145_20260501_507AC0000000037/`
  - `data/normalized/jp_egov_336CO0000000011_20260501_507CO0000000362/`
  - `data/normalized/jp_egov_336M50000100001_20260501_507M60000100117/`
  - `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/`
  - `data/normalized/jp_egov_416M60000100179_20260501_507M60000100117/`
- 昇格内容: 各doc_idで `promotion_candidate` の4ファイルを複写
  - `regdoc_ir.yaml`
  - `parser_profile.yaml`
  - `regdoc_profile.yaml`
  - `meta.yaml`
- 昇格対象外: `data/normalized/ARCHIVE_jp_egov_336M50000100002_20260501_507M60000100117/`
- 検証:
  - `tools/check_ir_structure.py data/normalized/<doc_id>`: 5件すべて `OK`
  - SHA256確認: 各doc_idの4ファイルは昇格元と昇格先で一致
