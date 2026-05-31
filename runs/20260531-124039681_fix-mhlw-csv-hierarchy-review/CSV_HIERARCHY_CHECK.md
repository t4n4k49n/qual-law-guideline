# CSVガイドライン 階層チェック

- run_id: `20260531-124039681_fix-mhlw-csv-hierarchy-review`
- 対象: MHLW CSVガイドライン parser/profile
- 種別: 正規化RUNではない通常修正

## 指摘箇所

原文では、章3の `(1)` 配下にある `④ 基本的な考え方` の下へ、次の中黒項目がぶら下がる。

```text
④ 基本的な考え方
・ソフトウェアのカテゴリ分類
・製品品質に対するリスクアセスメント
・供給者アセスメント
・開発、検証及び運用段階で実施すべき項目等
・コンピュータシステムの廃棄に関する事項
```

## 修正後の確認結果

実CSV HTMLを `jp_mhlw_csv_guideline_v1` でパースし、該当箇所の親子関係を確認した。

```text
cha3.i1 item コンピュータ化システムの開発、検証及び運用管理に関する基本方針
  cha3.i1.si1 subitem 目的
  cha3.i1.si2 subitem 適用範囲
  cha3.i1.si3 subitem システム台帳の作成
  cha3.i1.si4 subitem 基本的な考え方
    cha3.i1.si4.poi1 point ソフトウェアのカテゴリ分類
    cha3.i1.si4.poi2 point 製品品質に対するリスクアセスメント
    cha3.i1.si4.poi3 point 供給者アセスメント
    cha3.i1.si4.poi4 point 開発、検証及び運用段階で実施すべき項目等
    cha3.i1.si4.poi5 point コンピュータシステムの廃棄に関する事項
```

## 併せて確認した問題

前回の目視で見落としていた別問題として、`1.1 目的` などの小見出しが paragraph の本文先頭に混入していた。
この修正では、CSV profile の `section_decimal` に限り、マーカー残部を `heading` に入れる。

確認例:

```text
cha1.p1_1.heading = 目的
cha1.p1_1.text    = このガイドラインは...
cha1.p1_3.heading = カテゴリ分類
cha1.p1_3.text    = このガイドラインの適用を受ける...
```

## 検証

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_text2ir_csv_guideline.py tests/test_mhlw_csv_annex2_tables.py tests/test_mhlw_csv_annexes.py tests/test_mhlw_csv_annex_source_recovery.py tests/test_candidate_visibility_profiles_6_9.py -q
```

結果: `17 passed`
