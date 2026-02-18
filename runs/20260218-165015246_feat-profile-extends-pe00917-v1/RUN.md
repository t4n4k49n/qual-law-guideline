# RUN: 20260218-165015246_feat-profile-extends-pe00917-v1

- run_id: `20260218-165015246_feat-profile-extends-pe00917-v1`
- branch: `feat/profile-extends-pe00917-v1`

## 目的
- parser_profile の extends 継承を導入し、PE 009-17 系プロファイルの重複前処理を共通化したうえで、既存 strict パイプライン互換を維持する。

## 実装
- `src/qai_text2ir/profile_loader.py`
  - `extends`（単一/複数）解決、deep merge、marker_types(id単位)マージ、循環参照検出を追加。
  - テスト用 `profiles_dir_override` を追加。
- `src/qai_text2ir/profiles/pics_pe00917_common_v1.yaml`
  - PE 009-17 共通前処理を集約するベースプロファイルを追加。
- PICS系各プロファイル
  - `extends: pics_pe00917_common_v1` を付与。
  - 共通 `drop/strip/merge/repeated` の重複を削減し、個別ロジックのみ保持。
- tests
  - `tests/test_profile_loader_extends.py` を追加。
  - `tests/test_pics_annex1_profile_v2.py` を継承解決ロードに更新。

## 実行
- `python -m pytest -q -p no:cacheprovider`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --out-dir out/20260218-165015246_feat-profile-extends-pe00917-v1 --doc-id pics_pe00917_annexes_20230825_refined_v3_extends --title "PIC/S GMP Guide (PE 009-17) Annexes (25 August 2023) [refined v3 + extends]" --short-title "PIC/S Annexes refined v3 extends" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/8881" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Annexes)" --parser-profile src/qai_text2ir/profiles/pics_annexes_default_v3.yaml --qualitycheck --strict --emit-only all`

## 確認結果
- テスト: `74 passed, 1 skipped`
- strict: 成功（終了コード0）
- PICS Annexes refined v3 の生成を extends 適用後も維持
- プロファイル重複を削減し、以後の横展開に必要な継承基盤を追加

## 生成物
- `out/20260218-165015246_feat-profile-extends-pe00917-v1/pics_pe00917_annexes_20230825_refined_v3_extends.regdoc_ir.yaml`
- `out/20260218-165015246_feat-profile-extends-pe00917-v1/pics_pe00917_annexes_20230825_refined_v3_extends.parser_profile.yaml`
- `out/20260218-165015246_feat-profile-extends-pe00917-v1/pics_pe00917_annexes_20230825_refined_v3_extends.regdoc_profile.yaml`
- `out/20260218-165015246_feat-profile-extends-pe00917-v1/pics_pe00917_annexes_20230825_refined_v3_extends.meta.yaml`
- `out/20260218-165015246_feat-profile-extends-pe00917-v1/manifest.yaml`
- `runs/20260218-165015246_feat-profile-extends-pe00917-v1/RUN.md`
