# BASELINE

## ベースラインテスト

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

結果:

```text
148 passed, 1 skipped
```

## 現行text2ir機能確認

| 観点 | 現行実装 | 主な根拠 |
|---|---|---|
| `qai.regdoc_ir.v4` 出力 | 実装済み | `src/qai_xml2ir/models_ir.py`, text2ir再生成結果 |
| 4ファイル出力 | 実装済み | `src/qai_text2ir/cli.py` |
| manifest出力 | 実装済み | `src/qai_text2ir/cli.py` |
| qualitycheck/strict | 実装済み | `src/qai_text2ir/cli.py`, `src/qai_text2ir/text_parser.py` |
| source_spans | 実装済み | `src/qai_text2ir/text_parser.py` |
| table構造化 | Markdown tableは実装済み | `src/qai_text2ir/text_parser.py`, `tests/test_markdown_table_parsing.py` |
| note/descendant表示 | 実装済み | `src/qai_text2ir/context_display.py`, `tests/test_normal_note_descendants.py` |
| profile extends | 実装済み | `src/qai_text2ir/profile_loader.py` |
| subtree refine/dispatch/fallback | 実装済み | `src/qai_text2ir/text_parser.py`, `src/qai_text2ir/profiles/pics_annexes_default_v3.yaml` |

## 確認RUNから引き継ぐベースライン

- 代表9文書は `--qualitycheck --strict` exit 0。
- 代表9文書は `qai_xml2ir.verify.verify_document` pass。
- 代表9文書はv4、4ファイル、manifest、source_spansの基礎GOALを満たす。
- 代表9文書では `table`, `table_row`, `note`, `preformatted` が0件で、実データ由来の表・注記確認が未了。
- CFR Part 11 / Part 211 は現行repo内に代表入力がない。

## Phase 0結論

修正前のテスト状態は良好。Phase 1では、strict成功に加えてv4、4ファイル、manifest、source_spans、nid/ord、`dq_gmp_checklist` を一括確認できるGOAL検証ハーネスを追加する。
