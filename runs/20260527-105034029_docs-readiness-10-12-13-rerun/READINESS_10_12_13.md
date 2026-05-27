# 10/12/13 readiness after current-main rerun

## Summary

`docs/NORMALIZATION_PLAN_10_12_13.md` の Phase A/B として、10 EU GMP、12 PIC/S、13 WHO LBM 3rd の既存GOAL pass文書を現行mainで再生成した。

結果:

- 単体8文書は `--qualitycheck --strict`、GOAL、promotion GOAL がすべてpass。
- 旧成果で全件に出ていた `meta_family_missing` は、現行CLIで `--family` を付けて再生成した結果、解消した。
- PIC/S Annexes refined は `--strict` で fail。`ann20.sec7_2.ii.si14:text: page-number-only line remains` が検出された。
- table/note/possible_table の横断監査では、現行mainで表・注記が実文書本体に反映されるようになっている。
- `data/normalized/` への昇格は未実施。

## Readiness table

| priority | doc_id | source | profile | strict | GOAL | promotion GOAL | family warning | table | row | note | readiness | next action |
|---:|---|---|---|---|---|---|---|---:|---:|---:|---|---|
| 1 | `eu_gmp_vol4_chap1_20130131` | exists | `eu_gmp_chap1_default_v2` | pass | pass | pass | none | 0 | 0 | 0 | ready | 正規化RUNでpromotion candidate化する |
| 2 | `pics_pe00917_annex11_20230825` | exists | `pics_annex11_default_v1` | pass | pass | pass | none | 0 | 0 | 0 | ready | 正規化RUNでpromotion candidate化する |
| 3 | `pics_pe00917_annex1_20230825` | exists | `pics_annex1_default_v2` | pass | pass | pass | none | 6 | 35 | 16 | ready with table review | 表・注記をSAMPLE_COMPARISONで確認後、promotion candidate化する |
| 4 | `who_lbm_3rd_2004_9241546506` | exists | `who_lbm_3rd_default_v4` | pass | pass | pass | none | 15 | 210 | 14 | ready with scope review | 対象章範囲とcandidate visibilityを決めてからpromotion candidate化する |
| 5 | `pics_pe00917_annex2a_20230825` | exists | `pics_annex2a_default_v1` | pass | pass | pass | none | 1 | 6 | 4 | ready with table review | Annex 1後に表・figure確認を行う |
| 6 | `pics_pe00917_part2_20230825` | exists | `pics_part2_default_v1` | pass | pass | pass | none | 1 | 7 | 1 | ready later | Annex単体の後に検討する |
| 7 | `pics_pe00917_part1_20230825` | exists | `pics_part1_default_v3` | pass | pass | pass | none | 0 | 0 | 2 | ready later | Annex単体の後に検討する |
| 8 | `pics_pe00917_annex15_20230825` | exists | `pics_annex15_default_v1` | pass | pass | pass | none | 0 | 0 | 0 | ready later | 優先順外だが単体候補として保持する |
| 9 | `pics_pe00917_annexes_20230825_refined_v3_extends_trace` | exists | `pics_annexes_default_v3` | fail | not run | not run | not evaluated | n/a | n/a | n/a | not ready | page-number-only lineを除去できるまで正式化初手にしない |

## Findings

### meta_family_missing

旧 `runs/20260522-053004_text2ir-goal-gap-longrun` では全件で `meta_family_missing` が出ていた。今回の再生成では、CLIの `--family` により `meta.doc.family` が出力され、単体8文書の GOAL warning は0になった。

### tables and notes

旧 Phase 6 の代表9文書本体では table/note 件数が0だったが、現行mainでは次の文書で表・注記が出ている。

- `pics_pe00917_annex1_20230825`: table 6、row 35、note 16
- `pics_pe00917_annex2a_20230825`: table 1、row 6、note 4
- `pics_pe00917_part2_20230825`: table 1、row 7、note 1
- `who_lbm_3rd_2004_9241546506`: table 15、row 210、note 14

`possible_table` は全件0。正式候補化では、表セルと注記が実PDF/TXTに対応しているかをSAMPLE_COMPARISONで確認する。

### PIC/S Annexes refined

Annexes refined は現行mainの `--strict` で失敗した。検出内容:

```text
qualitycheck: ann20.sec7_2.ii.si14:text: page-number-only line remains
```

これは `docs/NORMALIZATION_PLAN_10_12_13.md` の「Annexes refinedは正式昇格の最初の候補にしない」という判断と整合する。

## Recommended next run

次の1runは、`eu_gmp_vol4_chap1_20130131` の正規化RUNにする。理由:

- strict / GOAL / promotion GOAL がpass。
- warningなし。
- 表・注記がなく、レビュー負荷が小さい。
- 過去計画でも最初の正式化候補に位置づけられている。

その次は `pics_pe00917_annex11_20230825`。Annex 1 と WHO はreadyだが、表・注記または対象範囲のレビューを挟む。
