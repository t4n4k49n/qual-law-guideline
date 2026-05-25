# RUN: 20260525-144814194_feat-candidate-visibility-profiles-6-9

## 目的

6/7/8/9の個別開発計画フェーズAとして、対象外OK範囲をParserではなくcandidate visibilityで制御できるようにする。

このRUNはParser開発の後続部品開発であり、正式な正規化RUNではない。`data/normalized/` への昇格や、正規化承認を前提にしない。

## 対象

- `src/qai_text2ir/candidate_visibility_profiles.py`
- `src/qai_text2ir/candidate_visibility_profiles/*.yaml`
- `src/qai_text2ir/cli.py`
- `tests/test_candidate_visibility_profiles_6_9.py`
- `docs/INDIVIDUAL_ADAPTER_PLAN_6_9.md`
- `docs/NORMALIZED_RUN_OUTPUT_4FILES_GUIDE.md`

## 実施内容

- candidate visibility profileのロード・適用部品を追加した。
  - `load_candidate_visibility_profile`
  - `apply_candidate_visibility_profile`
- `text2ir bundle` に候補表示profile指定オプションを追加した。
  - `--candidate-visibility-profile-id`
  - `--candidate-visibility-profile`
- 6/7/8/9向けの文書別candidate visibility profileを追加した。
  - `jp_pmda_api_gmp_guideline_visibility_v1`
  - `jp_pmda_aseptic_processing_guideline_visibility_v1`
  - `jp_niid_pathogen_safety_management_visibility_v1`
  - `jp_mhlw_csv_guideline_visibility_v1`
- profile適用と既存mock-ui candidate visibilityロジックの結合をテストした。
- 計画文書と4ファイルガイドに、candidate visibility profileの配置・適用方法を追記した。

## 個別と共通の整理

- 共通に入れたもの:
  - candidate visibility profileをregdoc_profileへ適用する汎用部品。
  - `text2ir bundle` からprofileを指定するCLIオプション。
- 個別profileに閉じたもの:
  - 対象外OKの具体的なNID範囲。
  - 用語集、表1、序論、定義、第5章、第6章などの文書別判断。
- Parser profileには対象外OK範囲を入れていない。IRには残し、候補表示だけを制御する。

## 検証

```powershell
.venv\Scripts\python.exe -m pytest tests\test_candidate_visibility_profiles_6_9.py -q
```

結果: `6 passed`

```powershell
.venv\Scripts\python.exe -m pytest tests\test_candidate_visibility_profiles_6_9.py tests\test_mock_ui_candidate_visibility.py tests\test_text2ir_bundle.py tests\test_text2ir_csv_guideline.py tests\test_text2ir_aseptic_processing_guideline.py tests\test_text2ir_api_gmp_guideline.py tests\test_text2ir_niid_pathogen_safety.py tests\test_text2ir_goal_check.py -q
```

結果: `26 passed`

```powershell
.venv\Scripts\python.exe -m pytest tests\test_candidate_visibility_profiles_6_9.py tests\test_mock_ui_candidate_visibility.py tests\test_text2ir_bundle.py -q
```

結果: `9 passed`

## 残課題

- 対象外OK範囲の最終妥当性は、正規化候補レビュー時に確認する。
- 8b別表・付表、6表1、7固定幅表候補、9別紙は次フェーズ以降の個別adapter対象とする。
