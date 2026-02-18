# RUN: 20260218-172825019_feat-pics-trace-provenance-v1

- run_id: `20260218-172825019_feat-pics-trace-provenance-v1`
- branch: `feat/pics-trace-provenance-v1`

## 目的
- parser_profile 継承元の provenance と refine_subtrees の適用結果を、manifest と regdoc_ir ノードタグに追跡可能な形で残す。

## 実装
- `src/qai_text2ir/profile_loader.py`
  - `load_parser_profile_with_provenance()` を追加。
  - extends 解決時に profile ごとの `profile_id/internal_id/path/sha256/extends` を収集。
  - `load_parser_profile()` は互換のまま新API経由で解決。
- `src/qai_text2ir/text_parser.py`
  - refine 成功時に annex ノード tags へ `refined_by` / `refine_kind` / `refine_key` を付与。
  - subprofile ロードへ `profiles_dir_override` を伝播可能化（テスト容易化）。
- `src/qai_text2ir/cli.py`
  - `--write-manifest/--no-write-manifest`（既定: true）追加。
  - `--overwrite-manifest`（既定: false）追加。
  - manifest 自動出力（プロンプトなし）を実装。
  - manifest に parser profile provenance / qualitycheck概要 / refine適用サマリを記録。
- `tests/test_trace_provenance.py`
  - extends chain の provenance 収集を検証。
  - dispatch/fallback refine のタグ付与を検証。

## 実行
- `python -m pytest -q -p no:cacheprovider`
- `python -m qai_text2ir.cli --input data/human-readable/pics/pe009-17_annexes_2023-08-25_en.txt --out-dir out/20260218-172825019_feat-pics-trace-provenance-v1 --doc-id pics_pe00917_annexes_20230825_refined_v3_extends_trace --title "PIC/S PE 009-17 Annexes (25 August 2023) refined v3 extends + trace" --short-title "PICS Annexes trace" --jurisdiction INTL --family PICS --language en --doc-type guideline --source-url "https://picscheme.org/docview/8881" --source-format pdf --retrieved-at "2026-02-18" --pics-doc-id "PE 009-17 (Annexes)" --parser-profile src/qai_text2ir/profiles/pics_annexes_default_v3.yaml --qualitycheck --strict --write-manifest --emit-only all`

## 確認結果
- テスト: `76 passed, 1 skipped`
- strict: 成功（warnings 0）
- `manifest.yaml` に `parser_profile.provenance` と `refine.applied` を記録
- `regdoc_ir` の annex ノードに `refined_by=...`, `refine_kind=annex`, `refine_key=...` を記録

## 生成物
- `out/20260218-172825019_feat-pics-trace-provenance-v1/pics_pe00917_annexes_20230825_refined_v3_extends_trace.regdoc_ir.yaml`
- `out/20260218-172825019_feat-pics-trace-provenance-v1/pics_pe00917_annexes_20230825_refined_v3_extends_trace.parser_profile.yaml`
- `out/20260218-172825019_feat-pics-trace-provenance-v1/pics_pe00917_annexes_20230825_refined_v3_extends_trace.regdoc_profile.yaml`
- `out/20260218-172825019_feat-pics-trace-provenance-v1/pics_pe00917_annexes_20230825_refined_v3_extends_trace.meta.yaml`
- `out/20260218-172825019_feat-pics-trace-provenance-v1/manifest.yaml`
- `runs/20260218-172825019_feat-pics-trace-provenance-v1/RUN.md`
