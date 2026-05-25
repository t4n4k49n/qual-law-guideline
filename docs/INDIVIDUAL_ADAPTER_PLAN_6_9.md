# 6/7/8/9 個別adapter開発計画

## 位置づけ

この文書は `docs/NORMALIZATION_PLAN_6_9.md` のParser開発後に見えた、文書別のadapter・個別部品候補を整理する。

現時点の成果はParser開発であり、正式な正規化RUN承認ではない。`data/normalized/` への昇格判断や候補表示の最終判断とは分けて扱う。

## 共通化の判断基準

共通parser/profileへ入れてよいもの:

- 文書名、通知番号、特定表題に依存しない。
- 少なくとも複数文書で同じ構造として説明できる。
- 誤検出を抑える境界条件をprofileから指定できる。
- 既存のCFR/EU/WHO/PIC/S/JP回帰テストに副作用を出さない。

個別profile/adapterへ閉じるもの:

- 特定文書のタイトル、通知名、表紙、序文、本文開始位置。
- 特定文書だけで確認された表崩れ、画像参照、別表境界。
- 文書ごとに意味が変わる番号階層。
- 対象外OKなど、文書別の候補表示範囲。

## 現在地

| 対象 | Parser開発状況 | 個別処理の残り |
| --- | --- | --- |
| 6 原薬GMPガイドライン | 本文階層と表1保持まで実施 | 表1 adapter、候補表示制御 |
| 7 無菌操作法指針 | 本文・参考情報階層まで実施 | 固定幅表候補、対象外OK範囲の候補表示制御 |
| 8 病原体等安全管理規程 | 8a本文条文まで実施 | 8b別表・付表 adapter、候補表示制御 |
| 9 CSVガイドライン | HTML抽出と本文階層まで実施 | 別紙画像/別紙表、対象外OK範囲の候補表示制御 |

## 優先順

### 1. 候補表示制御profile

目的:

- Parserで保持したIRから、DQチェックシート等で候補に出す範囲を文書別に制御する。
- 「対象外OK」をParser段階で削除せず、表示候補ルールとして扱う。

対象:

- 7: 冒頭から用語定義、改訂履歴など。
- 9: `1.1`, `1.2`, `2.10` など指定表上の対象外OK範囲。
- 8: 冒頭から定義、第5章、第6章など。
- 6: 用語集相当や表1周辺の候補扱い。

実装方針:

- `regdoc_profile` の `candidate_visibility` を文書別に拡張する。
- Parser profileには入れない。
- 条文・節・章のNID安定性を先にテストで固定する。

完了条件:

- 対象外範囲がIR上には残る。
- 候補抽出では対象外範囲が除外される。
- 除外理由をprofileまたはRUNに記録できる。

実装メモ:

- `src/qai_text2ir/candidate_visibility_profiles/` に文書別profileを置く。
- `text2ir bundle` では `--candidate-visibility-profile-id` または `--candidate-visibility-profile` で適用する。

### 2. 8b 別表・付表保持adapter

目的:

- 病原体等安全管理規程の `別表１` 以降を落とさず保持し、後段でtable化できる形にする。

対象:

- `別表１` から `別表１０`。
- `付表１－１` から `付表４`。
- 固定幅表、段落型表、複数ページにまたがる表。

実装方針:

- まずNIID専用profileで `別表` / `付表` をroot直下の `chapter` または `annex` 相当として保持する。
- 次に、表ごとに以下を分類する。
  - そのまま `preformatted` 保持でよいもの。
  - 行単位 `table_row` に分けられるもの。
  - 列復元が必要なもの。
- 列復元が必要なものだけ、`niid_pathogen_annex_adapter` として個別部品化する。

共通化しない理由:

- NIID別表は表題、付表、ページ分割、固定幅崩れの組み合わせが強く文書固有。
- 共通表検出を緩めると、通常本文をtable扱いするリスクが高い。

完了条件:

- `別表１` 以降がIR上で欠落しない。
- `special_structure_audit` で未解決ブロックが一覧化される。
- 最低限、表題と原文行を追跡可能なsource span付きで保持する。

### 3. 6 表1 adapter

目的:

- 原薬GMPガイドラインの `表１：原薬生産に対する本ガイドラインの適用` を個別adapterで安定保持する。

背景:

- RUN `20260525-121645707_run-normalized-api-gmp-guideline-v1` では、RUN内の整形済み入力で表1を1列markdown tableへ置換した。
- 共通parserにragged fixed-width table検出を入れる案は、通常本文の誤table化リスクがあるため採用しなかった。

実装方針:

- `api_gmp_table1_adapter` を個別部品として設計する。
- 入力はPDF抽出TXTの表1ブロック。
- 出力は当面1列 `raw_line` tableでよい。
- 列復元は、必要性がレビューで確認された後に別段階で行う。

完了条件:

- RUN内手作業置換なしで同等のtable保持ができる。
- 表1の行内容とsource spanが追跡できる。
- 本文章・節構造に副作用がない。

### 4. 7 固定幅表候補adapter

目的:

- 無菌操作法指針で残った固定幅表候補を、必要に応じて個別adapter化する。

対象候補:

- `cha7.p7_1`
- `cha11.p11_3`
- `cha11.p11_3.pre1`

実装方針:

- まず対象ブロックを原文行単位で切り出し、表として扱う必要があるかを確認する。
- 表でない場合は、`special_structure_audit` の検知条件調整を検討する。
- 表である場合のみ `aseptic_processing_table_adapter` を作る。

完了条件:

- 表候補ごとに「table化する/本文保持でよい/検知対象外」の判断がRUNに残る。
- table化する場合は個別adapterで処理し、共通表検出は緩めない。

### 5. 9 別紙adapter

目的:

- CSVガイドラインの `別紙1` / `別紙2` を、本文とは別の個別部品として扱う。

現状:

- `別紙1` はHTML上で画像参照として抽出される。
- `別紙2` は表題行のみが本文抽出に残る。

実装方針:

- `extract-mhlw-html` の出力だけで完結させるか、HTML内画像/リンクを追跡するかを先に決める。
- `別紙1` は画像OCRまたは画像メタ情報保持が必要かを確認する。
- `別紙2` はHTML本文に表構造が残っているかを再確認する。
- 必要なら `mhlw_csv_annex_adapter` として、HTML抽出後の別紙処理を分離する。

完了条件:

- 別紙の有無、形式、抽出可否がRUNで追跡できる。
- 本文Parser profileに別紙固有処理を混ぜない。

## フェーズ案

| フェーズ | ブランチ案 | 内容 | PR停止点 |
| --- | --- | --- | --- |
| A | `feat/candidate-visibility-profiles-6-9` | 対象外OKを候補表示制御に落とす | 4文書のprofile案とテスト |
| B | `feat/niid-pathogen-annex-adapter-v1` | 8b別表・付表の保持形確認と最小adapter | 別表欠落なし、監査結果付き |
| C | `feat/api-gmp-table1-adapter-v1` | 6表1の手作業置換を個別adapter化 | RUN内置換なしで同等出力 |
| D | `feat/aseptic-processing-table-candidates-v1` | 7固定幅表候補の判定と必要分adapter | 候補別判断表と必要な出力 |
| E | `feat/mhlw-csv-annex-adapter-v1` | 9別紙の抽出可否確認と必要分adapter | 別紙の保持/非保持判断 |

## 記録対象

各個別adapter RUNでは、最低限以下を残す。

- 対象ブロックの原文範囲。
- 共通化しない理由。
- adapter入力と出力の契約。
- `goal_check` / `special_structure_audit` の結果。
- 候補表示に影響する場合は、Parser処理とcandidate visibility処理の境界。

## 参照RUN

- `runs/20260525-120304474_feat-jp-text2ir-base/RUN.md`
- `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/RUN.md`
- `runs/20260525-121645707_run-normalized-api-gmp-guideline-v1/ADAPTER_NOTES.md`
- `runs/20260525-133209443_feat-aseptic-processing-parser-v1/RUN.md`
- `runs/20260525-134750168_feat-csv-guideline-parser-v1/RUN.md`
- `runs/20260525-135841668_feat-niid-pathogen-safety-parser-v1/RUN.md`
