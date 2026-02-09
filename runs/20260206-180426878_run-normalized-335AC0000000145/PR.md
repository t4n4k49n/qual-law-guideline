# PR: PMD Act 正規化RUN（20260206-180426878_run-normalized-335AC0000000145）

## 変更内容
- PMD Act XML を xml2ir で正規化し、IR/プロファイル/メタを生成

## 検証結果
- verify.py の最小チェックを通過
  - assert_unique_nids: OK
  - check_annex_article_nids: OK
  - check_appendix_scoped_indices: OK

## AIレビュー（目視代替）
- 断片抽出により階層の整合性を確認（最終確認は人間がPRで実施）

## 比較表（人間レビュー用）
| 人間可読（祖先をすべて含む） | YAML断片（祖先をすべて含む） |
| --- | --- |
| document → chapter（第七章: 医薬品、医療機器及び再生医療等製品の販売業等） → section（第一節: 医薬品の販売業） → article（第二十九条の二: （店舗販売業者の遵守事項）） → paragraph（1: 厚生労働大臣は、厚生労働省令で、次に掲げる事項その他店舗の業務に関し店舗販売業者が遵守すべき事項を定めることができる。） → item（二: 店舗における医薬品の販売又は授与の実施方法（その店舗においてその店舗以外の場所にいる者に対して次のイ又はロに掲げる医薬品を販売し、又は授与する場合におけるその者との間の通信手段に応じた当該実施方法を含む。）に関する事項） → subitem（ロ: 一般用医薬品） | - kind: document<br>  nid: root<br>- kind: chapter<br>  nid: ch7<br>  num: 第七章<br>  heading: 医薬品、医療機器及び再生医療等製品の販売業等<br>- kind: section<br>  nid: ch7.sec1<br>  num: 第一節<br>  heading: 医薬品の販売業<br>- kind: article<br>  nid: art29_2<br>  num: 第二十九条の二<br>  heading: （店舗販売業者の遵守事項）<br>- kind: paragraph<br>  nid: art29_2.p1<br>  num: 1<br>  text: 厚生労働大臣は、厚生労働省令で、次に掲げる事項その他店舗の業務に関し店舗販売業者が遵守すべき事項を定めることができる。<br>- kind: item<br>  nid: art29_2.p1.i2<br>  num: 二<br>  text: 店舗における医薬品の販売又は授与の実施方法（その店舗においてその店舗以外の場所にいる者に対して次のイ又はロに掲げる医薬品を販売し、又は授与する場合におけるその者との間の通信手段に応じた当該実施方法を含む。）に関する事項<br>- kind: subitem<br>  nid: art29_2.p1.i2.ro<br>  num: ロ<br>  text: 一般用医薬品 |

## 備考
- 入力XML: %USERPROFILE%\Documents\GitHub\qual-law-guideline_OLD-HANDMADE\data\xml\335AC0000000145_20260501_507AC0000000037\335AC0000000145_20260501_507AC0000000037.xml
- DocID: jp_egov_335AC0000000145_20260501_507AC0000000037
