## まとめ

text2irの最終GOAL到達に向けて、前回RUNでprofile課題として扱った項目をサンプル比較で閉じます。修正済みの前提にせず、Annex 15 / Annex 11 / Annex 2A / Part II / WHO LBM 3rdを確認対象として記録します。

## 変更内容

- `PROFILE_SAMPLE_COMPARISON.md` を追加
- Annex 15の見出し継続を確認
- Annex 11のsection heading/text分離を確認
- Annex 2AのPart A/B/B1階層を確認
- Part IIのsection heading/text分離を確認
- WHO LBM 3rdのitem粒度許容判断を記録

## 確認

```powershell
.\.venv\Scripts\python.exe -m pytest -q tests\test_pics_annex15_profile.py tests\test_pics_annex11_profile.py tests\test_pics_annex2a_profile.py tests\test_pics_part2_v1.py tests\test_text2ir_who_lbm_3rd.py
```

結果: `12 passed`

`data/normalized/` は変更していません。

<!-- PR_BODY_FILE: runs/20260522-130045_text2ir-final-goal-closure/PR.md -->
