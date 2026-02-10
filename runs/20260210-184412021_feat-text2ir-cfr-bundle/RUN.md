# RUN: text2ir bundle（CFR txt -> 4 YAML）

- run_id: 20260210-184412021_feat-text2ir-cfr-bundle
- branch: feat/text2ir-cfr-bundle
- date: 2026-02-10 18:44:27 +09:00
- status: 実装完了（未コミット）

## 目的
- XML以外（txt）入力でも、`meta / parser_profile / regdoc_ir / regdoc_profile` の4 YAMLを同一 `doc_id` 軸で一括出力できるようにする。
- CFR向けの行頭prefixベース解析を導入し、`(a)(1)(i)` の複合prefixを木構造（paragraph -> item -> subitem）へ展開する。

## 実装概要
- 新規CLI `text2ir bundle` を追加（Typer）。
- 新規パッケージ `src/qai_text2ir/` を追加。
- CFR用 `parser_profile` をYAML外出しで同梱。
- txt行パーサをプロファイル駆動で実装（構造許可表で親決定、継続行連結、source_spans付与）。
- CFR向け `regdoc_profile` を実装（`include_ancestors_until_kind: section`）。
- `meta.yaml` はUS/txt向けに調整（`jurisdiction: US`, `language: en`, `cfr_title/cfr_part` 反映）。
- 出力後に `verify_document` で健全性検証するようにした。

## 変更ファイル
1. `pyproject.toml`
2. `src/qai_xml2ir/verify.py`
3. `src/qai_text2ir/__init__.py`
4. `src/qai_text2ir/cli.py`
5. `src/qai_text2ir/profile_loader.py`
6. `src/qai_text2ir/text_parser.py`
7. `src/qai_text2ir/profiles/us_cfr_default_v1.yaml`
8. `tests/fixtures/CFR_PART11_SubpartA.txt`
9. `tests/test_text2ir_bundle.py`

## テスト実行結果
- `python -m pytest -q tests/test_text2ir_bundle.py` -> 1 passed
- `python -m pytest -q tests/test_bundle_gmp.py tests/test_ir_structure.py tests/test_serialize_overwrite.py` -> 10 passed

## 補足
- `runs/20260210-184412021_feat-text2ir-cfr-bundle/` と `out/20260210-184412021_feat-text2ir-cfr-bundle/` を同名で作成済み。

