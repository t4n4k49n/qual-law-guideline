# 旧e-Gov正規化の再正規化準備

## まとめ

旧e-Gov正規化を「公式e-Gov XMLから現行IR基準で再生成する」タスクとして定義し、対象5件の入力XMLとtrial candidateを揃えました。これにより、次の正規化RUNでは旧YAMLの救済移行ではなく、入力正本から再現可能な形で `data/normalized` を更新できます。

## 変更内容

- e-Gov公式APIから対象5件のXMLを取得し、入力正本として追加
- `xml2ir` 共通部で巨大XMLテキストノードを読めるよう `huge_tree=True` を共通化
- e-Gov個別部でAPI v1ラッパの `LawFullText/Law` から法令本文・法令番号を読むよう修正
- `trial_candidates_r4` に5件の再生成候補を作成

## 検証

- `uv run python tools/check_ir_structure.py runs/20260602-005222271_egov-renormalization-prep/trial_candidates_r4`
  - `[OK] no structure problems found (scanned: 20 yaml files)`
- `uv run python -m pytest -q tests/test_xml_common.py tests/test_egov_api_wrapper.py tests/test_egov_article_structure.py tests/test_egov_table_spans.py tests/test_egov_table_payload_header_inference.py tests/test_xml2ir_no_fold_article.py tests/test_xml2ir_profiles_table_context.py tests/test_ecfr_parser.py`
  - `17 passed`

## 正規化RUNへの引き継ぎ

次の正規化RUNでは、この準備RUNの `trial_candidates_r4` と同じ入力XML・同じ生成方針で `promotion_candidate/` を作成します。`ARCHIVE_jp_egov_*` は正式昇格対象外として維持します。

<!-- PR_BODY_FILE: runs/20260602-005222271_egov-renormalization-prep/PR.md -->
