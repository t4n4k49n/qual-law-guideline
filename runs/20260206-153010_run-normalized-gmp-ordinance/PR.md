# 正規化RUN: GMP省令 (416M60000100179)

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

| Level | NID | Content (Snippet) |
| :--- | :--- | :--- |
| document | `root` | **document**  |
| chapter | `ch2` | **chapter 2** 製造所における医薬品の製造の管理...  |
| section | `ch2.sec1` | **section 1** 製品標準書...  |
| article | `art9` | **article 9** 製造業者等は、医薬品の製品ごとに...  |
| paragraph | `art9.p1` | **paragraph 1** 製造業者等は、医薬品の製造の管理、品質の管理... <br>医薬品の製造の管理、品質の管理及び製造販売業者等への通知（... |
| item | `art9.p1.i5` | **item 5** 再加工を行う場合にあつては、その方法... <br>再加工を行う場合にあつては、その方法、理由及び製造管理者の承認... |
| subitem | `art9.p1.i5.i` | **subitem イ** 再加工することにより生じる不純物、分解物... <br>再加工することにより生じる不純物、分解物、残留溶媒その他の... |

※ コンソール出力時の文字化け等は修正して記載しています。

## 次のアクション
- マージ後、`data/normalized/` へ正式配置を行います。
