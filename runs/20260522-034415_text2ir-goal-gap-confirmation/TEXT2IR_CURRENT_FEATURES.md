# TEXT2IR_CURRENT_FEATURES

## 結論

現行 `qai_text2ir` は、v4出力、4ファイル出力、manifest、profile provenance、source_spans、qualitycheck/strict、profile extends、subtree refine、table/note/descendant表示の基礎機能をすでに持つ。一方、代表文書の再生成では table/note 系ノードが出ておらず、実データでの到達確認は別課題として残る。

| 観点 | 現状 | 根拠 |
|---|---|---|
| schema v4対応 | 実装済み | 再生成9件すべて `qai.regdoc_ir.v4` |
| 4ファイル出力 | 実装済み | CLIが4 YAMLを出力、9件全件あり |
| meta / manifest | 実装済み | `src/qai_text2ir/cli.py`, 9件全件 `manifest.yaml` あり |
| parser profile provenance | 実装済み | `profile_loader.py`, manifestにprovenance記録 |
| source_spans | 実装済み | `text_parser.py`; 9件でroot以外ほぼ全ノードにline locatorあり |
| qualitycheck / strict | 実装済み | `cli.py`, `text_parser.py`; 9件全件strict exit 0 |
| profile extends / inheritance | 実装済み | `profile_loader.py`; PIC/S系profileでextends使用 |
| subtree refine / dispatch / fallback | 実装済み | `text_parser.py`; Annexes全体refinedで19 annexに適用 |
| table / table_row / table_header / table_note | 実装済みだが代表文書では未発火 | `text_parser.py`, `tests/test_markdown_table_parsing.py`; 今回9件はtable 0 |
| normal_note / footnote / preformatted | note/preformatted基礎あり、代表文書では未発火 | `text_parser.py`, note fixture tests; 今回9件はnote 0/preformatted 0 |
| context_display_policy ancestor / descendant | 実装済み | `context_display.py`, `qai_mock_ui/render.py`, tests |
| `selectable_kinds` に table_row | 実装済み | 再生成9件のregdoc_profileで `table_row` を含む |
| markdown table fixture / note fixture | テストあり | `tests/test_markdown_table_parsing.py`, `tests/test_normal_note_descendants.py` |

## 注意点

- 実装済み機能と、各代表文書の正式化品質は別に評価する必要がある。
- 現行の代表文書入力はプレーンテキストであり、PDF中の表や注記がMarkdown table/noteとして入力に残っていない場合、共通parserだけではtable/noteノード化されない。
