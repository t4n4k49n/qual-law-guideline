# EU GMP Chapter 2 構造再合成チェック

- IR: `runs/20260601-035105630_run-normalized-eu-gmp-vol4-chap2-v1/promotion_candidate/eu_gmp_vol4_chap2_20140328.regdoc_ir.yaml`
- source: `data/human-readable/eu_gmp/vol4/source_texts/2014-03_chapter_2.txt`
- method: IR YAMLをparseし、source span順、section再構成、item階層、脚注混入、改行・空白を確認

## 全体

- chapter: `1`
- document: `1`
- item: `28`
- paragraph: `23`
- preamble: `1`
- section: `6`

## 表・note

- source上の `Table` 見出し候補: `0`
- IR table nodes: `0`
- IR note nodes: `0`
- 判定: Chapter 2本文には表が無いため、表再合成は該当なし。`special_structure_audit` でも source_tables/generated_tables/unresolved がすべて `0`。

## 項番なしheading

| nid | heading | paragraph範囲 | source line |
|---|---|---|---:|
| `cha2.sec1` | `Principle` | `` | 57 |
| `cha2.sec2` | `General` | `2.1-2.4` | 66 |
| `cha2.sec3` | `Key Personnel` | `2.5-2.9` | 94 |
| `cha2.sec4` | `Training` | `2.10-2.14` | 206 |
| `cha2.sec5` | `Personnel Hygiene` | `2.15-2.22` | 234 |
| `cha2.sec6` | `Consultants` | `2.23` | 269 |

## item階層

| parent | num | child nums |
|---|---|---|
| `cha2.sec3.p2_6` | `2.6` | `a, b` |
| `cha2.sec3.p2_7` | `2.7` | `i, ii, iii, iv, v, vi` |
| `cha2.sec3.p2_8` | `2.8` | `i, ii, iii, iv, v, vi, vii` |
| `cha2.sec3.p2_9` | `2.9` | `i, ii, iii, iv, v, vi, vii, viii, ix, x, xi, xii, xiii` |

## source順序

- 親子内のsource line逆転: `0`
- 判定: PASS

## 脚注・不要改行・スペース

- 脚注由来の禁止文字列hit: `0`
- 判定: PDF脚注本文・脚注番号の混入なし
- heading/textの改行・タブ・前後空白・連続スペースhit: `0`
- 判定: PASS

## 重点サンプル

- `cha2.sec1` `section` line `57`: Principle
- `cha2.sec2` `section` line `66`: General
- `cha2.sec3.p2_6` `paragraph` line `114`: The duties of the Qualified Person(s) are described in Article 51 of Directive 2001/83/EC, and can be summarised as follows:
- `cha2.sec3.p2_7` `paragraph` line `140`: The head of the Production Department generally has the following responsibilities:
- `cha2.sec3.p2_9` `paragraph` line `179`: The heads of Production, Quality Control and where relevant, Head of Quality Assurance or Head of Quality Unit, generally have some shared, or jointly exercised, responsibilities relating to quality including in particul
- `cha2.sec6.p2_23` `paragraph` line `271`: Consultants should have adequate education, training, and experience, or any combination thereof, to advise on the subject for which they are retained. Records should be maintained stating the name, address, qualificatio
