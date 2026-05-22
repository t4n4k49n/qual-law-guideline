# PROMOTION_CANDIDATE_REVIEW

## 結論

Phase 7で review candidate を作成した。これは正式昇格ではなく、人間レビュー用の候補である。`data/normalized/` へのコピーは行っていない。

## 作成したreview candidate

| 優先 | 文書 | doc_id | 候補パス | 状態 |
|---:|---|---|---|---|
| 1 | EU GMP Vol.4 Chapter 1 | `eu_gmp_vol4_chap1_20130131` | `runs/20260522-053004_text2ir-goal-gap-longrun/review_candidate/eu_gmp_vol4_chap1_20130131/` | 作成済み |
| 2 | PIC/S PE 009-17 Annex 15 | `pics_pe00917_annex15_20230825` | `runs/20260522-053004_text2ir-goal-gap-longrun/review_candidate/pics_pe00917_annex15_20230825/` | 作成済み |
| 3 | PIC/S Annex 11 | `pics_pe00917_annex11_20230825` | `runs/20260522-053004_text2ir-goal-gap-longrun/review_candidate/pics_pe00917_annex11_20230825/` | 作成済み |

## 各候補に含めたファイル

- `<doc_id>.regdoc_ir.yaml`
- `<doc_id>.parser_profile.yaml`
- `<doc_id>.regdoc_profile.yaml`
- `<doc_id>.meta.yaml`
- `manifest.yaml`
- `GOAL_CHECK_RESULT.md`
- `SAMPLE_COMPARISON.md`
- `QUALITYCHECK_RESULT.md`

## レビュー観点

- `SAMPLE_COMPARISON.md` の代表ノードが人間可読経路として妥当か。
- `nid` と階層パスが対応しているか。
- `source_spans` が監査説明に足りるか。
- EU GMP Chapter 1を最初の正式昇格対象としてよいか。
- Annex 15 / Annex 11を続く候補として扱ってよいか。

## 次の候補

Phase 7時点では、長期指示書で指定された3候補を作成済み。次の判断は、review candidateをpromotion candidateへ進めるか、追加の文書候補を作るかである。

## 作成時の条件

- `runs/<run_id>/review_candidate/<doc_id>/` に4ファイル、manifest、GOAL_CHECK_RESULT、SAMPLE_COMPARISON、QUALITYCHECK_RESULTを置く。実施済み。
- `data/normalized/` へは承認前にコピーしない。
