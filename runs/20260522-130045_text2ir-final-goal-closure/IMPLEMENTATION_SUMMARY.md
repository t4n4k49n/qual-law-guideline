# IMPLEMENTATION_SUMMARY

## Phase 9A

`meta.doc.family` を正式候補で欠落させないため、text2irのmeta出力とGOAL_CHECKを強化した。

変更点:

- `--family` 指定時に `meta.doc.family` へ反映。
- `--family` 未指定時は `parser_profile.applies_to.family` から補完。
- `goal_check --mode promotion` / `--mode release` では family 欠落をerror化。
- `has_markers` 判定を `marker_types` 対応に修正。

検証:

- `tests/test_text2ir_goal_check.py`: `8 passed`

未実施:

- Phase 9B以降の表・注記反映、再生成、promotion candidate作成は後続フェーズで実施する。
