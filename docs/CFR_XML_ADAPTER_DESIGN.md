# CFR XML Adapter Design

## Conclusion

CFR Part 11 / Part 211 は、`qai_text2ir` の汎用プレーンテキストparserだけで最終GOAL到達扱いにしない。Part 211 は章・節・段落の安定構造を持つため、eCFR XMLを入口にする専用adapterを優先する。

## Proposed Entry

候補名:

- `qai_cfrxml2ir`
- `qai_text2ir.adapters.ecfr_xml`

推奨は `qai_text2ir.adapters.ecfr_xml`。理由は、出力先とGOAL_CHECKをtext2ir系の4ファイル構成に揃えつつ、入力処理だけをadapterとして分離できるため。

## Why XML First

- プレーンテキストではsection境界、paragraph階層、注記、引用、表の折返しが崩れやすい。
- eCFR XMLにはsection番号、見出し、paragraph階層、改正日等の構造情報がある。
- `source_spans` 相当の追跡情報を、行番号よりも安定したXML locatorで表現できる。
- Part 211 はGMPチェックシートで参照頻度が高く、崩れたプレーンテキストを後処理するより、正本構造に寄せた方が監査説明しやすい。

## Output Contract

出力は既存の正規化GOALと同じ4ファイル構成にする。

```text
<doc_id>.regdoc_ir.yaml
<doc_id>.parser_profile.yaml
<doc_id>.regdoc_profile.yaml
<doc_id>.meta.yaml
manifest.yaml
```

必須:

- `schema: qai.regdoc_ir.v4`
- `meta.doc.family: CFR`
- `meta.doc.jurisdiction: US`
- `manifest.parser_profile.provenance`
- `source_spans` 相当のlocator
- promotion/release modeのGOAL_CHECK pass

## IR Mapping

| eCFR概念 | IR kind候補 | 備考 |
|---|---|---|
| title / part | `part` または `chapter` | 既存regdoc_profile側の表示ポリシーと調整 |
| section | `section` または `paragraph` | `num` に `211.XX` / `11.XX` を保持 |
| paragraph | `paragraph` | XML階層があれば親子維持 |
| item / clause | `item` / `subitem` | `(a)` / `(1)` / `(i)` を安定変換 |
| table | `table` / `table_header` / `table_row` | XML tableがある場合のみ構造化 |
| note | `note` | FR note等は本文と分離 |

## Source Locator

推奨locator:

```yaml
source_spans:
  - source_label: eCFR
    locator: xpath:/ECFR/.../SECTION[...]/P[...]
    data:
      section: "211.XX"
      version_date: "YYYY-MM-DD"
```

代替:

- section番号 + paragraph marker
- XML byte offset
- 変換前XMLを保存した場合のline locator

最初のRUNでは `xpath` と `section` の併用を推奨する。

## Migration Plan

1. eCFR XMLサンプルを `data/human-readable` ではなく、入力種別が分かる場所に配置する。
2. adapterでCFR XMLを内部node treeへ変換する。
3. 既存の4ファイルwriter / GOAL_CHECK / audit_reportへ接続する。
4. CFR Part 11で小さく検証する。
5. CFR Part 211でsection階層・表・注記を検証する。
6. promotion candidateはCFR Part 11またはPart 211のどちらか1文書に限定して作る。

## Not Implemented In This Run

このRUNではCFR XML adapterは実装しない。理由:

- 現行repo内に正式代表入力がない。
- Part 211をプレーンテキスト汎用parserで無理に通すと、text2ir本体にCFR固有処理を混ぜるリスクが高い。
- 先にEU GMP Chapter 1でpromotion candidate運用を固める方が安全。

## Next RUN TODO

- eCFR XML入力の取得・保存方針を決める。
- CFR Part 11 / Part 211の対象版日を決める。
- `qai_text2ir.adapters.ecfr_xml` の最小prototypeを作る。
- CFR用regdoc_profileの `selectable_kinds` とcontext表示を定義する。
