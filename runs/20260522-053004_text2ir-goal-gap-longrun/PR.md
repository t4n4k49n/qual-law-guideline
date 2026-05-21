## まとめ

text2ir正規化GOAL到達に向けた長期RUNのPhase 4として、確認RUNでprofile変更対象としたPIC/S Annex 15、Annex 11、Annex 2A、Part IIの見出し・階層課題を修正します。あわせてWHO LBM 3rdのitem粒度候補をレビューし、当面のDQ候補粒度として許容できるかを記録します。

## 変更内容

- Annex 15の見出し継続profile設定を補強
- Annex 11とPart IIのsection見出し抽出を改善
- Annex 2AのB1階層markerを追加
- `PROFILE_FIX_REVIEW.md` を追加
- `WHO_LBM_CANDIDATE_GRANULARITY_REVIEW.md` を追加
- `RUN.md` にPhase 4の実装・検証結果を追記

## 確認

- `.\.venv\Scripts\python.exe -m pytest -q tests\test_pics_annex15_profile.py tests\test_pics_annex11_profile.py tests\test_pics_annex2a_profile.py tests\test_pics_part2_v1.py`
- `.\.venv\Scripts\python.exe -m pytest -q`
- 結果: `160 passed, 1 skipped`

<!-- PR_BODY_FILE: runs/20260522-053004_text2ir-goal-gap-longrun/PR.md -->
