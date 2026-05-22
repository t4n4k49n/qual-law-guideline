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

## Phase 9B

表・注記の本番入力適用に着手した。

変更点:

- `qai_text2ir.table_note_inventory` を追加。
- 固定幅表のcaption検出を拡張。
- 安全な固定幅表は `table/table_header/table_row` 化。
- 不安定な固定幅表は `preformatted possible_table` として保持。
- table直後のnoteを保持。
- Annex 1 / WHO LBM / Annex 2A / Part II / Part I / Annexes refined profileで表・注記検出を有効化。
- skip block処理の行index上書きバグを修正。

検証:

- related tests: `20 passed`
- Annex 1 full input smoke: strict exit 0、`preformatted=4`、`note=9`

## Phase 9C

profile課題をサンプル比較で確認した。

確認結果:

- Annex 15: 見出し継続は解消。
- Annex 11: section heading/text分離は解消。
- Annex 2A: Part A/B/B1階層は解消。
- Part II: section heading/text分離は解消。
- WHO LBM 3rd: item粒度を当面DQ候補として許容。

検証:

- profile関連テスト: `12 passed`
