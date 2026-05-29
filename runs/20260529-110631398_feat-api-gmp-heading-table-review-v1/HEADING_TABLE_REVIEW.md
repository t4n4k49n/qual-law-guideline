# 原薬GMPガイドライン Heading / Table 目検レビュー

## 判定

正規化RUN前の目検レビューで、旧候補のHeading階層に修正必要な問題を確認した。

修正後の再生成では、Heading階層と表1の接続は正規化RUNへ進められる状態になった。

## Heading確認

旧候補では、次のような見出しが `paragraph` として章直下に置かれ、後続条文と兄弟関係になっていた。

| 例 | 旧構造の問題 | 修正後 |
|---|---|---|
| `2.1 原則` -> `2.10` | `2.1` と `2.10` が兄弟 | `cha2.sec2_1` 配下に `p2_10` |
| `3.1 従業員の適格性` -> `3.10` | `3.1` と `3.10` が兄弟 | `cha3.sec3_1` 配下に `p3_10` |
| `12.3 適格性評価` -> `12.30` | `12.3` と `12.30` が兄弟 | `cha12.sec12_3` 配下に `p12_30` |

修正後の代表パス:

```text
root > cha2 > cha2.sec2_1 > cha2.sec2_1.p2_10
root > cha3 > cha3.sec3_1 > cha3.sec3_1.p3_10
root > cha12 > cha12.sec12_3 > cha12.sec12_3.p12_30
```

Heading-like short `paragraph` count is now `0`.

## 見出しがない章

次の章は原文上、`13.1` のような中間見出しを持たず、`13.10` などの本文が章直下に始まる。このため、修正後もparagraphを章直下に保持する。

| chapter | heading | direct paragraph count |
|---|---|---:|
| `cha13` | `変更管理` | 8 |
| `cha15` | `苦情及び回収` | 6 |
| `cha16` | `受託製造業者（試験機関を含む）` | 7 |

これは「見出しがある条文」と「見出しがない条文」を区別するため、期待どおり。

## 表1確認

表1は修正後も `1.3 適用範囲` の配下に保持されている。

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
- raw rowは保持
- `record_review.table_row_promotion`: `deferred`

## 検証結果

- GOAL check: pass
- Special structure audit: pass
- Source span coverage: `1.0`
- Full tests: `253 passed, 1 skipped`

## 結論

旧promotion candidateはHeading階層が不十分なため、そのまま昇格しない。

このRUNの修正を取り込んだ後、正式な正規化RUNでfreshな `promotion_candidate/` を作成する。
