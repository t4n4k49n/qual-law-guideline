# 原薬GMPガイドライン Heading / Table 正規化候補レビュー

## 判定

PR `#213` のHeading修正を取り込んだmainからfreshに生成した正規化候補である。

Codex目検では、Heading階層と表1の保持状態は正規化候補としてレビュー可能な状態。

## Heading確認

代表パス:

```text
root > cha2 > cha2.sec2_1 > cha2.sec2_1.p2_10
root > cha3 > cha3.sec3_1 > cha3.sec3_1.p3_10
root > cha12 > cha12.sec12_3 > cha12.sec12_3.p12_30
```

確認内容:

| nid | kind | heading/text | 判定 |
|---|---|---|---|
| `cha2.sec2_1` | `section` | `原則` | `2.10` 以降の親として保持 |
| `cha2.sec2_1.p2_10` | `paragraph` | `品質は原薬の生産に関係する全ての人々の責任であること。` | `2.1` 配下 |
| `cha3.sec3_1` | `section` | `従業員の適格性` | `3.10` 以降の親として保持 |
| `cha3.sec3_1.p3_10` | `paragraph` | `中間体・原薬の生産を実施し監督するために...` | `3.1` 配下 |
| `cha12.sec12_3` | `section` | `適格性評価` | `12.30` の親として保持 |
| `cha12.sec12_3.p12_30` | `paragraph` | `プロセスバリデーションの作業を始める前に...` | `12.3` 配下 |

Heading-like short `paragraph` count: `0`.

## 見出しがない章

原文上、章直下に `13.10` などの本文が始まり、`13.1` の中間見出しがない章は、章直下paragraphとして保持する。

| chapter | heading | direct paragraph count |
|---|---|---:|
| `cha13` | `変更管理` | 8 |
| `cha15` | `苦情及び回収` | 6 |
| `cha16` | `受託製造業者（試験機関を含む）` | 7 |

## 表1確認

表1は `1.3 適用範囲` の配下に保持されている。

```text
root > cha1 > cha1.sec1_3 > cha1.sec1_3.tbl1
```

確認内容:

- `cha1.sec1_3.heading`: `適用範囲`
- `cha1.sec1_3.text`: 適用範囲本文を保持
- `cha1.sec1_3.tbl1.heading`: `表１：原薬生産に対する本ガイドラインの適用`
- table count: `1`
- table row count: `26`
- `reconstructed_records`: `7`
- raw rowを保持
- `record_review.table_row_promotion`: `deferred`

## 検証結果

- GOAL check: pass
- Special structure audit: pass
- Source span coverage: `1.0`
- Focused tests: `20 passed`
- Full tests: `253 passed, 1 skipped`

## 結論

このpromotion candidateは、親PRレビューへ進める。

`data/normalized/` への複写は、親PR承認後の子PRでのみ実施する。
