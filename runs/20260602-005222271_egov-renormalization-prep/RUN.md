# 旧e-Gov正規化 再正規化準備RUN

## 目的

「旧e-Gov正規化を現行基準へ再正規化する」を、以下のように定義する。

- 旧e-Gov正規化: `data/normalized/jp_egov_*` に存在する、fold廃止前または旧パーサ出力のe-Gov正規化データ
- 現行基準: `article -> paragraph -> item/subitem/point` を維持し、`article.text` を空にする現行IR構造
- 再正規化: 既存YAMLを救済移行するのではなく、公式e-Gov XMLから現行 `xml2ir bundle --xml-family egov` で再生成すること

## 対象

| doc_id | 公式URL | 旧出力の構造問題 |
|---|---|---:|
| `jp_egov_335AC0000000145_20260501_507AC0000000037` | `https://laws.e-gov.go.jp/law/335AC0000000145/20260501_507AC0000000037` | 734 |
| `jp_egov_336CO0000000011_20260501_507CO0000000362` | `https://laws.e-gov.go.jp/law/336CO0000000011/20260501_507CO0000000362` | 382 |
| `jp_egov_336M50000100001_20260501_507M60000100117` | `https://laws.e-gov.go.jp/law/336M50000100001/20260501_507M60000100117` | 1200 |
| `jp_egov_336M50000100002_20260501_507M60000100117` | `https://laws.e-gov.go.jp/law/336M50000100002/20260501_507M60000100117` | 0 |
| `jp_egov_416M60000100179_20260501_507M60000100117` | `https://laws.e-gov.go.jp/law/416M60000100179/20260501_507M60000100117` | 98 |

`ARCHIVE_jp_egov_336M50000100002_20260501_507M60000100117` は正式対象ではなく、過去版比較用として扱う。

## 入力XML

repo内に旧e-GovのXML正本が残っていなかったため、公式e-Gov API v1から再取得した。

保存先:

- `data/human-readable/egov/source_xml/335AC0000000145_20260501_507AC0000000037.xml`
- `data/human-readable/egov/source_xml/336CO0000000011_20260501_507CO0000000362.xml`
- `data/human-readable/egov/source_xml/336M50000100001_20260501_507M60000100117.xml`
- `data/human-readable/egov/source_xml/336M50000100002_20260501_507M60000100117.xml`
- `data/human-readable/egov/source_xml/416M60000100179_20260501_507M60000100117.xml`

## 切り分け

### xml2ir共通部

- `src/qai_xml2ir/xml_common.py`
  - `parse_xml_document()` を追加
  - `lxml.etree.XMLParser(huge_tree=True)` を共通化
  - 薬機法XMLの巨大テキストノードで `xmlSAX2Characters: huge text node` になる問題を解消
- `src/qai_xml2ir/ecfr_parser.py`
  - CFR側も同じ共通XML読込を使用

### xml2ir e-Gov個別部

- `src/qai_xml2ir/egov_parser.py`
  - e-Gov API v1の `DataRoot/ApplData/LawFullText/Law` ラッパから `LawBody` / `LawNum` を読むよう修正
  - `LawNum` が空の `ApplData/LawNum` に吸われ、`doc_type` が誤る問題を解消
- `src/qai_xml2ir/cli.py`
  - 日本語の `法律` 判定を `guess_doc_type()` に保持

### その他

- 入力XMLの正本を `data/human-readable/egov/source_xml/` に追加
- trial candidate は `runs/20260602-005222271_egov-renormalization-prep/trial_candidates_r4/` を正候補とする
- `trial_candidates` / `trial_candidates_r2` / `trial_candidates_r3` は準備中の失敗・再実行履歴

## trial candidate

生成コマンドの形:

```powershell
uv run python -m qai_xml2ir.cli bundle `
  --input data/human-readable/egov/source_xml/<law_id>_<as_of>_<revision_id>.xml `
  --out-dir runs/20260602-005222271_egov-renormalization-prep/trial_candidates_r4/<doc_id> `
  --doc-id <doc_id> `
  --retrieved-at 2026-06-02 `
  --source-url https://laws.e-gov.go.jp/law/<law_id>/<as_of>_<revision_id> `
  --xml-family egov `
  --emit-only all
```

trial candidate件数:

| doc_id | article | paragraph | item | table | note |
|---|---:|---:|---:|---:|---:|
| `jp_egov_335AC0000000145_20260501_507AC0000000037` | 642 | 1467 | 669 | 2 | 0 |
| `jp_egov_336CO0000000011_20260501_507CO0000000362` | 290 | 673 | 95 | 14 | 0 |
| `jp_egov_336M50000100001_20260501_507M60000100117` | 967 | 2502 | 2236 | 26 | 0 |
| `jp_egov_336M50000100002_20260501_507M60000100117` | 35 | 86 | 111 | 1 | 0 |
| `jp_egov_416M60000100179_20260501_507M60000100117` | 69 | 140 | 260 | 0 | 0 |

## 検証

```powershell
uv run python tools/check_ir_structure.py runs/20260602-005222271_egov-renormalization-prep/trial_candidates_r4
```

結果:

```text
[OK] no structure problems found (scanned: 20 yaml files)
```

```powershell
uv run python -m pytest -q tests/test_xml_common.py tests/test_egov_api_wrapper.py tests/test_egov_article_structure.py tests/test_egov_table_spans.py tests/test_egov_table_payload_header_inference.py tests/test_xml2ir_no_fold_article.py tests/test_xml2ir_profiles_table_context.py tests/test_ecfr_parser.py
```

結果:

```text
17 passed
```

## 次の正規化RUN方針

- 正規化RUNでは `trial_candidates_r4` と同じ入力XML・同じコマンド系列で `promotion_candidate/` を生成する
- 対象は上記5件
- 親PRでは `promotion_candidate/` をレビューし、承認後に子PRで `data/normalized/<doc_id>/` へ昇格する
- `data/normalized/ARCHIVE_*` は昇格対象外のまま維持する
