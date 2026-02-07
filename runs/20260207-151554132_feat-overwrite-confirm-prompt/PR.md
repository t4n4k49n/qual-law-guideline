## 概要

`serialize.py` に上書き確認を追加し、既存ファイルへ書き込む際に `Overwrite?"Yes"` を1回だけ確認するようにしました。

## 変更内容

- `src/qai_xml2ir/serialize.py`
  - 既存ファイルへ書く場合のみ確認プロンプトを表示
  - 入力が厳密一致 `Yes` のときのみ上書きを許可（大文字・小文字区別）
  - 最初の1回だけ確認し、`Yes` 後は同一プロセス内の全上書きを許可
  - `Yes` 以外は `FileExistsError` を送出して停止
- `tests/test_serialize_overwrite.py`
  - `yes` では拒否されること
  - `Yes` を1回入力後は複数ファイルの上書きが継続許可されること
  - 確認が1回だけであること

## テスト

- `python -m pytest -q`
- 結果: `8 passed, 1 skipped`
