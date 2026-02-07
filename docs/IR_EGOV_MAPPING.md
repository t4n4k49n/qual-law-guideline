# IR ↔ e-Gov XML 対応表（親和性の説明）

この文書は「IRの設計がe-Gov法令XMLスキーマと構造的に親和性が高い」ことを示すための対応表です。
完全再現やXSD完全準拠を保証するものではなく、主要な構造要素の対応関係を示します。

## 対応表（主要構造）

| IRのkind | e-Gov XMLの代表タグ | 由来/対応フィールド | 備考 |
| --- | --- | --- | --- |
| document | Law/LawBody | ルート | IRの`root`ノード |
| part | Part | `PartTitle` | 章より上位の区切り |
| chapter | Chapter | `ChapterTitle` | 章 |
| section | Section | `SectionTitle` | 節 |
| subsection | Subsection | `SubsectionTitle` | 款 |
| division | Division | `DivisionTitle` | 目 |
| article | Article | `ArticleTitle` / `ArticleCaption` | 条 / 条見出し |
| paragraph | Paragraph | `ParagraphNum` / `ParagraphSentence` | 項 |
| item | Item | `ItemTitle` / `ItemSentence` | 号 |
| subitem | Subitem1 | `Subitem1Title` / `Subitem1Sentence` | イロハ |
| point | Subitem2/3/4 | `Subitem2Sentence` など | 括弧付き番号など |
| annex | SupplProvision | `SupplProvisionLabel` | 附則 |
| appendix | Appdx* / SupplProvisionAppdx* | `AppdxTitle` 等 | 別表/別記/付表等 |

## テキストの対応（抜粋）

| IRフィールド | e-Gov XMLの由来 |
| --- | --- |
| `article.heading` | `ArticleCaption` |
| `article.num` | `ArticleTitle` |
| `paragraph.num` | `ParagraphNum` |
| `paragraph.text` | `ParagraphSentence` の連結 |
| `item.num` | `ItemTitle` |
| `item.text` | `ItemSentence` の連結 |
| `subitem.num` | `Subitem1Title` 等 |
| `subitem.text` | `Subitem1Sentence` 等の連結 |
| `appendix.text` | 対象タグ直下のテキスト |

## `nid` / `num` / `ord` の役割分担

- `nid`: 構造ID（参照/経路復元用）。
- `num`: 表示ラベル（第〇条、二、ロ など）。
- `ord`: 文書内の絶対順序キー（ソート専用・一意、`qai.regdoc_ir.v3` では文字列）。
- `ord` は ID として使わない（ID は `nid` を使う）。

### `ord` の形式

- 8桁ゼロ埋め連番の文字列（例: `00000001`）。
- root を除く全ノードに付与される。
- `ord` は XML 由来の出現順を表し、`num` の意味解釈には使わない。

## 親和性の根拠（要点）

- e-Gov XMLの主要階層（編/章/節/款/目/条/項/号/イロハ）がIRの`kind`に1対1で対応する。
- 章・節などの見出しは`Title`、条の見出しは`Caption`として自然にIRへ写像できる。
- 号やイロハはXML上の要素階層とIRの`children`階層が一致する。
- `SupplProvision`（附則）や`Appdx*`（別表等）もIRで独立ノードとして保持する。

## 差分・未保持になり得る情報

- ルビ（`Ruby`）や細かな混在要素は、IRではテキストとして平坦化される。
- XML属性（`Delete` / `Hide` など）はIRに保持されない。
- XMLの空要素や正規化前の表記揺れはIR側で正規化される可能性がある。
- `nid` はIR独自で、XMLの識別子とは別物。

## 具体例（IR側の抜粋）

同一条文内の「条 → 号 → イロハ」の対応例。

```yaml
nid: art6
kind: article
num: 第六条
heading: （一般区分の医薬品製造業者等の製造所の構造設備）
children:
- nid: art6.i4
  kind: item
  num: 四
  text: 製造作業を行う場所（以下「作業所」という。）は、次に定めるところに適合するものであること。
  children:
  - nid: art6.i4.i
    kind: subitem
    num: イ
    text: 照明及び換気が適切であり、かつ、清潔であること。
```

対応するe-Gov XMLの構造は概念的に以下のようなイメージになる。

- `Article`（`ArticleTitle`/`ArticleCaption`）
  - `Item`（`ItemTitle`/`ItemSentence`）
    - `Subitem1`（`Subitem1Title`/`Subitem1Sentence`）

## まとめ

IRは「構造階層」と「本文テキスト」の両面でe-Gov XMLの設計思想と整合しており、
主要な条文階層を損なわずに再構成できるため、標準スキーマとの親和性が高い。
