# 正規化RUN: GMP省令 (416M60000100179) - Re-submit

## 概要
- GMP省令のXMLをIR（YAML）へ正規化しました。
- `xml2ir` を使用し、テスト用検証スクリプトをパスしています。

## 実行詳細
- **Run ID**: `20260206-153010_run-normalized-gmp-ordinance`
- **Input**: `416M60000100179_20260501_507M60000100117.xml`
- **Doc ID**: `jp_egov_416M60000100179_20260501_507M60000100117`

## 検証結果
- `verify_temp.py`: **PASS**
  - `assert_unique_nids`: OK
  - `check_annex_article_nids`: OK
  - `check_appendix_scoped_indices`: OK

## 比較サンプル（IR構造確認）
JSONパスと人間可読テキストの対応確認です。

| Level | NID (Partial) | Content (Snippet) |
| :--- | :--- | :--- |
| document | `root` | **document**  |
| chapter | `ch2` | **chapter 第二章**  |
| section | `sec1` | **section 第一節**  |
| article | `art9` | **article 第九条**  |
| paragraph | `p1` | **paragraph 1** <br>医薬品に係る製品の製造所の構造設備は、次に定めるところに適合するものでなければならない。 |
| item | `i5` | **item 五** <br>次に掲げる場合においては、製品等を取り扱う作業室（密閉容器に収められた製品等のみを取り扱う作業室及び製品等から採取された... |
| subitem | `i` | **subitem イ** <br>飛散しやすく、微量で過敏症反応を示す製品等を取り扱う場合 |

## 変更点 (vs 旧PR)
- 比較表のNIDを簡略化（末尾のみ表示）し、可読性を向上
- 文字化けを修正し、章・条の番号が確認できるように改善

## 次のアクション
- マージ後、`data/normalized/` へ正式配置を行います。
