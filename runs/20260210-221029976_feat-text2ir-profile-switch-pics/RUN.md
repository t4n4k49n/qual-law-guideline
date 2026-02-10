# RUN: text2ir profile切替対応とPIC/S txt対応拡張

- run_id: 20260210-221029976_feat-text2ir-profile-switch-pics
- branch: feat/text2ir-profile-switch-pics
- date: 2026-02-10 22:10:42 +09:00
- status: 実装・テスト完了（未コミット）

## 目的
- `text2ir bundle` を CFR固定から拡張し、プロファイル差し替えで PIC/S 等の別フォーマットtxtでも4 YAMLを生成できるようにする。

## 実装内容
1. `profile_loader` 拡張
- `load_parser_profile(profile_id=None, path=None)` を追加
- 解決優先度: `path > profile_id > us_cfr_default_v1`

2. `cli.py` 拡張
- 追加オプション:
  - `--parser-profile` / `--parser-profile-id`
  - `--regdoc-profile` / `--context-root-kind`
  - `--jurisdiction` / `--language`
- 互換維持:
  - 未指定時は CFR既定プロファイルで従来どおり動作
- メタ拡張:
  - `doc.jurisdiction` / `doc.language` / `sources.label` をプロファイルまたはCLIから解決
  - `source_url` 未指定でも出力可能（既存挙動維持）

3. `text_parser.py` 最小拡張
- `num` 抽出のフォールバック追加
  - `num_group` 指定 > `num` グループ > 最初の非空グループ
- `structural_kinds` を parser_profile から受ける仕様に変更
  - role/normativity と heading/text の扱いに反映
- 親未発見時の marker は root フォールバックでぶら下げる

4. PIC/S parser_profile 追加
- `src/qai_text2ir/profiles/pics_part1_default_v1.yaml`
- `src/qai_text2ir/profiles/pics_annex1_default_v1.yaml`
- 既存 `us_cfr_default_v1.yaml` に `structural_kinds` 等の拡張キーを追加

5. テスト/fixture 追加
- `tests/fixtures/PICS_PE_009-17_PART-I_CHAPTER-5-9_formatted.txt`
- `tests/fixtures/PICS_PE_009-17_ANNEX-1.txt`
- `tests/test_text2ir_profiles_pics.py`

## 実行コマンドと結果
```powershell
python -m pytest -q tests/test_text2ir_bundle.py tests/test_text2ir_profiles_pics.py
# 3 passed

python -m pytest -q tests/test_bundle_gmp.py tests/test_ir_structure.py tests/test_serialize_overwrite.py
# 10 passed

python -m pytest -q
# 15 passed, 1 skipped
```

## プロファイル × fixture 確認
- `pics_part1_default_v1` + `PICS_PE_009-17_PART-I_CHAPTER-5-9_formatted.txt`: pass
- `pics_annex1_default_v1` + `PICS_PE_009-17_ANNEX-1.txt`: pass
- `us_cfr_default_v1`（未指定既定）+ `CFR_PART11_SubpartA.txt`: pass

## 変更ファイル
- `src/qai_text2ir/cli.py`
- `src/qai_text2ir/profile_loader.py`
- `src/qai_text2ir/text_parser.py`
- `src/qai_text2ir/profiles/us_cfr_default_v1.yaml`
- `src/qai_text2ir/profiles/pics_part1_default_v1.yaml`
- `src/qai_text2ir/profiles/pics_annex1_default_v1.yaml`
- `tests/fixtures/PICS_PE_009-17_PART-I_CHAPTER-5-9_formatted.txt`
- `tests/fixtures/PICS_PE_009-17_ANNEX-1.txt`
- `tests/test_text2ir_profiles_pics.py`

