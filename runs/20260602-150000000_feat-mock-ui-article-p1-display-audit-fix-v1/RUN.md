# RUN: mock-ui article paragraph1 display audit/fix

## Task
- 起点ブランチ: `feat/mock-ui-article-p1-display-only-v1`
- 新ブランチ: `feat/mock-ui-article-p1-display-audit-fix-v1`
- 指定メモ: `out/administrators-memos/20260602第一条第一項統合表示/20260602最大の難関、第一条第一項問題のバグ改修.txt`

## Problem Statement
- 「各条第一項の統合表示」は、第一項を条へデータ上統合する機能ではない。
- IR の `article -> paragraph -> item -> subitem` 関係を維持したまま、表示上だけ `第一条　<第一項本文>` と見せる例外措置である。
- 親 item が未選択で、その子または孫だけが選択された場合でも、必要な親文脈は落としてはいけない。

## Current Code Audit

### IR/Index
- `src/qai_mock_ui/ir_model.py` の `build_doc_index()` は raw IR を `Node` ツリーに変換するだけで、第一項と条を結合していない。
- `DocIndex.ancestors_of()` は `parent_nid` をたどるため、IR 側の親子関係が維持されていれば論理祖先も維持される。

### Profile
- 対象正本 profile:
  - `data/normalized/jp_egov_336M50000100002_20260501_507M60000100117/jp_egov_336M50000100002_20260501_507M60000100117.regdoc_profile.yaml`
- `dq_gmp_checklist.context_display_policy` は `subitem` / `item` / `paragraph` / `statement` で、選択ノードの祖先本文（例: 第一項本文、親の号本文）を表示する設定になっている。
- 正本 profile には `force_article_p1_text` は存在しない。

### Renderer
- `src/qai_mock_ui/render.py` は `_SelectionPlan` 内で以下を分けている。
  - `dedup_header_lines_full`: 省略判定用の論理ヘッダ
  - `dedup_context_lines_full`: prefix 省略用の論理文脈
  - `header_lines_full` / `item_lines`: 最終表示行
- `egov_merge_article_p1=True` の表示例外は `_apply_line_templates_split()` に閉じている。
- 現コードは IR ノードを直接変更していないが、表示テンプレート適用後に header/item へ再配分するため、省略判定・親文脈表示との干渉点がこの関数に集中している。

### App Layer
- `apps/mock_gmp_checklist_ui.py` の `_normalize_effective_purpose()` は、カスタム profile やセッションに残った旧設定から `force_article_p1_text` を消し、`subitem` / `item` / `paragraph` / `statement` では祖先本文を表示する設定に戻す。
- これは旧ゴミの再混入を防ぐ保護として機能するが、レンダラ外で表示仕様を補正しているため、仕様境界としては明文化が必要。

## Confirmed by Test
- `python -m pytest tests/test_mock_ui_render.py tests/test_mock_ui_yaml_folder_source.py -q`
- Initial result: `31 passed`
- After audit/spec tests and nid-based dedup fix: `34 passed`

## Initial Assessment
- 現時点のコードは「データ構造を崩して第一項を条へ統合する」実装ではない。
- ただし、第一項統合の表示例外が、レンダリング途中の header/item 分配と dedup 文脈にまたがっている。
- そのため、個別ケースを直すたびに別ケースへ副作用が出やすい構造になっている。

## Specification Questions
1. 第一項統合 ON のとき、第一項自身が選択された表示は次で確定か: **YES**
   - heading: `（薬局の構造設備）`
   - item/body: `第一条　薬局の構造設備の基準は、次のとおりとする。`
   - `第一条` 単独行と `１　...` 行は出さない。
   - 注意: あくまで表示上の例外。条と項をデータ上統合する意図ではない。
2. 第一項配下の item/subitem が選択されたとき、第一項は「祖先文脈」として `第一条　<第一項本文>` で出す、で確定か。 **YES**
   - 第一項統合 ON/OFF により表示形だけが変わる。
3. 第一項統合 ON でも、第二項・第三項など第一項以外の paragraph は `２　...` / `３　...` として表示し、条ラベルとは統合しない、で確定か。 **YES**
   - 日本国内法の第一項だけの例外。
4. 親 item 未選択・子 subitem 選択の場合、親 item は必ず文脈として表示する、で確定か。 **YES as default**
   - ただし profile YAML/JSON の明示設定があれば、それが優先される可能性がある。
   - 現在の正本 profile では「条までの祖先経路を含める」「祖先本文を出す」設定なので、親 item は祖先文脈として表示される。
   - 現コードの祖先停止設定は「その種類の祖先までの経路を含める」であり、途中の親 item だけを飛ばす設定ではない。
   - 祖先本文を出さない設定にすると、親 item だけでなく第一項本文など祖先本文全体が抑制される。
   - ただし祖先見出しを出す設定なら、条の heading などは残る。
5. 共通先祖省略では、直前ブロックの選択本文まで含めて prefix 比較するのか、それとも ancestor header のみを比較するのか。
   - 現コードは prefix モードで `dedup_context_lines_full = header + item` を前回文脈として使っている。
6. 兄弟 subitem を複数選択した場合、親 item は最初だけ表示し、2件目以降は省略する、で確定か。 **設定次第**
   - ユーザー回答: NO寄り、一部YES。兄弟省略/子孫省略の設定次第。

## Spec Sources Found
- `docs/specs/table_display_requirements.md`
  - 選択ノードの親・先祖を表示し、文脈を失わないことが背景として明記されている。
  - 子孫表示は `regdoc_profile` の宣言的設定で制御する、と明記されている。
- `docs/specs/notes_display_requirements.md`
  - 選択ノードの注書きなど子孫表示を profile で制御する、と明記されている。
- `runs/20260602-092803441_feat-mock-ui-table-row-context-v1/MOCK_UI_ISSUE_EXAMPLES.md`
  - 「どの祖先・子孫・見出しを出すか」は表示プロファイル YAML 化の課題として整理されている。
- `data/mock_ui/display_examples.yaml`
  - UI表示例で `dedup_mode_label: "共通先祖省略"` / `"兄弟のみ先祖省略"` を指定している。
- `apps/mock_gmp_checklist_ui.py`
  - `"共通先祖省略"` -> renderer `header_dedup_mode="prefix"`
  - `"兄弟のみ先祖省略"` -> renderer `header_dedup_mode="exact"`
- `src/qai_mock_ui/render.py`
  - `exact`: 直前ブロックと現在ブロックのヘッダ列が完全一致した場合だけ省略。
  - `prefix`: 直前ブロックの `header + item` を文脈として、現在ヘッダの共通 prefix を省略。

## Spec Source Gap
- 「兄弟のみ先祖省略」の人間向け仕様を1枚で明確に書いた docs は未発見。
- 実仕様は現状、UIラベル・表示例・renderer実装・テストに分散している。
- 今回の修正では、この分散仕様をテストで固定し、RUNに明記する。

## Ambiguity Inventory
仕様の揺らぎは、少なくとも以下の8系統に分散している。

1. `docs/NORMALIZED_RUN_OUTPUT_4FILES_GUIDE.md`
   - profile key の一覧と子孫表示設定の例はある。
   - 「祖先見出し」と「祖先本文」の相互作用は説明不足。
2. `docs/specs/table_display_requirements.md`
   - 「親・先祖を表示し、文脈を失わない」は明記。
   - どの省略モードでどこまで省略するかは未記載。
3. `docs/specs/notes_display_requirements.md`
   - 子孫表示は `include_descendants*` で制御すると明記。
   - 兄弟/祖先省略とは別レイヤー。
4. `runs/20260602-092803441_feat-mock-ui-table-row-context-v1/MOCK_UI_ISSUE_EXAMPLES.md`
   - 「どの祖先・子孫・見出しを出すか」は YAML 化課題と記載。
   - つまり仕様がまだ運用形で固まりきっていないことを示す。
5. `data/mock_ui/display_examples.yaml`
   - 表示例ごとに `共通先祖省略` / `兄弟のみ先祖省略` と第一項統合 ON/OFF を持つ。
   - 表示例は仕様例だが、仕様文そのものではない。
6. `data/mock_ui/profiles/*.yaml`
   - `context_display_policy` が祖先・子孫表示の実設定。
   - `example2_candidate_visibility_default.yaml` と `table_row_context_default.yaml` で table_row の止め方が違う。
7. `apps/mock_gmp_checklist_ui.py`
   - UIラベルを renderer mode に変換している。
   - `共通先祖省略` -> `prefix`、`兄弟のみ先祖省略` -> `exact`。
8. `src/qai_mock_ui/render.py` / `tests/test_mock_ui_render.py`
   - 実際の省略意味はここにある。
   - `exact`: 前回ヘッダ列と完全一致したときだけ省略。
   - `prefix`: 前回の `header + item` を文脈として、現在ヘッダの共通 prefix を省略。

## Internal Name Translation
以下はCodex実装上の内部名であり、ユーザーが提示した仕様語ではない。仕様確認では左列ではなく右列の意味で扱う。

| 内部名 | 画面上の意味 |
| --- | --- |
| `include_headings` | 祖先ノードの見出し文を出す。例: `（薬局の構造設備）` |
| `include_chapeau_text` | 祖先ノードの本文・番号付き本文を出す。例: `第一条`、`１　...`、`十　...` |
| `include_ancestors_until_kind(s)` | どの種類の祖先まで経路に含めるか。途中の親だけを個別に飛ばす設定ではない |
| `include_descendants*` | 選択ノードまたは祖先ノードの子孫を追加表示する。主に note/注記向け |
| `header_dedup_mode=exact` | 直前ブロックと祖先表示が完全一致したときだけ祖先表示を省略する。UI名は「兄弟のみ先祖省略」 |
| `header_dedup_mode=prefix` | 直前ブロックの文脈を使い、現在ブロックの先頭から共通する祖先表示を省略する。UI名は「共通先祖省略」 |
| `egov_merge_article_p1` | e-Gov国内法の第一項だけ、表示上 `第一条　<第一項本文>` にする |

## Confirmed Human Specification

### Display Targets
- データ上の親子関係は絶対に崩さない。
- 親・先祖文脈は原則表示する。
- 祖先のどこまでを文脈として出すかは、原則として表示設定で指定された上限まで全部出す。
- 祖先の見出しは原則出す。
  - ただし法令・profileごとの表示設定で出さない指定ができるなら、その明示設定を優先する。
- 祖先の本文は原則出す。
  - 文脈理解に必要なため。
  - ただし法令・profileごとの表示設定で出さない指定がある場合は、その明示設定を優先する。
- 選択ノードの子孫（note/注記など）を追加で出すかは設定で決められるようにする。
- 祖先の見出し・祖先の本文・子孫注記は、それぞれ別の表示対象として扱う。
- note/注記は位置としては子孫方向にあるが、表示上は footer 的な文脈であり、重複省略の対象になり得る。

### Omission Modes
- 省略モードは、表示対象を決めた後に、連続表示時の重複をどこまで畳むかの話である。
- 「兄弟のみ先祖省略」
  - 例: `十` の下の `ロ` と `ハ` を連続選択したら、2件目では `十` などを繰り返さない。
  - これは `ロ` と `ハ` が兄弟だから。
  - それ以外は一切省略しない。
- 「共通先祖省略」
  - 連続表示時に、直前の表示文脈と今回の表示文脈で共通する先祖を省略する。
  - 兄弟方向だけでなく、親から子・子孫へ続く流れでも共通文脈を省略できる。

### Article Paragraph 1 Merge
- 第一項統合表示は、国内法の第一項だけの表示例外。
- データ構造は `article -> paragraph -> item -> subitem` のまま維持する。
- 第一項統合は最後の見た目だけの変換であり、省略判定や親子関係判定に使ってはいけない。
- これは死守する。

### Implementation Direction
- 省略判定は表示文字列ではなく、論理ノード列（nid/path）で行う。
- 第一項統合後の `第一条　<第一項本文>` のような表示文字列を、省略判定の比較キーにしない。
- 表示対象の抽出、重複省略、最終表示変換を分ける。

## Implementation Done
- `_SelectionPlan` に省略判定用の論理 nid 列を追加した。
  - `dedup_header_nids_full`
  - `dedup_context_nids_full`
- `_apply_header_dedup()` を、表示文字列ではなく nid 列で比較できるようにした。
- 「共通先祖省略」は、直前の `header + item` に対応する nid 列と、今回の header nid 列の共通 prefix で省略する。
- 「兄弟のみ先祖省略」は、直前選択ノードと今回選択ノードの親 nid が同じ場合だけ省略する。
  - 親→子、子→親、従兄弟などでは省略しない。
- デバッグトレースにも比較対象 nid を出すようにした。

## Regression Tests Added
- art1.p1 配下の全 subitem について、親 item 未選択でも親 item が文脈に残ることを確認。
- 祖先本文を出さない設定では、親 item 本文や第一項本文は消えるが、祖先見出しは設定に従って残ることを確認。
- 「兄弟のみ先祖省略」では、親→子の連続選択で文脈を省略しないことを確認。

## Manual Check Result
- User checked `MANUAL_CHECKLIST.md` on `http://localhost:8502`.
- Overall result: 概ね良好。
- Checklist defect found:
  - ケース8（兄弟のみ先祖省略では別親を省略しない）で、親 item `十` / `十二` だけでなく、`（薬局の構造設備）` と `第一条　薬局の構造設備の基準は、次のとおりとする。` も出ることを期待に明記していなかった。
  - This was a checklist expectation gap, not a code failure.
- `MANUAL_CHECKLIST.md` was updated to reflect this expected context display.

## Next Plan
1. art1 配下の item/subitem 全体で、親未選択・孫選択時に親 item が落ちないことを網羅テスト化する。
2. 第一項統合の表示例外を「論理 plan は不変、表示化だけ別関数」に寄せ、dedup 用配列に表示済み文字列が混ざらないように整理する。
3. `_normalize_effective_purpose()` のような app 層補正が必要な範囲を最小化し、仕様として必要なものだけ残す。
