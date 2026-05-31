# 深い階層サンプル抽出

- source: `runs/20260531-125138676_run-normalized-mhlw-csv-guideline-v3/promotion_candidate/jp_mhlw_csv_guideline_20101021.regdoc_ir.yaml`
- target_nid: `cha3.i1.si4.poi1`
- method: IR YAMLをparseし、target_nidの祖先経路を抽出

| 階層 | nid | kind | kind_raw | text / heading |
|---:|---|---|---|---|
| 1 | `root` | `document` |  |  |
| 2 | `cha3` | `chapter` | `1.` | `コンピュータ化システムの開発、検証及び運用管理に関する文書の作成` |
| 3 | `cha3.i1` | `item` | `(1)` | `コンピュータ化システムの開発、検証及び運用管理に関する基本方針` |
| 4 | `cha3.i1.si4` | `subitem` | `④` | `基本的な考え方` |
| 5 | `cha3.i1.si4.poi1` | `point` | `・` | `ソフトウェアのカテゴリ分類` |

## レビュー用読み下し

```text
3. コンピュータ化システムの開発、検証及び運用管理に関する文書の作成
  (1) コンピュータ化システムの開発、検証及び運用管理に関する基本方針
    ④ 基本的な考え方
      ・ソフトウェアのカテゴリ分類
```

このサンプルは、原文上で `④ 基本的な考え方` の配下にある中黒項目が、IRでも `cha3.i1.si4` の子 `cha3.i1.si4.poi1` として表現されていることを確認するためのもの。
