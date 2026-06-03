# RUN: yaml 4-set gap report

## run_id

`20260603-014940040_feat-yaml-4set-gap-report-v1`

## branch

`feat/yaml-4set-gap-report-v1`

## 目的

旧ダウンロードzip `qual-law-guideline-main_0210-1000.zip` に含まれる正式版4点YAMLと、現行 `main` の `data/normalized` 4点YAMLのギャップを整理する。

Devin が旧YAMLを前提に DQ チェックリストを実装していたため、現行YAMLで再実装する際の影響範囲を、人向け・AIエンジニア向けの両方で読めるMarkdownとして出す。

## 入力

- 旧zip: `%USERPROFILE%\Downloads\qual-law-guideline-main_0210-1000.zip`
- 現行正式版: `data/normalized`

## 出力

- 共有用レポート: `runs/20260603-014940040_feat-yaml-4set-gap-report-v1/YAML_4SET_GAP_REPORT.md`
- 比較スクリプト: `runs/20260603-014940040_feat-yaml-4set-gap-report-v1/compare_yaml_4sets.py`
- 構造契約抽出スクリプト: `runs/20260603-014940040_feat-yaml-4set-gap-report-v1/analyze_yaml_contract.py`
- 比較JSON: `out/20260603-014940040_feat-yaml-4set-gap-report-v1/yaml_4set_gap_summary.json`
- 構造契約JSON: `out/20260603-014940040_feat-yaml-4set-gap-report-v1/yaml_contract_summary.json`

## 実施内容

1. 旧zip内の `data/normalized` 配下にある4点YAMLを抽出対象にした。
2. 現行 `data/normalized` 配下の4点YAMLを抽出対象にした。
3. doc_id単位で、4ファイル有無、SHA-256、IRノード数、kind構成、最大深さを比較した。
4. 旧zip版と現行YAMLから、4ファイル別キーパス、IR kind集合、IRノードキー集合、profile必須パスを抽出した。
5. チーフエンジニア向けの判断ポイントと、Devin向けの実装契約を1つのMarkdownにまとめた。
6. UIモック相当の候補表示・チェックシート表示・文脈表示に限る論点へ `【UI-MOC相当】` マークを付け、Devin側に同等UI実装がない場合は必須対応に含めないことを明記した。

## 結果概要

- 旧zip版: 5セット
- 現行: 27セット
- 現行のみ: 22セット
- 旧zip版のみ: 0セット
- 共通5セット: すべて変更あり

旧zip版の一部 `meta.yaml` には、未クォートの `%USERPROFILE%...` パスにより標準YAMLとしてパースできないものがあった。比較ではハッシュと所在は記録しつつ、現行版を正として扱った。

現行IRで旧zip版になかったkindは次の9種類。

`figure`, `note`, `part`, `preamble`, `statement`, `subpart`, `table`, `table_header`, `table_row`

## 検証

比較スクリプトを実行し、以下のサマリを得た。

```json
{
  "old_total": 5,
  "old_complete": 5,
  "current_total": 27,
  "current_complete": 27,
  "common": 5,
  "current_only": 22,
  "old_only": 0,
  "changed_common": 5,
  "unchanged_common": 0
}
```
