## まとめ

NIID「病原体等安全管理規程」の別表・付表を本文Parserから分離し、欠落させずにIR上で追跡できる専用profileを追加しました。正式な正規化ではなく、後続の表列復元adapterへ進むための開発段階として、別表・付表の保持境界を明確化しています。

## 変更内容

- `jp_niid_pathogen_safety_management_annex_v1` profileを追加
- 別表1、付表1-1から付表4、別表2から別表10をroot直下の`annex`として保持
- 本文用profileの挙動を回帰テストで維持
- RUN記録、goal_check、special_structure_audit結果を追加

## 確認

- `.\.venv\Scripts\python.exe -m pytest tests\test_text2ir_niid_pathogen_annex.py tests\test_text2ir_niid_pathogen_safety.py tests\test_candidate_visibility_profiles_6_9.py -q`
- `.\.venv\Scripts\python.exe -m qai_text2ir.cli bundle --parser-profile-id jp_niid_pathogen_safety_management_annex_v1 --strict`
- `.\.venv\Scripts\python.exe -m qai_text2ir.goal_check --mode normal`
- `.\.venv\Scripts\python.exe -m qai_text2ir.special_structure_audit --mode normal`

## 注意

- 共通parser本体は変更していません。
- 列復元は未実施です。今回は別表・付表を欠落させず、source span付きで保持する段階です。
- `data/normalized/` への昇格は行っていません。

<!-- PR_BODY_FILE: runs/20260525-150333206_feat-niid-pathogen-annex-adapter-v1/PR.md -->
