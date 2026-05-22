# PROMOTION_CANDIDATE_REVIEW: EU GMP Chapter 1

## Conclusion

- EU GMP Chapter 1 は最初の promotion candidate として妥当。
- `data/normalized/` へのコピーは実施していない。
- 人間レビュー後に、正規化RUNの子PRで正式昇格する前提。

## Candidate Files

- `eu_gmp_vol4_chap1_20130131.regdoc_ir.yaml`
- `eu_gmp_vol4_chap1_20130131.parser_profile.yaml`
- `eu_gmp_vol4_chap1_20130131.regdoc_profile.yaml`
- `eu_gmp_vol4_chap1_20130131.meta.yaml`
- `manifest.yaml`
- `GOAL_CHECK_RESULT.md`
- `goal_check_result.json`
- `SAMPLE_COMPARISON.md`

## GOAL Check

- status: PASS
- schema: `qai.regdoc_ir.v4`
- nodes: 72
- source span coverage: 1.0
- family: `EU_GMP`
- errors: 0
- warnings: 0

## Review Points

- paragraph 1.4 / 1.8 / 1.10 / 1.13 のitem粒度がDQチェック候補として過不足ないか。
- ancestor/descendant表示でChapter 1配下の文脈が十分か。
- EU GMP Chapter 1を最初の正式昇格対象として進めてよいか。

## Non-goals

- このPhaseでは `data/normalized/` を変更しない。
- 表・注記が複雑なPIC/S Annex 1やWHO LBMは、このpromotion candidateには含めない。
