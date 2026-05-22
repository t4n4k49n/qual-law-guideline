# PROFILE_SAMPLE_COMPARISON

## 結論

Phase 9Cでは、前回RUNで「profile課題」として扱った代表課題を、fixtureベースのサンプル比較で確認した。確認対象はすべて期待構造を満たした。

## PIC/S Annex 15

確認対象:

- `tests/fixtures/pics_annex15_heading_continuation_fixture.txt`
- profile: `src/qai_text2ir/profiles/pics_annex15_default_v1.yaml`

期待:

- `ORGANISING AND PLANNING FOR QUALIFICATION AND VALIDATION` が1つのsection headingになる。
- `VALIDATION` が本文先頭に孤立しない。

結果:

- section `1` heading: `ORGANISING AND PLANNING FOR QUALIFICATION AND VALIDATION`
- section `1` text: `VALIDATION` で開始しない。
- 判定: 解消。

## PIC/S Annex 11

確認対象:

- `tests/fixtures/pics_annex11_profile_fixture.txt`
- profile: `src/qai_text2ir/profiles/pics_annex11_default_v1.yaml`

期待:

- `Risk Management` / `Validation` 等がsection headingへ入り、本文先頭へ吸収されない。

結果:

- section `4` heading: `Validation`
- section `4` text先頭に `Validation` は残らない。
- paragraph `4.1` は本文として分離。
- 判定: 解消。

## PIC/S Annex 2A

確認対象:

- `tests/fixtures/pics_annex2a_part_hierarchy_fixture.txt`
- profile: `src/qai_text2ir/profiles/pics_annex2a_default_v1.yaml`

期待:

- `Part A`, `Part B`, `B1` がchapter/section階層として扱われる。

結果:

- chapter `A` heading: `GENERAL GUIDANCE`
- chapter `B` heading: `SPECIFIC GUIDANCE ON SELECTED PRODUCT TYPES`
- section `B1` heading: `ANIMAL SOURCED PRODUCTS`
- 判定: 解消。

## PIC/S Part II

確認対象:

- `tests/fixtures/pics_part2_toc_intro_fixture.txt`
- profile: `src/qai_text2ir/profiles/pics_part2_default_v1.yaml`

期待:

- `Objective` / `Scope` / `Principles` 系のsection headingが本文へ吸収されない。

結果:

- chapter `1` heading: `INTRODUCTION`
- section `1.1` heading: `Objective`
- section `1.1` text先頭に `Objective` は残らない。
- 判定: 解消。

## WHO LBM 3rd

確認対象:

- `tests/test_text2ir_who_lbm_3rd.py`
- 前回RUN: `runs/20260522-053004_text2ir-goal-gap-longrun/WHO_LBM_CANDIDATE_GRANULARITY_REVIEW.md`

判断:

- WHO LBM 3rdは当面item粒度をDQ候補として許容する。
- 理由は、WHO LBMの本文構造が法令条文型より説明・手順型に近く、paragraph相当へ無理に寄せるより、source_spans付きのitem候補として扱う方が安全なため。
- paragraph化は、UI/レビューで粒度不足が実際に観測された後に検討する。

## Validation

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_pics_annex15_profile.py tests\test_pics_annex11_profile.py tests\test_pics_annex2a_profile.py tests\test_pics_part2_v1.py tests\test_text2ir_who_lbm_3rd.py
```

Result:

- `12 passed`
