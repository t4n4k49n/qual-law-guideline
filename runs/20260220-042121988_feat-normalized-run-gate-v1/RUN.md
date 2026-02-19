# RUN: 20260220-042121988_feat-normalized-run-gate-v1

- branch: feat/normalized-run-gate-v1
- purpose: normalized-run-gate を導入し、正規化RUN PRのマージ前条件を機械判定する。

## Changes
- .github/workflows/normalized-run-gate.yml を追加
- docs/NORMALIZED_RUN_PLAYBOOK.md を最小追記

## Notes
- このRUNでは data/normalized の昇格は実施しない。
- チェック実行確認は別PRでスモーク実施する。
