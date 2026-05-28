# PIC/S Annex 15 目検最終確認・校正

## 対象

- doc_id: `pics_pe00917_annex15_20230825`
- source: `data/human-readable/pics/pe009-17_annex15_2023-08-25_en.txt`
- generated bundle: `out/20260529-053112180_feat-pics-annex15-final-review-v1/pics_pe00917_annex15_20230825_after_heading_fix`

## Table / Warning確認

| 確認項目 | 結果 |
|---|---|
| 原文のTable/Figure/Warning/Note候補検索 | 構造化対象のTable/Figure/Warning/Noteなし |
| IRの `kind: table` / `kind: table_row` / `kind: note` / `preformatted` | none |
| `possible_plaintext_table_not_structured` / `possible_form_or_table` scan | none |
| special structure audit | pass (`source_tables=0`, `source_figures=0`, `unresolved_special_blocks=0`) |
| promotion goal check | pass, warnings none |

## 校正で修正した点

原文では以下の通り、`General` は `5. PROCESS VALIDATION` の次行に置かれた小見出し相当の行だった。

```text
253: 5.             PROCESS VALIDATION
254: General
```

修正前IRでは `heading: PROCESS VALIDATION General` となっていたため、Annex 15プロファイルでTitle Case単語を見出し継続から除外した。修正後は以下の形で保持される。

```yaml
nid: ann15.sec5
kind: section
heading: PROCESS VALIDATION
text: General
```

## 階層サンプル

最大深度5の `ann15.sec5.p5_22.ivi` を抽出した。詳細は `SAMPLE_EXTRACT.md`。
